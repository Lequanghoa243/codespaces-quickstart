from langchain_community.utilities import SQLDatabase
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    engine_args = {
    "pool_recycle": 3600,
    "pool_pre_ping": True  
    }

    db_uri = (
    f"mysql+pymysql://{os.getenv('db_user')}:{os.getenv('db_password')}"
    f"@{os.getenv('db_host')}:{os.getenv('db_port')}/{os.getenv('db_name')}"
    )

    return SQLDatabase.from_uri(
        db_uri, engine_args=engine_args, sample_rows_in_table_info=1
        )

db = get_db_connection()