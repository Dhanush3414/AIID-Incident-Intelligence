
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pathlib import Path
from functools import lru_cache
from datetime import datetime
import pandas as pd
import numpy as np
import joblib
import json
import os
import tempfile
import math

from similar_incidents import (
    load_incidents,
    build_similarity_index,
    find_similar_incidents
)

from rag.rag_pipeline import (
    load_faiss_index,
    retrieve_similar_incidents,
    generate_investigation_report
)


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

REPORTS_PATH = (
    PROJECT_DIR / "data" / "processed" / "investigation_reports.json"
)

MODEL_PATH = (
    PROJECT_DIR / "models" / "classification"
    / "risk_domain_classifier.joblib"
)

VECTORIZER_PATH = (
    PROJECT_DIR / "models" / "tfidf"
    / "tfidf_vectorizer.joblib"
)

DATASET_PATH = (
    PROJECT_DIR / "data" / "processed"
    / "incidents_feature_engineered.csv"
)


# ==========================================
# JSON DATA CLEANING
# ==========================================

def clean_for_json(value):
    """
    Convert NumPy and Pandas values into JSON-compatible values.
    Replace NaN, Infinity, and missing values with None.
    """

    if isinstance(value, dict):
        return {
            str(key): clean_for_json(val)
            for key, val in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            clean_for_json(item)
            for item in value
        ]

    if isinstance(value, np.ndarray):
        return clean_for_json(value.tolist())

    if isinstance(value, np.generic):
        value = value.item()

    if value is None or value is pd.NA or value is pd.NaT:
        return None

    if isinstance(value, (datetime, pd.Timestamp)):
        return value.isoformat()

    if isinstance(value, float):
        if not math.isfinite(value):
            return None

    return value


# ==========================================
# REPORT STORAGE FUNCTIONS
# ==========================================

def load_saved_reports():

    if not REPORTS_PATH.exists():
        return []

    try:
        with open(REPORTS_PATH, "r", encoding="utf-8") as file:
            reports = json.load(file)

        if not isinstance(reports, list):
            raise ValueError(
                "Report storage must contain a JSON list."
            )

        # Clean old reports containing NaN or Infinity.
        reports = clean_for_json(reports)

        return reports

    except (json.JSONDecodeError, OSError, ValueError) as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to read saved reports: {str(error)}"
        )


def save_investigation_report(report):

    REPORTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    reports = load_saved_reports()

    # Clean the new report before saving.
    report = clean_for_json(report)

    reports.insert(0, report)

    # Clean the complete report history.
    reports = clean_for_json(reports)

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".tmp",
            dir=REPORTS_PATH.parent,
            delete=False
        ) as file:

            temp_path = file.name

            json.dump(
                reports,
                file,
                indent=4,
                ensure_ascii=False,
                allow_nan=False
            )

        os.replace(temp_path, REPORTS_PATH)

    except Exception:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        raise


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="AIID Incident Intelligence API",
    description="Backend API for AI-powered incident investigation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def home():

    return {
        "message": "AIID Incident Intelligence API is running",
        "status": "success"
    }


@app.get("/api/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AIID Backend"
    }


# ==========================================
# DASHBOARD STATISTICS
# ==========================================

@app.get("/api/dashboard/stats")
def get_dashboard_stats():

    if not DATASET_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Dashboard dataset not found."
        )

    df = pd.read_csv(DATASET_PATH)

    total_incidents = len(df)

    classified_df = df[
        df["Risk Domain"].notna()
        & (df["Risk Domain"].astype(str).str.strip() != "")
    ]

    classified_incidents = len(classified_df)

    unclassified_incidents = (
        total_incidents - classified_incidents
    )

    risk_distribution = (
        classified_df["Risk Domain"]
        .value_counts()
        .to_dict()
    )

    return {
        "total_incidents": total_incidents,
        "classified_incidents": classified_incidents,
        "unclassified_incidents": unclassified_incidents,
        "risk_domains_count": len(risk_distribution),

        "risk_distribution": [
            {
                "domain": str(domain),
                "count": int(count)
            }
            for domain, count in risk_distribution.items()
        ],

        "classification_distribution": [
            {
                "status": "Classified",
                "count": classified_incidents
            },
            {
                "status": "Unclassified",
                "count": unclassified_incidents
            }
        ]
    }


# ==========================================
# HISTORICAL INCIDENTS
# ==========================================

@app.get("/api/incidents")
def get_incidents(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=100),
    search: str = "",
    domain: str = ""
):

    if not DATASET_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Historical incidents dataset not found."
        )

    df = pd.read_csv(DATASET_PATH)

    df = df.fillna("Unknown")

    if search:

        mask = (
            df["title"].astype(str).str.contains(
                search,
                case=False,
                na=False
            )
            |
            df["description"].astype(str).str.contains(
                search,
                case=False,
                na=False
            )
        )

        df = df[mask]

    if domain and domain != "All Domains":

        df = df[
            df["Risk Domain"].astype(str) == domain
        ]

    total = len(df)

    total_pages = (
        total + page_size - 1
    ) // page_size

    start = (page - 1) * page_size

    records = df.iloc[
        start:start + page_size
    ].to_dict(orient="records")

    return jsonable_encoder(
        clean_for_json({
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "incidents": records
        })
    )


# ==========================================
# INCIDENT INVESTIGATION REQUEST
# ==========================================

class InvestigationRequest(BaseModel):

    title: str = ""

    description: str = ""

    generate_rag_report: bool = True


# ==========================================
# LOAD ML, SIMILARITY AND RAG RESOURCES
# ==========================================

@lru_cache(maxsize=1)
def load_analysis_resources():

    model = joblib.load(MODEL_PATH)

    vectorizer = joblib.load(VECTORIZER_PATH)

    historical_df = load_incidents()

    similarity_vectorizer, incident_vectors = (
        build_similarity_index(historical_df)
    )

    rag_index, rag_metadata = load_faiss_index()

    return (
        model,
        vectorizer,
        historical_df,
        similarity_vectorizer,
        incident_vectors,
        rag_index,
        rag_metadata
    )


# ==========================================
# INCIDENT INVESTIGATION API
# ==========================================

@app.post("/api/investigate")
def investigate_incident(request: InvestigationRequest):

    if (
        not request.title.strip()
        and not request.description.strip()
    ):

        raise HTTPException(
            status_code=400,
            detail="Enter an incident title or description."
        )

    try:

        (
            model,
            vectorizer,
            historical_df,
            similarity_vectorizer,
            incident_vectors,
            rag_index,
            rag_metadata
        ) = load_analysis_resources()

        # ----------------------------------
        # 1. ML RISK CLASSIFICATION
        # ----------------------------------

        combined_text = (
            request.title.strip()
            + " "
            + request.description.strip()
        ).strip()

        text_features = vectorizer.transform(
            [combined_text]
        )

        predicted_domain = model.predict(
            text_features
        )[0]

        probabilities = {}

        if hasattr(model, "predict_proba"):

            prediction_values = model.predict_proba(
                text_features
            )[0]

            probabilities = {
                str(label): float(probability)
                for label, probability in zip(
                    model.classes_,
                    prediction_values
                )
            }

        # ----------------------------------
        # 2. SIMILAR HISTORICAL INCIDENTS
        # ----------------------------------

        similar_results = find_similar_incidents(
            title=request.title,
            description=request.description,
            df=historical_df,
            vectorizer=similarity_vectorizer,
            incident_vectors=incident_vectors,
            top_n=5
        )

        similar_records = similar_results.to_dict(
            orient="records"
        )

        # ----------------------------------
        # 3. RAG INVESTIGATION
        # ----------------------------------

        rag_records = []

        investigation_report = None

        if request.generate_rag_report:

            rag_results = retrieve_similar_incidents(
                query=combined_text,
                df=rag_metadata,
                index=rag_index,
                top_k=5
            )

            rag_records = rag_results.to_dict(
                orient="records"
            )

            if not rag_results.empty:

                investigation_report = (
                    generate_investigation_report(
                        incident_title=request.title,
                        incident_description=request.description,
                        retrieved_incidents=rag_results
                    )
                )

        # ----------------------------------
        # 4. PREPARE INVESTIGATION REPORT
        # ----------------------------------

        now = datetime.now()

        report_data = {
            "id": now.strftime("%Y%m%d%H%M%S%f"),

            "created_at": now.isoformat(),

            "title": request.title,

            "description": request.description,

            "predicted_domain": str(predicted_domain),

            "probabilities": probabilities,

            "similar_incidents": similar_records,

            "rag_evidence": rag_records,

            "investigation_report": investigation_report
        }

        # Convert Pandas, NumPy and other values.
        report_data = jsonable_encoder(report_data)

        # Remove NaN and Infinity values.
        report_data = clean_for_json(report_data)

        # ----------------------------------
        # 5. SAVE INVESTIGATION REPORT
        # ----------------------------------

        save_investigation_report(report_data)

        return {
            "status": "success",
            **report_data
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Investigation failed: {str(error)}"
        )


# ==========================================
# GET SAVED INVESTIGATION REPORTS
# ==========================================

@app.get("/api/reports")
def get_investigation_reports():

    reports = load_saved_reports()

    # Ensure all previously saved reports are JSON-safe.
    reports = clean_for_json(reports)

    return {
        "total": len(reports),
        "reports": reports
    }


# ==========================================
# CLEAR SAVED INVESTIGATION REPORTS
# ==========================================

@app.delete("/api/reports")
def clear_investigation_reports():

    REPORTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        REPORTS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            [],
            file,
            indent=4,
            allow_nan=False
        )

    return {
        "status": "success",
        "message": "All investigation reports have been cleared.",
        "total": 0
    }
