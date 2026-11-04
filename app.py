from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
import plotly.express as px
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

# --------------------------------------------------
# 1. Application configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AIID Incident Intelligence",
    page_icon="🤖",
    layout="wide"
)

PROJECT_DIR = Path(__file__).resolve().parent

MODEL_PATH = (
    PROJECT_DIR
    / "models"
    / "classification"
    / "risk_domain_classifier.joblib"
)

VECTORIZER_PATH = (
    PROJECT_DIR
    / "models"
    / "tfidf"
    / "tfidf_vectorizer.joblib"
)


# --------------------------------------------------
# 2. Load the trained model and vectorizer
# --------------------------------------------------

@st.cache_resource
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer

# --------------------------------------------------
# Load historical incidents for similarity search
# --------------------------------------------------

@st.cache_resource
def load_similarity_resources():

    historical_df = load_incidents()

    similarity_vectorizer, incident_vectors = (
        build_similarity_index(historical_df)
    )

    return (
        historical_df,
        similarity_vectorizer,
        incident_vectors
    )

# --------------------------------------------------
# Load RAG resources
# --------------------------------------------------

@st.cache_resource
def load_rag_resources():

    rag_index, rag_metadata = load_faiss_index()

    return rag_index, rag_metadata

# --------------------------------------------------
# Dashboard header and KPI cards
# --------------------------------------------------

st.title("🤖 AIID Incident Intelligence")
st.subheader("AI Incident Risk Domain Classification")

st.markdown(
    """
    An intelligent dashboard for exploring AI incidents and
    predicting their risk domains using machine learning.
    """
)

# KPI values from the completed project analysis
total_incidents = 1749
classified_incidents = 1496
risk_domains = 7
model_accuracy = 72.67

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Incidents",
        value=f"{total_incidents:,}"
    )

with col2:
    st.metric(
        label="Classified Incidents",
        value=f"{classified_incidents:,}"
    )

with col3:
    st.metric(
        label="Risk Domains",
        value=risk_domains
    )

with col4:
    st.metric(
        label="Model Accuracy",
        value=f"{model_accuracy:.2f}%"
    )

st.divider()

# --------------------------------------------------
# Risk subdomain analysis
# --------------------------------------------------

st.header("🔎 Risk Subdomain Analysis")

SUBDOMAIN_FILE = (
    PROJECT_DIR
    / "results"
    / "analysis"
    / "risk_subdomain_distribution.csv"
)

if SUBDOMAIN_FILE.exists():

    subdomain_df = pd.read_csv(SUBDOMAIN_FILE)

    subdomain_df.columns = subdomain_df.columns.str.strip()

    subdomain_column = subdomain_df.columns[0]
    count_column = subdomain_df.columns[1]

    subdomain_df[count_column] = pd.to_numeric(
        subdomain_df[count_column],
        errors="coerce"
    )

    subdomain_df = subdomain_df.dropna(
        subset=[subdomain_column, count_column]
    )

    subdomain_df = subdomain_df.sort_values(
        by=count_column,
        ascending=False
    ).head(10)

    total_subdomain_records = int(
        subdomain_df[count_column].sum()
    )

    st.caption(
        "The following chart shows the ten most frequently "
        "recorded risk subdomains among classified incidents."
    )

    col1, col2 = st.columns([2, 1])

    with col1:

        st.subheader("Top 10 Risk Subdomains")

        fig = px.bar(
            subdomain_df,
            x=count_column,
            y=subdomain_column,
            orientation="h",
            text=count_column,
            title="Most Frequently Recorded Risk Subdomains",
            labels={
                subdomain_column: "Risk Subdomain",
                count_column: "Number of Incidents"
            }
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate=(
                "Risk Subdomain: %{y}<br>"
                "Number of Incidents: %{x}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            },
            xaxis_title="Number of Incidents",
            yaxis_title="Risk Subdomain",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Subdomain Summary")

        display_df = subdomain_df.rename(
            columns={
                subdomain_column: "Risk Subdomain",
                count_column: "Incident Count"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        if not subdomain_df.empty:

            top_subdomain = subdomain_df.iloc[0]

            st.metric(
                "Most Frequent Risk Subdomain",
                f"{int(top_subdomain[count_column]):,} incidents"
            )

            st.caption(
                str(top_subdomain[subdomain_column])
            )

    with st.expander("View top 10 risk subdomain data"):

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

else:

    st.warning(
        "Risk subdomain distribution file was not found."
    )

st.divider()

# --------------------------------------------------
# Responsible Entity Analysis
# --------------------------------------------------

st.header("👥 Responsible Entity Analysis")

ENTITY_FILE = (
    PROJECT_DIR
    / "results"
    / "analysis"
    / "responsible_entity_distribution.csv"
)

if ENTITY_FILE.exists():

    entity_df = pd.read_csv(ENTITY_FILE)

    # Ensure the incident counts are numeric.
    count_column = entity_df.columns[1]
    entity_df[count_column] = pd.to_numeric(
        entity_df[count_column],
        errors="coerce"
    )

    entity_df = entity_df.dropna(
        subset=[entity_df.columns[0], count_column]
    )

    # Calculate percentages.
    total_incidents = entity_df[count_column].sum()

    entity_df["Percentage"] = (
        entity_df[count_column] / total_incidents * 100
    ).round(2)

    st.caption(
        "Distribution of AI incidents by their recorded "
        "responsible entity classification."
    )

    st.metric(
        "Total Classified Entity Records",
        f"{int(total_incidents):,}"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Incidents by Responsible Entity")

        entity_chart = entity_df.rename(
            columns={
                entity_df.columns[0]: "Responsible Entity",
                count_column: "Incident Count"
            }
        )

        fig = px.bar(
            entity_chart.sort_values("Incident Count"),
            x="Incident Count",
            y="Responsible Entity",
            orientation="h",
            text="Incident Count",
            title="Responsible Entity Distribution",
            labels={
                "Incident Count": "Number of Incidents",
                "Responsible Entity": "Responsible Entity"
            }
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            yaxis_title="Responsible Entity",
            xaxis_title="Number of Incidents",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:
        st.subheader("Entity Summary")

        st.dataframe(
            entity_df.rename(
                columns={
                    entity_df.columns[0]: "Responsible Entity",
                    count_column: "Incident Count"
                }
            ),
            use_container_width=True,
            hide_index=True
        )

        # Identify the most frequent entity.
        top_entity = entity_df.loc[
            entity_df[count_column].idxmax()
        ]

        st.subheader("Key Observation")

        st.write(
            f"**{top_entity.iloc[0]}** is the most frequently "
            f"recorded responsible entity, with "
            f"**{int(top_entity[count_column]):,} incidents** "
            f"({top_entity['Percentage']:.2f}% of classified records)."
        )

    with st.expander("View detailed responsible entity data"):

        st.dataframe(
            entity_df.rename(
                columns={
                    entity_df.columns[0]: "Responsible Entity",
                    count_column: "Incident Count"
                }
            ),
            use_container_width=True,
            hide_index=True
        )

else:
    st.warning(
        "Responsible entity distribution file was not found."
    )

st.divider()

# --------------------------------------------------
# Incident Timing Analysis
# --------------------------------------------------

st.header("⏱️ Incident Timing Analysis")

TIMING_FILE = (
    PROJECT_DIR
    / "results"
    / "analysis"
    / "timing_distribution.csv"
)

if TIMING_FILE.exists():

    timing_df = pd.read_csv(TIMING_FILE)

    # Identify the columns.
    timing_column = timing_df.columns[0]
    count_column = timing_df.columns[1]

    # Ensure incident counts are numeric.
    timing_df[count_column] = pd.to_numeric(
        timing_df[count_column],
        errors="coerce"
    )

    timing_df = timing_df.dropna(
        subset=[timing_column, count_column]
    )

    # Calculate percentages.
    total_incidents = timing_df[count_column].sum()

    timing_df["Percentage"] = (
        timing_df[count_column] / total_incidents * 100
    ).round(2)

    st.caption(
        "Distribution of AI incidents according to their "
        "recorded timing in the AI Incident Database."
    )

    # Total classified records.
    st.metric(
        "Total Classified Timing Records",
        f"{int(total_incidents):,}"
    )

    col1, col2 = st.columns(2)

    # ------------------------------
    # Timing distribution chart
    # ------------------------------
    with col1:

        st.subheader("Incidents by Timing")

        chart_df = timing_df.rename(
            columns={
                timing_column: "Incident Timing",
                count_column: "Incident Count"
            }
        ).sort_values("Incident Count")

        fig = px.bar(
            chart_df,
            x="Incident Count",
            y="Incident Timing",
            orientation="h",
            text="Incident Count",
            title="Recorded Incident Timing",
            labels={
                "Incident Count": "Number of Incidents",
                "Incident Timing": "Incident Timing"
            }
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Number of Incidents",
            yaxis_title="Incident Timing",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ------------------------------
    # Timing summary table
    # ------------------------------
    with col2:

        st.subheader("Timing Summary")

        display_df = timing_df.rename(
            columns={
                timing_column: "Incident Timing",
                count_column: "Incident Count"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # Find the most frequently recorded timing.
        top_timing = timing_df.loc[
            timing_df[count_column].idxmax()
        ]

        st.subheader("Key Observation")

        st.write(
            f"**{top_timing[timing_column]}** is the most "
            f"frequently recorded incident timing, with "
            f"**{int(top_timing[count_column]):,} incidents** "
            f"({top_timing['Percentage']:.2f}% of classified records)."
        )

    # ------------------------------
    # Detailed timing data
    # ------------------------------
    with st.expander("View detailed incident timing data"):

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

else:
    st.warning(
        "Incident timing distribution file was not found."
    )

st.divider()

# --------------------------------------------------
# AI Harm Level Analysis
# --------------------------------------------------

st.header("⚠️ AI Harm Level Analysis")

HARM_LEVEL_FILE = (
    PROJECT_DIR
    / "results"
    / "analysis"
    / "ai_harm_level_distribution.csv"
)

if HARM_LEVEL_FILE.exists():

    harm_df = pd.read_csv(HARM_LEVEL_FILE)

    # Identify the columns.
    harm_column = harm_df.columns[0]
    count_column = harm_df.columns[1]

    # Convert incident counts to numeric values.
    harm_df[count_column] = pd.to_numeric(
        harm_df[count_column],
        errors="coerce"
    )

    harm_df = harm_df.dropna(
        subset=[harm_column, count_column]
    )

    # Calculate percentages.
    total_incidents = harm_df[count_column].sum()

    harm_df["Percentage"] = (
        harm_df[count_column] / total_incidents * 100
    ).round(2)

    st.caption(
        "Distribution of AI incidents by their recorded AI harm level. "
        "This analysis includes only records with a recorded harm-level "
        "classification."
    )

    # Total classified records.
    st.metric(
        "Total Classified Harm-Level Records",
        f"{int(total_incidents):,}"
    )

    col1, col2 = st.columns(2)

    # -----------------------------------------------
    # Harm level distribution chart
    # -----------------------------------------------
    with col1:

        st.subheader("Incidents by AI Harm Level")

        chart_df = harm_df.rename(
            columns={
                harm_column: "AI Harm Level",
                count_column: "Incident Count"
            }
        ).sort_values("Incident Count")

        fig = px.bar(
            chart_df,
            x="Incident Count",
            y="AI Harm Level",
            orientation="h",
            text="Incident Count",
            title="Recorded AI Harm-Level Distribution",
            labels={
                "Incident Count": "Number of Incidents",
                "AI Harm Level": "AI Harm Level"
            }
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Number of Incidents",
            yaxis_title="AI Harm Level",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------------------------
    # Harm level summary
    # -----------------------------------------------
    with col2:

        st.subheader("Harm Level Summary")

        display_df = harm_df.rename(
            columns={
                harm_column: "AI Harm Level",
                count_column: "Incident Count"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # Identify the most frequent recorded classification.
        top_harm = harm_df.loc[
            harm_df[count_column].idxmax()
        ]

        st.subheader("Key Observation")

        st.write(
            f"The most frequently recorded harm-level classification "
            f"is **{top_harm[harm_column]}**, with "
            f"**{int(top_harm[count_column]):,} incidents** "
            f"({top_harm['Percentage']:.2f}% of classified records)."
        )

    # -----------------------------------------------
    # Detailed harm-level data
    # -----------------------------------------------
    with st.expander("View detailed AI harm-level data"):

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

else:
    st.warning(
        "AI harm level distribution file was not found."
    )

st.divider()

# --------------------------------------------------
# Yearly incident trends
# --------------------------------------------------

st.header("📈 Yearly AI Incident Trends")

YEARLY_TRENDS_FILE = (
    PROJECT_DIR
    / "results"
    / "analysis"
    / "yearly_incident_trends.csv"
)

if YEARLY_TRENDS_FILE.exists():

    # Load yearly incident data
    yearly_df = pd.read_csv(YEARLY_TRENDS_FILE)

    # Identify year and incident-count columns
    year_column = yearly_df.columns[0]
    count_column = yearly_df.columns[1]

    # Convert columns to numeric values
    yearly_df[year_column] = pd.to_numeric(
        yearly_df[year_column],
        errors="coerce"
    )

    yearly_df[count_column] = pd.to_numeric(
        yearly_df[count_column],
        errors="coerce"
    )

    # Remove invalid rows and sort chronologically
    yearly_df = (
        yearly_df
        .dropna(subset=[year_column, count_column])
        .sort_values(by=year_column)
        .copy()
    )

    yearly_df[year_column] = yearly_df[year_column].astype(int)

    # Create interactive Plotly line chart
    fig = px.line(
        yearly_df,
        x=year_column,
        y=count_column,
        markers=True,
        title="Recorded AI Incidents by Year",
        labels={
            year_column: "Year",
            count_column: "Number of Incidents"
        },
        hover_data={
            year_column: True,
            count_column: True
        }
    )

    # Improve chart appearance
    fig.update_xaxes(
        tickmode="linear",
        dtick=2,
        range=[
            int(yearly_df[year_column].min()) - 0.5,
            int(yearly_df[year_column].max()) + 0.5
        ]
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Recorded Incidents",
        hovermode="x unified",
        height=450
    )

    # Display chart
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Annual counts of incidents recorded in the AI Incident Database. "
        "The 2026 count represents a partial year because the dataset "
        "currently contains incidents only through October 7, 2026."
    )

    # Display the underlying data
    with st.expander("View yearly incident data"):
        st.dataframe(
            yearly_df,
            use_container_width=True,
            hide_index=True
        )

        # Download yearly data
        csv_data = yearly_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download yearly incident data",
            data=csv_data,
            file_name="yearly_incident_trends.csv",
            mime="text/csv"
        )

else:
    st.warning(
        "Yearly incident trends file was not found."
    )

st.divider()

# --------------------------------------------------
# Incident intent distribution
# --------------------------------------------------

st.header("🎯 Incident Intent Analysis")

INTENT_FILE = (
    PROJECT_DIR
    / "results"
    / "analysis"
    / "intent_distribution.csv"
)

if INTENT_FILE.exists():

    intent_df = pd.read_csv(INTENT_FILE)

    # Identify columns safely
    intent_column = intent_df.columns[0]
    count_column = intent_df.columns[1]

    # Clean and validate data
    intent_df[intent_column] = intent_df[intent_column].astype(str)
    intent_df[count_column] = pd.to_numeric(
        intent_df[count_column],
        errors="coerce"
    )

    intent_df = intent_df.dropna(subset=[count_column])
    intent_df = intent_df.sort_values(
        by=count_column,
        ascending=False
    )

    total_intent_records = int(intent_df[count_column].sum())

    # Calculate percentages
    intent_df["Percentage"] = (
        intent_df[count_column] / total_intent_records * 100
    ).round(2)

    st.caption(
        "Distribution of incidents by their recorded intent classification."
    )

    # KPI
    st.metric(
        "Total Classified Intent Records",
        f"{total_intent_records:,}"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Intent Distribution")

        fig = px.bar(
            intent_df,
            x=count_column,
            y=intent_column,
            orientation="h",
            text=count_column,
            title="Incidents by Intent",
            labels={
                intent_column: "Intent",
                count_column: "Number of Incidents"
            }
        )

        fig.update_traces(
        textposition="outside",
        hovertemplate=(
        "Intent: %{y}<br>"
        "Number of Incidents: %{x}<br>"
        "<extra></extra>"
        )
)

        fig.update_layout(
            yaxis_title="Intent",
            xaxis_title="Number of Incidents",
            yaxis={"categoryorder": "total ascending"},
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:
        st.subheader("Intent Summary")

        display_df = intent_df.rename(
            columns={
                intent_column: "Intent",
                count_column: "Incident Count"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.write("**Key Observation**")

        if not intent_df.empty:
            dominant_intent = intent_df.iloc[0][intent_column]
            dominant_count = int(
                intent_df.iloc[0][count_column]
            )
            dominant_percentage = (
                dominant_count / total_intent_records * 100
            )

            st.write(
                f"**{dominant_intent}** is the most frequent "
                f"recorded intent, with {dominant_count:,} incidents "
                f"({dominant_percentage:.2f}%)."
            )

    with st.expander("View detailed intent data"):
        st.dataframe(
            intent_df,
            use_container_width=True,
            hide_index=True
        )

else:
    st.warning(
        "Intent distribution file was not found."
    )

st.divider()

st.write(
    """
    Enter the title and description of an AI-related incident.
    The application will use a trained machine learning model
    to predict its most likely risk domain.
    """
)

st.info(
    "This application uses a TF-IDF text vectorizer and a "
    "Logistic Regression classifier trained on labelled AI "
    "Incident Database records."
)


# --------------------------------------------------
# 3. Check and load model files
# --------------------------------------------------

if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
    st.error(
        "Model files could not be found. Please check that "
        "the trained model and TF-IDF vectorizer exist in "
        "the expected models folders."
    )
    st.stop()

try:
    model, vectorizer = load_artifacts()
except Exception as error:
    st.error(f"Unable to load model artifacts: {error}")
    st.stop()

# Load the historical incident dataset and its similarity index.
try:
    (
        historical_df,
        similarity_vectorizer,
        incident_vectors
    ) = load_similarity_resources()
except Exception as error:
    st.error(f"Unable to load historical incidents: {error}")
    st.stop()

# --------------------------------------------------
# Load saved RAG resources
# --------------------------------------------------

try:
    rag_index, rag_metadata = load_rag_resources()

    st.success(
        f"RAG resources loaded successfully: "
        f"{rag_index.ntotal} historical incidents."
    )

except Exception as error:
    st.error(f"Unable to load RAG resources: {error}")
    st.stop()

# --------------------------------------------------
# 4. Incident input form
# --------------------------------------------------

st.header("Enter Incident Details")

with st.form("incident_prediction_form"):

    incident_title = st.text_input(
        "Incident Title",
        placeholder="Example: AI chatbot provides misleading medical information"
    )

    incident_description = st.text_area(
        "Incident Description",
        placeholder=(
            "Describe what happened, the AI system involved, "
            "and the possible consequences."
        ),
        height=180
    )

    generate_rag_report = st.checkbox(
        "Generate AI Incident Investigation Report (RAG)",
        value=False
    )

    submitted = st.form_submit_button(
        "Predict Risk Domain",
        type="primary"
    )


# --------------------------------------------------
# 5. Prediction and similar historical incidents
# --------------------------------------------------

if submitted:

    if not incident_title.strip() and not incident_description.strip():
        st.warning(
            "Please enter an incident title or description."
        )

    else:
        combined_text = (
            incident_title.strip() + " " + incident_description.strip()
        ).strip()

        try:
            # ------------------------------------------
            # Risk domain prediction
            # ------------------------------------------
            text_features = vectorizer.transform([combined_text])
            predicted_domain = model.predict(text_features)[0]

            st.divider()
            st.header("Prediction Results")

            st.success(
                f"Predicted Risk Domain: {predicted_domain}"
            )

            # Display estimated class probabilities.
             # Display estimated class probabilities.
            if hasattr(model, "predict_proba"):

                try:
                    # Fix compatibility with the saved LogisticRegression model.
                    if not hasattr(model, "multi_class"):
                        model.multi_class = "auto"

                    probabilities = model.predict_proba(text_features)[0]

                    probability_table = pd.DataFrame(
                        {
                            "Risk Domain": model.classes_,
                            "Estimated Probability": probabilities
                        }
                    ).sort_values(
                        by="Estimated Probability",
                        ascending=False
                    ).reset_index(drop=True)

                    top_probability = float(probabilities.max())

                    st.metric(
                        "Top Estimated Probability",
                        f"{top_probability:.2%}"
                    )

                    st.caption(
                        "These probabilities are model estimates, not "
                        "guaranteed confidence levels."
                    )

                    st.subheader("Probability by Risk Domain")

                    st.bar_chart(
                        probability_table.set_index("Risk Domain")[
                            "Estimated Probability"
                        ]
                    )

                    with st.expander("View probability table"):
                        st.dataframe(
                            probability_table.style.format(
                                {"Estimated Probability": "{:.2%}"}
                            ),
                            use_container_width=True
                        )

                except Exception as probability_error:
                    st.warning(
                        f"Probability display failed: {probability_error}"
                    )

            # ------------------------------------------
            # Similar historical incident retrieval
            # ------------------------------------------
            st.divider()
            st.header("🔍 Similar Historical Incidents")
            st.write(
                "These historical incidents have text that is similar to "
                "the incident you entered. Similarity is based on TF-IDF "
                "and cosine similarity."
            )

            similar_results = find_similar_incidents(
                title=incident_title,
                description=incident_description,
                df=historical_df,
                vectorizer=similarity_vectorizer,
                incident_vectors=incident_vectors,
                top_n=5
            )

            if similar_results.empty:
                st.info("No similar historical incidents were found.")
            else:
                st.subheader("Top 5 Similar Historical Incidents")

                for index, row in similar_results.iterrows():
                    with st.expander(
                        f"Incident {index + 1}: {row['title']}"
                    ):
                        st.write(f"**Incident ID:** {row['Incident ID']}")
                        st.write(
                            f"**Recorded Risk Domain:** {row['Risk Domain']}"
                        )
                        st.metric(
                            "Textual Similarity",
                            f"{row['Similarity (%)']:.2f}%"
                        )
                        st.write("**Description:**")
                        st.write(row["description"])

            st.caption(
                "Similarity scores measure textual resemblance only. "
                "They are not probabilities, proof of equivalence, or "
                "confirmation that the historical risk-domain label is correct."
            )

                        # ------------------------------------------
            # RAG-based AI incident investigation
            # ------------------------------------------

            if generate_rag_report:

                st.divider()
                st.header("🤖 AI Incident Investigation Report")

                with st.spinner(
                    "Retrieving historical evidence and generating report..."
                ):

                    # Retrieve relevant historical incidents using FAISS.
                    rag_results = retrieve_similar_incidents(
                        query=combined_text,
                        df=rag_metadata,
                        index=rag_index,
                        top_k=5
                    )

                    if rag_results.empty:

                        st.warning(
                            "No historical incidents were retrieved "
                            "for the investigation."
                        )

                    else:

                        st.subheader("RAG Historical Evidence")

                        st.dataframe(
                            rag_results[
                                [
                                    "Incident ID",
                                    "Title",
                                    "Risk Domain",
                                    "Similarity Score"
                                ]
                            ],
                            use_container_width=True,
                            hide_index=True
                        )

                        # Generate the investigation report.
                        investigation_report = generate_investigation_report(
                            incident_title=incident_title,
                            incident_description=incident_description,
                            retrieved_incidents=rag_results
                        )

                        st.subheader("Investigation Report")

                        st.markdown(investigation_report)

        except Exception as error:
            st.error(
                f"Prediction or similar-incident retrieval failed: {error}"
            )


# --------------------------------------------------
# 6. Model information
# --------------------------------------------------

with st.expander("About this model"):

    st.write(
        """
        **Model:** Logistic Regression

        **Text representation:** TF-IDF

        **Training dataset:** 1,196 labelled incidents

        **Test dataset:** 300 labelled incidents

        **Test accuracy:** 72.67%

        **Weighted F1-score:** 71.95%

        **Macro F1-score:** 54.05%

        The model predicts one of seven risk domains based on
        the text supplied. Performance varies between classes,
        particularly for classes with fewer training examples.

        The prediction should support investigation, not replace
        human review. Do not interpret it as a definitive finding
        about an incident.
        """
    )

st.caption(
    "AIID Incident Intelligence | Machine Learning Classification"
)