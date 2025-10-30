import pandas as pd
from sqlalchemy import create_engine, inspect
from database_url import SQLALCHEMY_DATABASE_URL, excel_file_path

engine = create_engine(SQLALCHEMY_DATABASE_URL)
inspector = inspect(engine)

xls = pd.ExcelFile(excel_file_path)

for sheet_name in xls.sheet_names:
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

    if df.empty:
        print(f"Sheet '{sheet_name}' is empty. Skipping.")
        continue

    table_exists = inspector.has_table(sheet_name)

    if not table_exists:
        df.to_sql(sheet_name, engine, if_exists="replace", index=False)
        print(f"Table '{sheet_name}' created with {len(df)} records.")
    else:
        # Read existing table data
        existing_df = pd.read_sql_table(sheet_name, engine)

        if "id" in df.columns and "id" in existing_df.columns:
            # Compare based on ID column if present
            new_df = df[~df["id"].isin(existing_df["id"])]
        else:
            # Compare based on all columns if no ID
            combined = pd.concat([df, existing_df], ignore_index=True)
            combined = combined.drop_duplicates(keep=False)
            new_df = combined[combined.index < len(df)]  # keep only new rows from df

        if not new_df.empty:
            new_df.to_sql(sheet_name, engine, if_exists="append", index=False)
            print(f"Inserted {len(new_df)} new records into '{sheet_name}'.")
        else:
            print(f"No new records to insert for '{sheet_name}'.")
