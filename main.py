import pandas as pd
from sqlalchemy import create_engine, inspect
from database_url import SQLALCHEMY_DATABASE_URL, excel_file_path

# Connect to PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
inspector = inspect(engine)

# Load Excel file
xls = pd.ExcelFile(excel_file_path)

# Loop through every sheet in the Excel file
for sheet_name in xls.sheet_names:
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, index_col=None)

    # Skip empty sheets
    if df.empty:
        print(f"Sheet '{sheet_name}' is empty. Skipping.")
        continue

    # Check if table already exists
    table_exists = inspector.has_table(sheet_name)

    if not table_exists:
        # Create table and insert all rows
        df.to_sql(sheet_name, engine, if_exists="replace", index=False)
        print(f"Table '{sheet_name}' created with {len(df)} records.")
    else:
        # Try to read existing IDs to detect duplicates
        try:
            existing_ids = pd.read_sql(f"SELECT id FROM {sheet_name}", engine)["id"]
            new_df = df[~df["id"].isin(existing_ids)]
        except Exception as e:
            print(f"An Error occurred: {e}")
            print(f"Table '{sheet_name}' has no 'id' column. Appending all rows.")
            new_df = df

        # Append only new rows
        if not new_df.empty:
            new_df.to_sql(sheet_name, engine, if_exists="append", index=False)
            print(f"Inserted {len(new_df)} new records into '{sheet_name}'.")
        else:
            print(f"No new records to insert for '{sheet_name}'.")
