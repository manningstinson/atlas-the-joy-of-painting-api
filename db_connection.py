import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# Load environment variables from .env file
load_dotenv()

# Debug: Print environment variables (without exposing sensitive info)
print("Checking environment variables...")
print(f"DB_HOST is set: {'DB_HOST' in os.environ}")
print(f"DB_NAME is set: {'DB_NAME' in os.environ}")
print(f"DB_USER is set: {'DB_USER' in os.environ}")
print(f"DB_PASSWORD is set: {'DB_PASSWORD' in os.environ}")

print("Initializing database connection...")

# Create engine
engine = create_engine(
   f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:25060/{os.getenv('DB_NAME')}",
   connect_args={'sslmode': 'require'}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()

# Database dependency
def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

def create_schema():
   try:
       print("Creating database schema...")
       # Updated path to schema.sql
       schema_path = os.path.join('database', 'schema.sql')
       with open(schema_path, 'r') as file:
           schema_sql = file.read()
       
       # Execute the schema SQL using text()
       with engine.connect() as connection:
           connection.execute(text(schema_sql))
           connection.commit()
       print("✅ Database schema created successfully!")
       
   except Exception as e:
       print("❌ Failed to create database schema!")
       print(f"Error: {str(e)}")

print("✅ Database connection initialized successfully!")

if __name__ == "__main__":
   create_schema()