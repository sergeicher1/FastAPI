import uuid
from fastapi import FastAPI, Body, status
from fastapi.responses import FileResponse, JSONResponse


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.id = str(uuid.uuid4())


# conditional database - a set of Person objects
people = [Person("Tom", 35), Person("Bob", 42), Person("Sam", 23)]


# to search for a user in the people list
def find_person(id):
    for person in people:
        if person.id == id:
            return person
    return None


app = FastAPI()


@app.get("/")
async def main():
    return FileResponse("public/index.html")


@app.get("/api/users")
def get_people():
    return people


@app.get("/api/users/{id}")
def get_person(id):
    # get the users by ID
    person = find_person(id)
    print(person)
    # if not found, send a status code and an error message
    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found"}
        )
    # if users is found, we send it
    return person


@app.post("/api/users")
def create_person(data=Body()):
    person = Person(data["name"], data["age"])
    # add the object to the people list/
    people.append(person)
    return person


@app.put("/api/users")
def edit_person(data=Body()):
    # get the user by ID
    person = find_person(data["id"])
    # if not found, status code and error
    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found"}
        )
    # if found, change data and send back to client
    person.name = data["name"]
    person.age = data["age"]
    return person


@app.delete("/api/users/{id}")
def delete_person(id):
    # get the user by ID
    person = find_person(id)
    # if not found, send status code and error
    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found"}
        )
    # if user is found, delete it
    people.remove(person)
    return person
