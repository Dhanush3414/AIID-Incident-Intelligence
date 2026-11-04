import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load feature-engineered dataset
file_path = Path("data/processed/incidents_feature_engineered.csv")
df = pd.read_csv(file_path)

# Convert date column
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Set visualization style
sns.set_theme(style="whitegrid")

print("=" * 70)
print("AI INCIDENT INTELLIGENCE - DATA ANALYSIS")
print("=" * 70)

# --------------------------------------------------
# ANALYSIS 1: YEARLY INCIDENT TRENDS
# --------------------------------------------------

print("\n1. YEARLY INCIDENT TRENDS")

yearly_incidents = (
    df.groupby(df["date"].dt.year)
    .size()
    .reset_index(name="Incident_Count")
    .rename(columns={"date": "Year"})
)

print(yearly_incidents.to_string(index=False))

# Plot yearly incident trends
plt.figure(figsize=(12, 6))

sns.lineplot(
    data=yearly_incidents,
    x="Year",
    y="Incident_Count",
    marker="o"
)

plt.title(
    "Yearly Distribution of Recorded AI Incidents",
    fontsize=15,
    fontweight="bold"
)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number of Recorded Incidents", fontsize=12)

# Display every second year to reduce label crowding
years = yearly_incidents["Year"].tolist()
plt.xticks(years[::2], rotation=45)

plt.tight_layout()
plt.show()

# --------------------------------------------------
# ANALYSIS 2: INCIDENTS BY RISK DOMAIN
# --------------------------------------------------

print("\n2. INCIDENTS BY RISK DOMAIN")

risk_counts = (
    df["Risk Domain"]
    .dropna()
    .value_counts()
)

print(risk_counts.to_string())

plt.figure(figsize=(12, 7))

sns.countplot(
    data=df.dropna(subset=["Risk Domain"]),
    y="Risk Domain",
    order=risk_counts.index
)

plt.title(
    "Distribution of AI Incidents by Risk Domain",
    fontsize=15,
    fontweight="bold"
)
plt.xlabel("Number of Incidents")
plt.ylabel("Risk Domain")
plt.tight_layout()
plt.show()

# --------------------------------------------------
# ANALYSIS 3: TOP 10 RISK SUBDOMAINS
# --------------------------------------------------

print("\n3. TOP 10 RISK SUBDOMAINS")

subdomain_counts = (
    df["Risk Subdomain"]
    .dropna()
    .value_counts()
    .head(10)
)

print(subdomain_counts.to_string())

plt.figure(figsize=(12, 7))

sns.barplot(
    x=subdomain_counts.values,
    y=subdomain_counts.index
)

plt.title(
    "Top 10 AI Incident Risk Subdomains",
    fontsize=15,
    fontweight="bold"
)
plt.xlabel("Number of Incidents")
plt.ylabel("Risk Subdomain")
plt.tight_layout()
plt.show()

# --------------------------------------------------
# ANALYSIS 4: INCIDENTS BY MONTH
# --------------------------------------------------

print("\n4. INCIDENTS BY MONTH")

month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly_counts = (
    df["Incident_Date_Month_Name"]
    .value_counts()
    .reindex(month_order, fill_value=0)
)

print(monthly_counts.to_string())

plt.figure(figsize=(12, 6))

sns.barplot(
    x=monthly_counts.index,
    y=monthly_counts.values
)

plt.title(
    "Monthly Distribution of Recorded AI Incidents",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Number of Incidents")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --------------------------------------------------
# ANALYSIS 5: INCIDENTS BY RESPONSIBLE ENTITY
# --------------------------------------------------

print("\n5. INCIDENTS BY RESPONSIBLE ENTITY")

entity_counts = (
    df["Responsible Entity"]
    .dropna()
    .value_counts()
)

print(entity_counts.to_string())

plt.figure(figsize=(9, 6))

sns.countplot(
    data=df.dropna(subset=["Responsible Entity"]),
    x="Responsible Entity",
    order=entity_counts.index
)

plt.title(
    "Distribution of AI Incidents by Responsible Entity",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Responsible Entity")
plt.ylabel("Number of Incidents")
plt.tight_layout()
plt.show()


# --------------------------------------------------
# ANALYSIS 6: INCIDENTS BY INTENT
# --------------------------------------------------

print("\n6. INCIDENTS BY INTENT")

intent_counts = df["Intent"].dropna().value_counts()

print(intent_counts.to_string())

plt.figure(figsize=(8, 8))

plt.pie(
    intent_counts.values,
    labels=intent_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title(
    "Distribution of AI Incidents by Intent",
    fontsize=14,
    fontweight="bold"
)

plt.tight_layout()
plt.show()

# --------------------------------------------------
# ANALYSIS 7: INCIDENTS BY TIMING
# --------------------------------------------------

print("\n7. INCIDENTS BY TIMING")

timing_counts = df["Timing"].dropna().value_counts()

print(timing_counts.to_string())

plt.figure(figsize=(9, 5))

sns.countplot(
    data=df.dropna(subset=["Timing"]),
    x="Timing",
    order=timing_counts.index
)

plt.title(
    "Distribution of AI Incidents by Timing",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Incident Timing")
plt.ylabel("Number of Incidents")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

# --------------------------------------------------
# ANALYSIS 8: TOP 10 DEVELOPERS
# --------------------------------------------------

print("\n8. TOP 10 DEVELOPERS ASSOCIATED WITH INCIDENTS")

developer_counts = (
    df["developer"]
    .dropna()
    .astype(str)
    .str.strip()
)

developer_counts = developer_counts[
    developer_counts != ""
].value_counts().head(10)

print(developer_counts.to_string())

plt.figure(figsize=(11, 6))

sns.barplot(
    x=developer_counts.values,
    y=developer_counts.index
)

plt.title(
    "Top 10 Developers Associated with AI Incidents",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Number of Incidents")
plt.ylabel("Developer")
plt.tight_layout()
plt.show()

# --------------------------------------------------
# ANALYSIS 9: DISTRIBUTION OF AI HARM LEVELS
# --------------------------------------------------

print("\n9. DISTRIBUTION OF AI HARM LEVELS")

harm_counts = df["AI Harm Level"].dropna().value_counts()

print(harm_counts.to_string())

plt.figure(figsize=(10, 6))

sns.barplot(
    x=harm_counts.values,
    y=harm_counts.index
)

plt.title(
    "Distribution of Recorded AI Harm Levels",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Number of Incidents")
plt.ylabel("AI Harm Level")
plt.tight_layout()
plt.show()

# --------------------------------------------------
# ANALYSIS 10: INCIDENTS BY LOCATION REGION
# --------------------------------------------------

print("\n10. INCIDENTS BY LOCATION REGION")

region_counts = (
    df["Location Region"]
    .dropna()
    .value_counts()
)

print(region_counts.to_string())

plt.figure(figsize=(10, 6))

sns.barplot(
    x=region_counts.values,
    y=region_counts.index
)

plt.title(
    "Distribution of Recorded AI Incidents by Region",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Number of Incidents")
plt.ylabel("Location Region")
plt.tight_layout()
plt.show()