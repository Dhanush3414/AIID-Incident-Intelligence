# AIID Incident Intelligence

An AI-powered incident analysis platform that uses Machine Learning, similarity-based retrieval, and Retrieval-Augmented Generation (RAG) to analyze historical AI incidents and provide investigation insights.

## Overview

AIID Incident Intelligence is built using the AI Incident Database (AIID). It helps users explore historical AI incidents, identify similar cases, classify incident risk domains, and generate AI-assisted investigation recommendations.

## Key Features

- **Incident Dashboard:** Visualizes AI incident statistics and trends.
- **Incident Classification:** Predicts risk domains using a Machine Learning model.
- **Similar Incident Analysis:** Identifies related historical incidents using similarity-based retrieval.
- **AI-Assisted Investigation:** Uses RAG to retrieve relevant incident information and generate recommendations.
- **Investigation Reports:** Generates investigation reports with PDF export support.
- **Interactive Interface:** Provides a React-based frontend and FastAPI backend.

## Technology Stack

- **Programming:** Python, JavaScript
- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** FastAPI
- **Machine Learning:** Scikit-learn, TF-IDF
- **Retrieval:** FAISS
- **Data Analysis:** Pandas, NumPy, Matplotlib, Seaborn, Plotly
- **AI / RAG:** Llama
- **Other Tools:** Streamlit, Jupyter Notebook, Git, GitHub

## Dataset

- **Source:** AI Incident Database (AIID)
- **Original Dataset:** `AIID_Excel_Export-20261019.xlsx`
- **Records:** 1,749 incidents
- **Columns:** 59

## Project Structure

```text
AIID-Incident-Intelligence/
│
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── data/             # Raw and processed datasets
├── models/           # Trained ML models and retrieval artifacts
├── notebooks/        # Data analysis and ML notebooks
├── app.py            # Streamlit application
├── PROJECT_SUMMARY.md
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Dhanush3414/AIID-Incident-Intelligence.git
cd AIID-Incident-Intelligence
```

### 2. Backend Setup

```bash
python -m venv .venv
```

Activate the environment:

**Windows:**
```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

Refer to the backend and frontend configuration for the respective startup commands.

## Documentation

For the complete project explanation, including data preprocessing, transformation, analysis, machine learning methodology, model evaluation, architecture, and implementation details, refer to **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**.

## Future Enhancements

- Improve machine learning classification performance.
- Expand incident analysis and retrieval capabilities.
- Enhance AI-generated investigation recommendations.
- Improve application deployment and scalability.

## Author

**Dhanush C**

GitHub: [Dhanush3414](https://github.com/Dhanush3414)

---

*AIID Incident Intelligence – Exploring, classifying, and investigating AI incidents through Machine Learning and Generative AI.*
