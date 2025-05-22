# # utils/sql_executor.py
# import pyodbc
# import pandas as pd

# def execute_query(query):
#     conn = pyodbc.connect(
#         "Driver={ODBC Driver 17 for SQL Server};"
#         "Server=senvangsolutions.com,1445;"
#         "Database=CRM_THIENNAM;"
#         "UID=dev2;"               # Tên đăng nhập SQL Server
#         "PWD=dev2;"     
#         "TrustServerCertificate=yes;"
#     )
#     df = pd.read_sql(query, conn)
#     conn.close()
#     return df.to_markdown(index=False)
# //////////////////////////////////////////////////
# from sqlalchemy import create_engine
# import pandas as pd

# def execute_query(query):
#     engine = create_engine(
#         "mssql+pyodbc://dev2:dev2@senvangsolutions.com:1445/CRM_THIENNAM?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
#     )
#     with engine.connect() as conn:
#         df = pd.read_sql(query, conn)
#     # return df.to_markdown(index=False)
#     return df.to_dict(orient="records") 
# //////////////////////////////////////////////////////
from sqlalchemy import create_engine, text
import pandas as pd

def execute_query(query):
    engine = create_engine(
        "mssql+pyodbc://dev2:dev2@senvangsolutions.com:1445/CRM_THIENNAM?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    )
    
    with engine.begin() as conn:  # begin() sẽ tự commit nếu không lỗi
        lower_query = query.strip().lower()
        
        if lower_query.startswith("select"):
            df = pd.read_sql(query, conn)
            return df.to_dict(orient="records")
        else:
            conn.execute(text(query))  # Dùng text() cho độ an toàn
            return {"message": "✅ Query executed successfully"}
