import pandas as pd

file_path = "file path.csv"  
df = pd.read_csv(file_path)

# ===== Clean column names (removes hidden spaces) =====
df.columns = df.columns.str.strip()

df = df[df["Risk"].notna()]

df = df[df["Risk"].str.strip().str.lower() != "none"]

# ===== Keep only real vulnerability severities =====
valid_risks = ["Critical", "High", "Medium", "Low"]
df = df[df["Risk"].isin(valid_risks)]

# ===== Select important columns =====
columns_to_keep = [
    "Host",
     "Protocol",
      "Port",
    "Name",
    "Risk",
    "Severity",
    "CVSS v3.0 Base Score"
]

existing_columns = [col for col in columns_to_keep if col in df.columns]
df_filtered = df[existing_columns]

# ===== Sort by severity order =====
severity_order = ["Critical", "High", "Medium", "Low"]
df_filtered["Risk"] = pd.Categorical(
    df_filtered["Risk"],
    categories=severity_order,
    ordered=True
)

df_filtered = df_filtered.sort_values("Risk")df_filtered.to_csv("parsed_nessus.csv", index=False)
