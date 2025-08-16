import pandas as pd
import cx_Oracle

# === File path to your cleaned dataset ===
csv_file = r"C:\Users\navne\OneDrive\Desktop\dataset\merged_crime_dataset_cleaned.csv"

# === Oracle connection details (change as needed) ===
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")  # Adjust service_name
conn = cx_Oracle.connect(user="UP_CRIME", password="UP_CRIME", dsn=dsn)
cursor = conn.cursor()

# === Load CSV ===
df = pd.read_csv(csv_file)

# === Insert Data ===
insert_sql = """
INSERT INTO crimes (
    State, District, Crime_Type, Crime_Date, Victims,
    Severity, Arrests, Reported, Risk_Score, Safe_Status
) VALUES (
    :1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5,
    :6, :7, :8, :9, :10
)
"""

# Loop through DataFrame rows and insert
for i, row in df.iterrows():
    try:
        cursor.execute(insert_sql, (
            row['State'],
            row['District'],
            row['Crime_Type'],
            str(row['Date']),        # Ensure it's a string
            int(row['Victims']),
            row['Severity'],
            int(row['Arrests']),
            int(row['Reported']),
            float(row['Risk_Score']),
            row['Safe_Status']
        ))
    except Exception as e:
        print(f"❌ Error inserting row {i}: {e}")

conn.commit()
print("✅ Data inserted successfully!")

cursor.close()
conn.close()
