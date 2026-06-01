from sqlalchemy import create_engine

DB_USER = "abhijeet"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "economic_earthquake"

DATABASE_URL = (f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = create_engine(DATABASE_URL)
print("Database connection initialized.")