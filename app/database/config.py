import os

import databases
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# load environment variables
load_dotenv()

# Get the database URL based on the environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    if os.environ.get("ENV") == "production":
        # database credentials should be stored in .env file
        # local with postgresql, for production; DATABASE_URL passed as ENV VAR
        DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"
    # For development and testing, using SQLite in-memory databases
    elif os.environ.get("ENV") == "test":
        DATABASE_URL = "sqlite:///./test.db"  # Change the path and name as needed
    else:
        DATABASE_URL = "sqlite:///./dev.db"  # Change the path and name as needed
# Create a Database instance
database = databases.Database(DATABASE_URL)

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a base class for declarative models
Base = declarative_base()


def initialize_database():
    """
    Initialize the database by creating all tables.
    """
    Base.metadata.create_all(bind=engine)


# def get_db():
#     """
#     Get a new database session.
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
def get_db():
    session = scoped_session(sessionmaker(bind=engine))
    try:
        yield session
    finally:
        session.remove()
