import pandas as pd
from sqlalchemy import create_engine

#Database URL
from database_url import SQLALCHEMY_DATABASE_URL, excel_file_path

#File location
excel_file = excel_file_path


engine = create_engine(SQLALCHEMY_DATABASE_URL)

df = pd.read_excel(excel_file, index_col=None)
print(df.to_string(index=False))
