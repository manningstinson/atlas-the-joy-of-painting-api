import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.pool import QueuePool

# Load environment variables from .env file
load_dotenv()

print("Initializing database connection...")

# Build connection string with explicit SSL requirements
DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:25060/{os.getenv('DB_NAME')}"
)

# Create engine with more robust settings
engine = create_engine(
    DATABASE_URL,
    connect_args={
        'sslmode': 'require',
        'connect_timeout': 60,  # Increase connection timeout
    },
    pool_size=5,  # Set connection pool size
    max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
    poolclass=QueuePool,  # Use queue pooling for better connection management
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Prevent expired object issues
)

# Create declarative base for models
Base = declarative_base()

# Database dependency with better error handling
def get_db():
    db = SessionLocal()
    try:
        # Test the connection
        db.execute(text('SELECT 1'))
        yield db
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        db.rollback()  # Rollback any failed transactions
        raise
    finally:
        db.close()

# Remove the create_schema function since your schema is already created
# and keeping it might cause accidental schema recreation

print("✅ Database connection initialized successfully!")

if __name__ == "__main__":
    # Test the connection
    with SessionLocal() as session:
        result = session.execute(text('SELECT 1'))
        print("Database connection test successful!")