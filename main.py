import pandas as pd
from sqlalchemy import create_engine

#Database URL
from database_url import SQLALCHEMY_DATABASE_URL, excel_file_path

engine = create_engine(SQLALCHEMY_DATABASE_URL)

df = pd.read_excel(excel_file_path, index_col=None)

sheet_name = pd.ExcelFile(excel_file_path).sheet_names[0]

df.to_sql(sheet_name, engine, if_exists="append", index=False)
print(f"Table '{sheet_name}' created and all rows inserted.")
