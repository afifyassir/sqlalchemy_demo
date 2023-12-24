from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import os

# Get the DATABASE_URL from the environment variable
DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://user:password@db:5432/fastapidb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Define the database model
class NameEntry(Base):
    __tablename__ = "names"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    random_number = Column(Integer)


# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/names/{name}")
def create_name_entry(name: str, db: SessionLocal = Depends(get_db)):
    # Check if the name already exists
    db_entry = db.query(NameEntry).filter(NameEntry.name == name).first()
    if db_entry:
        raise HTTPException(status_code=400, detail="Name already registered")

    # Assign a random integer to the name
    random_number = random.randint(1, 100)

    # Create a new database entry
    new_entry = NameEntry(name=name, random_number=random_number)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"name": name, "random_number": random_number}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
