# AIID Incident Intelligence
### AI-Powered Incident Analysis, Risk Classification & Investigation Platform

---

## 1. Project Overview

**AIID Incident Intelligence** is an AI-powered incident analysis and investigation platform developed using the AI Incident Database (AIID).

The platform combines Machine Learning, Natural Language Processing (NLP), similarity analysis, and Retrieval-Augmented Generation (RAG) to analyze historical AI incidents, classify potential risk domains, identify similar incidents, and generate investigation reports.

It provides an interactive interface for exploring AI incidents, understanding risk patterns, and supporting structured incident investigation through historical evidence and AI-generated recommendations.

## 2. Problem Statement

The increasing adoption of Artificial Intelligence across industries has introduced various risks, including misinformation, privacy violations, discrimination, security vulnerabilities, and system failures.

Analyzing these incidents manually can be time-consuming and makes it difficult to identify recurring patterns and relationships between incidents.

This project addresses these challenges by developing an intelligent platform that:

- Analyzes historical AI incident records.
- Identifies and classifies incident risk domains.
- Finds similar historical incidents.
- Retrieves relevant incident information.
- Generates structured investigation reports using RAG.
- Presents insights through an interactive dashboard.

## 3. Project Objectives

- Perform comprehensive Exploratory Data Analysis (EDA) on AIID records.
- Clean and preprocess incident data.
- Transform categorical variables and engineer relevant features.
- Develop a Machine Learning model for risk domain classification.
- Implement similarity-based incident retrieval.
- Integrate FAISS-based retrieval with a Llama-powered RAG pipeline.
- Develop an interactive frontend and backend architecture.
- Generate investigation reports using historical incident evidence.

## 4. Dataset Description

**Dataset:** AI Incident Database (AIID)

**Original file:** `AIID_Excel_Export-20261019.xlsx`

| Dataset Information | Details |
|---|---|
| Total records | 1,749 |
| Original columns | 59 |
| Data source | AI Incident Database |
| Duplicate Incident IDs | 0 |
| Essential fields | Incident ID, Date, Year, Title, Description |

The dataset contains historical AI incident information, including incident descriptions, risk domains, subdomains, responsible entities, deployment sectors, and other incident-related attributes.

Some taxonomy and descriptive fields contain missing values, which were examined during the data cleaning and validation stages.

## 5. Data Processing Workflow

The project follows a structured data processing pipeline.

### 5.1 Data Inspection and EDA

- Inspected dataset dimensions, column names, and data types.
- Examined missing values and duplicate records.
- Analyzed categorical and numerical attributes.
- Examined relationships between incident attributes.
- Validated dataset structure and taxonomy fields.

### 5.2 Data Cleaning

- Checked and validated Incident IDs.
- Removed duplicate records where applicable.
- Converted date fields into appropriate formats.
- Validated essential columns.
- Examined missing values in risk taxonomy fields.
- Preserved useful incident records rather than unnecessarily removing incomplete rows.

### 5.3 Data Transformation

- Converted categorical variables into suitable representations.
- Analyzed risk domain and risk subdomain distributions.
- Performed feature engineering.
- Prepared structured datasets for classification and analysis.
- Validated the transformed datasets.

### 5.4 Data Analysis

Performed analysis of:

- Risk domain distribution.
- Risk subdomain distribution.
- AI harm level distribution.
- Incident trends over time.
- Geographic distribution of incidents.
- Responsible entities.
- Incident intent and timing.

Generated analysis results and visualizations using Python data analysis libraries.

## 6. Machine Learning – Risk Domain Classification

A supervised Machine Learning pipeline was developed to classify AI incidents into risk domains.

### Workflow

1. Prepared the classification dataset.
2. Identified the target variable.
3. Performed training and testing data splitting.
4. Applied TF-IDF vectorization to incident text.
5. Trained a classification model.
6. Evaluated model performance.
7. Saved the trained classifier and vectorizer.
8. Integrated the trained model into the application.

### Model Performance

| Metric | Result |
|---|---:|
| Model Accuracy | 72.67% |
| Classification Coverage | 85.53% |
| Classified Incidents | 1,496 |
| Total Incidents | 1,749 |
| Risk Domains | 7 |

The evaluation also includes classification reports, confusion matrices, and class-wise performance visualizations.

**Note:** Classification coverage and model accuracy represent different measurements. Coverage indicates the proportion of incidents classified, while accuracy measures predictive correctness on the evaluated test data.

## 7. Similarity-Based Incident Analysis

The platform includes a similarity analysis component to identify historical incidents that are relevant to a given incident description.

### Workflow

- Loads historical incident records.
- Converts incident descriptions into numerical text representations.
- Builds a similarity index.
- Compares the submitted incident with historical incidents.
- Retrieves the most similar incident records.
- Displays relevant historical information for further investigation.

This functionality helps investigators understand recurring incident patterns and identify related historical cases.

## 8. Retrieval-Augmented Generation (RAG)

The project integrates a RAG pipeline to support evidence-based incident investigation.

### RAG Workflow

1. Accepts incident information for investigation.
2. Converts the incident query into a retrieval representation.
3. Searches the FAISS vector index.
4. Retrieves relevant historical incident information.
5. Supplies retrieved context to the Llama-based generation component.
6. Generates a structured investigation report.

### Key Components

- **FAISS:** Efficient similarity-based vector retrieval.
- **Llama:** Language model used for report generation.
- **Incident Metadata:** Stores supporting historical incident information.
- **RAG Pipeline:** Connects retrieval and generation components.

The purpose of RAG is to provide investigation recommendations using retrieved historical incident context rather than relying only on a language model's general knowledge.

## 9. Application Architecture

The project includes a React frontend and FastAPI backend, along with a Streamlit application.

### Frontend – React + Vite

The frontend provides an interactive interface with the following modules:

- **Dashboard:** Displays incident statistics and key performance indicators.
- **Historical Incidents:** Allows users to explore, search, and filter historical incidents.
- **Similarity Analysis:** Identifies similar historical incidents.
- **Investigation:** Supports AI incident investigation.
- **Investigation Reports:** Displays saved investigation reports and supports PDF export.
- **About:** Provides project information.

### Backend – FastAPI

The backend provides API endpoints for:

- Dashboard statistics.
- Historical incident retrieval.
- Incident search and filtering.
- Incident investigation.
- Similarity analysis.
- RAG report generation.
- Investigation report history.

### Streamlit Application

The root-level `app.py` provides an additional Streamlit-based interface for incident exploration, risk classification, and analysis.

## 10. Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python, JavaScript |
| Data Processing | Pandas, NumPy |
| Data Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn |
| NLP | TF-IDF |
| Classification | Supervised Machine Learning |
| Similarity Search | Text Vectorization, Similarity Analysis |
| Vector Database / Retrieval | FAISS |
| Generative AI | Llama |
| RAG | Retrieval-Augmented Generation |
| Frontend | React, Vite, Tailwind CSS |
| Backend | FastAPI |
| Additional UI | Streamlit |
| PDF Generation | jsPDF |
| Development Tools | VS Code, Jupyter Notebook, Git, GitHub |

## 11. Project Directory Structure

```text
AIID-Incident-Intelligence/
│
├── backend/
│   └── main.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
│
├── models/
│   ├── classification/
│   ├── rag/
│   └── tfidf/
│
├── notebooks/
│
├── rag/
│   └── rag_pipeline.py
│
├── results/
│   ├── analysis/
│   └── figures/
│
├── app.py
├── similar_incidents.py
├── PROJECT_SUMMARY.md
└── .gitignore
```

## 12. Key Features

- AI incident dataset exploration and analysis.
- Interactive incident dashboard.
- Machine Learning-based risk domain classification.
- Historical incident search and filtering.
- Similarity-based incident identification.
- FAISS-powered historical incident retrieval.
- Llama-based RAG investigation reports.
- Investigation report history.
- PDF report export.
- Separate React frontend and FastAPI backend.
- Streamlit-based application interface.

## 13. Project Outcomes

The project demonstrates the integration of multiple AI technologies into a unified incident intelligence platform.

Key outcomes include:

- Processed and analyzed 1,749 AI incident records.
- Developed a seven-domain risk classification pipeline.
- Achieved 72.67% reported model accuracy.
- Implemented similarity-based historical incident retrieval.
- Integrated FAISS and Llama into a RAG investigation workflow.
- Developed interactive application interfaces.
- Implemented investigation report storage and PDF export.

## 14. Future Enhancements

- Improve classification performance through advanced NLP models and hyperparameter optimization.
- Integrate additional AI incident datasets.
- Improve retrieval relevance and evaluation.
- Introduce explainable AI for classification decisions.
- Add real-time AI incident monitoring.
- Implement user authentication and role-based access.
- Deploy the platform to a cloud environment.
- Introduce automated risk alerts and incident trend monitoring.

## 15. Conclusion

AIID Incident Intelligence demonstrates how Machine Learning, NLP, similarity search, and Generative AI can be integrated to support AI incident analysis and investigation.

By combining historical incident exploration, automated risk classification, similarity-based retrieval, and RAG-generated investigation reports, the platform provides a structured approach to understanding AI-related risks.

The project highlights the practical application of AI technologies in improving incident intelligence, supporting evidence-based investigations, and promoting responsible AI development and deployment.

---

**Project:** AIID Incident Intelligence  
**Domain:** Artificial Intelligence | Machine Learning | NLP | Generative AI  
**Repository:** https://github.com/Dhanush3414/AIID-Incident-Intelligence
