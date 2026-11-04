AI Incident Intelligence

1. Project Overview

AI Incident Intelligence is a data analysis project that explores incidents involving artificial intelligence systems using data from the AI Incident Database (AIID).

The project focuses on understanding AI-related risks, identifying trends in reported incidents, analyzing risk categories, and examining the entities and circumstances associated with AI incidents.

The current implementation covers dataset inspection, data cleaning, transformation, feature engineering, exploratory data analysis, validation, and exporting analysis results.

2. Dataset Description

Dataset: AI Incident Database (AIID) Excel Export
Source file: AIID_Excel_Export-20261019.xlsx
Main sheet: Incidents
Original dataset size: 1,749 rows and 59 columns

The dataset includes information such as:

Incident ID, date, year, title, and description

Developer and deployer information

Risk domains and risk subdomains

Responsible entities and intent

Timing of incidents

AI technology and technical failure classifications

Harm classifications and reported injuries or fatalities

Deployment sectors and geographical information

Number of associated reports

The original Excel workbook also contains Reports, Entities, Data Dictionary, and Coverage Map sheets.

3. Data Cleaning

The initial data-cleaning process was implemented in:

notebooks/04_data_cleaning.py

The following operations were performed:

Loaded the Incidents worksheet from the original Excel workbook.

Removed completely empty rows and columns.

Cleaned column names by removing unnecessary surrounding whitespace.

Checked for duplicate incident IDs.

Converted the incident date column to a datetime format.

Validated essential columns, including Incident ID, date, year, title, and description.

Inspected missing values in important taxonomy and classification columns.

Exported the cleaned dataset to CSV format.

Cleaning Results

Original dataset: 1,749 rows and 59 columns.

Cleaned dataset: 1,749 rows and 59 columns.

Duplicate incident IDs: 0.

Missing values in essential fields: 0.

Missing values in classification fields were retained for further analysis rather than arbitrarily imputed.

Output file: data/processed/incidents_cleaned.csv

4. Data Transformation

Data transformation was implemented through the project scripts in the notebooks directory.

Date Transformation

The incident date was converted into a datetime representation.

The following features were created:

Incident_Date_Year

Incident_Date_Month

Incident_Date_Month_Name

Incident_Date_Quarter

Incident_Date_Day

Incident_Date_Day_Name

These features support time-based analysis of reported AI incidents.

Categorical and List-Like Data Transformation

List-like fields were inspected and safely parsed using Python's ast.literal_eval where appropriate.

Parsed fields include:

Sector of Deployment

Infrastructure Sectors

AI Goal

AI Technology

AI Technology (Potential)

Technical Failure

Technical Failure (Potential)

AI Task

AI Methods

Data Inputs

New columns with the _List suffix were created for the applicable fields.

The transformed dataset was saved to:

data/processed/incidents_transformed.csv

5. Feature Engineering

Feature engineering was implemented in:

notebooks/08_feature_engineering.py

The following features were created:

Feature

Purpose

Has_Reports

Indicates whether an incident has associated reports.

Has_Developer

Indicates whether developer information is available.

Has_Deployer

Indicates whether deployer information is available.

Has_Harm_Information

Indicates whether the incident contains information in the selected harm-related fields.

Incident_Age_Group

Groups incidents into historical periods.

The incident age groups are:

Before 2011

2011–2015

2016–2020

2021–2023

2024 onwards

The feature-engineered dataset contains 1,749 rows and 81 columns.

Output file: data/processed/incidents_feature_engineered.csv

6. Exploratory Data Analysis

Exploratory data analysis was implemented in:

notebooks/10_data_analysis.py

The analysis examined incident trends, risk classifications, intent, timing, responsible entities, developers, harm levels, and geographical distributions.

Visualizations and Analyses

The following analyses were performed:

Yearly incident trends

Risk domain distribution

Top 10 risk subdomains

Monthly incident distribution

Responsible entity distribution

Intent distribution

Incident timing distribution

Top 10 developers

AI harm level distribution

Location region distribution

These analyses help identify patterns in the available incident records and provide an overview of the types of risks documented in the database.

7. Validation and Exported Results

Data Validation

The project includes validation scripts to check the integrity of the cleaned and transformed datasets.

Validation checks include:

Duplicate rows and incident IDs

Missing values in essential columns

Date and year consistency

Presence of newly engineered features

Missing and invalid report counts

Consistency of analysis results

The analysis validation script independently verified the principal incident counts and distributions.

Exported Analysis Results

The analysis results were exported using:

notebooks/12_export_analysis_results.py

The exported files were then checked using:

notebooks/13_verify_analysis_exports.py

All 10 out of 10 analysis CSV files were successfully verified as present and readable.

The exported files are stored in results/analysis/.

File

Contents

yearly_incident_trends.csv

Incident counts by year

risk_domain_distribution.csv

Incident counts by risk domain

risk_subdomain_distribution.csv

Incident counts by risk subdomain

monthly_incident_distribution.csv

Incident counts by calendar month

responsible_entity_distribution.csv

Distribution of responsible entities

intent_distribution.csv

Distribution of incident intent

timing_distribution.csv

Distribution of incident timing

top_10_developers.csv

Ten most frequent developer entries

ai_harm_level_distribution.csv

Distribution of recorded AI harm levels

location_region_distribution.csv

Distribution of recorded geographical regions

8. Key Findings

The analysis of the 1,749 incident records identified the following patterns:

Recorded incident trends: The database contains 460 incidents dated 2025, the highest annual count in the dataset. The 2026 count is 267 through October 7, 2026, so it represents a partial year.

Risk domains: Malicious Actors & Misuse is the most frequent classified risk domain, with 566 records.

Risk subdomains: Fraud, scams, and targeted manipulation is the most frequent recorded risk subdomain, with 412 records.

Responsible entities: AI is recorded as the responsible entity in 960 incidents, while Human is recorded in 525.

Intent: The dataset contains 740 incidents classified as unintentional and 735 classified as intentional.

Timing: Post-deployment incidents account for 1,460 records.

Missing classifications: Risk Domain is missing in 253 records, while AI Harm Level and Location Region are each missing in 1,549 records.

Interpretation and Limitations

These findings describe incidents recorded in the AI Incident Database; they do not represent the true worldwide frequency of AI incidents.

The number of recorded incidents may be influenced by reporting practices, database coverage, and the availability of classification information. In particular, harm-level and geographical analyses cover only the subset with available classifications.

The yearly counts for 2026 are incomplete and should not be directly compared with full-year counts without accounting for the partial reporting period.

9. Tools and Technologies Used

Programming language: Python

Data manipulation: Pandas, NumPy

Data visualization: Matplotlib, Seaborn

Excel processing: OpenPyXL

Data formats: Excel and CSV

Development environment: Visual Studio Code

Environment management: Python virtual environment (.venv)

10. Current Project Status

The following stages have been completed:

Dataset inspection and quality assessment

Data cleaning

Date and categorical data transformation

Feature engineering

Exploratory data analysis and visualization

Data and analysis validation

Exporting and verifying analysis results

The current version establishes a validated data-analysis foundation for the project.

Advanced capabilities, such as machine-learning-based anomaly detection, incident classification, retrieval-augmented generation (RAG), and AI-assisted incident investigation, are not yet documented as completed and can be developed as future project stages.