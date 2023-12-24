from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from project.main import NameEntry
import os

# Get the DATABASE_URL from the environment variable
DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://user:password@localhost:5432/fastapidb")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a new session
db = Session(bind=engine)

# Now you can use 'db' to query the database
entries = db.query(NameEntry).all()

# Print all entries
for entry in entries:
    print(f"Name: {entry.name}, Random Number: {entry.random_number}")
