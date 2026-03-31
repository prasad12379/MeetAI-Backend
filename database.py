from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 🔥 Important for Render PostgreSQL
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}  # 🔥 must
)

# ✅ THIS LINE IS MOST IMPORTANT
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()