from pathlib import Path
import pandas as pd

# Directory containing exported analysis results
output_dir = Path("results/analysis")

# Expected CSV files
expected_files = [
    "yearly_incident_trends.csv",
    "risk_domain_distribution.csv",
    "risk_subdomain_distribution.csv",
    "monthly_incident_distribution.csv",
    "responsible_entity_distribution.csv",
    "intent_distribution.csv",
    "timing_distribution.csv",
    "top_10_developers.csv",
    "ai_harm_level_distribution.csv",
    "location_region_distribution.csv"
]

print("=" * 70)
print("AI INCIDENT INTELLIGENCE - EXPORT VALIDATION")
print("=" * 70)

successful_files = 0

for filename in expected_files:
    file_path = output_dir / filename

    if not file_path.exists():
        print(f"[FAILED] {filename} - File not found")
        continue

    try:
        data = pd.read_csv(file_path)

        if data.empty:
            print(f"[WARNING] {filename} - File is empty")
        else:
            print(
                f"[SUCCESS] {filename} | "
                f"Rows: {len(data)} | "
                f"Columns: {len(data.columns)}"
            )
            successful_files += 1

    except Exception as error:
        print(f"[FAILED] {filename} - {error}")

print("\n" + "=" * 70)
print(
    f"VALIDATION SUMMARY: "
    f"{successful_files}/{len(expected_files)} files valid"
)
print("=" * 70)

if successful_files == len(expected_files):
    print("All analysis exports are present and readable.")
else:
    print("Please investigate the missing, empty, or unreadable files.")