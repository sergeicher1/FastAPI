from database import *
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse

# create table
Base.metadata.create_all(bind=engine)
app = FastAPI()


# Define the dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# define routes
@app.get("/")
def main():
    return FileResponse("public/index.html")


@app.get("/api/users")
def get_people(db: Session = Depends(get_db)):
    return db.query(Person).all()


@app.get("/api/users/{id}")
def get_person(id, db: Session = Depends(get_db)):
    # get the user by ID
    person = db.query(Person).filter(Person.id == id).first()
    # if not found
    if person == None:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    # if found
    return person


@app.post("/api/users")
def create_person(data=Body(), db: Session = Depends(get_db)):
    person = Person(name=data["name"], age=data["age"])
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@app.put("/api/users")
def edit_person(data=Body(), db: Session = Depends(get_db)):
    # Get the user by ID
    person = db.query(Person).filter(Person.id == data["id"]).first()
    # if not found
    if person == None:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    # if found, change it and send back to the client
    person.age = data["age"]
    person.name = data["name"]
    db.commit()
    db.refresh(person)
    return person


@app.delete("/api/users/{id}")
def delete_person(id, db: Session = Depends(get_db)):
    # Get the user by ID
    person = db.query(Person).filter(Person.id == id).first()
    # if not found
    if person == None:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    # if found , delete it
    db.delete(person)
    db.commit()
    return person
