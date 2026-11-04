import pandas as pd
from pathlib import Path

# Load cleaned dataset
input_path = Path("data/processed/incidents_cleaned.csv")

# Create results directory if it does not exist
output_dir = Path("results/analysis")
output_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_path)

# Convert incident date
df["date"] = pd.to_datetime(df["date"], errors="coerce")

print("=" * 70)
print("EXPORTING AI INCIDENT ANALYSIS RESULTS")
print("=" * 70)

# 1. Yearly incident trends
yearly_trends = (
    df.dropna(subset=["date"])
      .groupby(df["date"].dt.year)
      .size()
      .reset_index(name="Incident_Count")
      .rename(columns={"date": "Year"})
)

yearly_trends.columns = ["Year", "Incident_Count"]

yearly_trends.to_csv(
    output_dir / "yearly_incident_trends.csv",
    index=False
)

print("1. Yearly incident trends exported.")

# 2. Risk domain distribution
risk_domain = (
    df["Risk Domain"]
      .value_counts()
      .rename_axis("Risk_Domain")
      .reset_index(name="Incident_Count")
)

risk_domain.to_csv(
    output_dir / "risk_domain_distribution.csv",
    index=False
)

print("2. Risk domain distribution exported.")

# 3. Risk subdomain distribution
risk_subdomain = (
    df["Risk Subdomain"]
      .value_counts()
      .rename_axis("Risk_Subdomain")
      .reset_index(name="Incident_Count")
)

risk_subdomain.to_csv(
    output_dir / "risk_subdomain_distribution.csv",
    index=False
)

print("3. Risk subdomain distribution exported.")

# 4. Monthly incident distribution
month_names = {
    1: "January", 2: "February", 3: "March",
    4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September",
    10: "October", 11: "November", 12: "December"
}

monthly = (
    df.dropna(subset=["date"])
      .groupby(df["date"].dt.month)
      .size()
      .reindex(range(1, 13), fill_value=0)
      .rename_axis("Month_Number")
      .reset_index(name="Incident_Count")
)

monthly["Month"] = monthly["Month_Number"].map(month_names)

monthly = monthly[["Month_Number", "Month", "Incident_Count"]]

monthly.to_csv(
    output_dir / "monthly_incident_distribution.csv",
    index=False
)

print("4. Monthly incident distribution exported.")

# 5. Responsible entity distribution
responsible_entity = (
    df["Responsible Entity"]
      .value_counts()
      .rename_axis("Responsible_Entity")
      .reset_index(name="Incident_Count")
)

responsible_entity.to_csv(
    output_dir / "responsible_entity_distribution.csv",
    index=False
)

print("5. Responsible entity distribution exported.")

# 6. Intent distribution
intent_distribution = (
    df["Intent"]
      .value_counts()
      .rename_axis("Intent")
      .reset_index(name="Incident_Count")
)

intent_distribution.to_csv(
    output_dir / "intent_distribution.csv",
    index=False
)

print("6. Intent distribution exported.")

# 7. Timing distribution
timing_distribution = (
    df["Timing"]
      .value_counts()
      .rename_axis("Timing")
      .reset_index(name="Incident_Count")
)

timing_distribution.to_csv(
    output_dir / "timing_distribution.csv",
    index=False
)

print("7. Timing distribution exported.")

# 8. Developer distribution
developer_distribution = (
    df["developer"]
      .fillna("Unknown")
      .value_counts()
      .head(10)
      .rename_axis("Developer")
      .reset_index(name="Incident_Count")
)

developer_distribution.to_csv(
    output_dir / "top_10_developers.csv",
    index=False
)

print("8. Top 10 developers exported.")

# 9. AI harm level distribution
harm_distribution = (
    df["AI Harm Level"]
      .value_counts()
      .rename_axis("AI_Harm_Level")
      .reset_index(name="Incident_Count")
)

harm_distribution.to_csv(
    output_dir / "ai_harm_level_distribution.csv",
    index=False
)

print("9. AI harm level distribution exported.")

# 10. Location region distribution
region_distribution = (
    df["Location Region"]
      .value_counts()
      .rename_axis("Location_Region")
      .reset_index(name="Incident_Count")
)

region_distribution.to_csv(
    output_dir / "location_region_distribution.csv",
    index=False
)

print("10. Location region distribution exported.")

print("\nAll analysis result files have been exported.")
print("Output directory:", output_dir.resolve())