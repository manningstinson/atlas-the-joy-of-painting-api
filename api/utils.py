from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

# Create engine
engine = create_engine(
   f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:25060/{os.getenv('DB_NAME')}",
   connect_args={'sslmode': 'verify-full', 'sslrootcert': '../ca-certificate.crt'}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
   db = SessionLocal()
   try:
       return db
   finally:
       db.close()