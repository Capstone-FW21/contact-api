from ctdb_utility_lib.utility import add_person, add_scan, connect_to_db
import fastapi
import sys
import names
import random
from fastapi import FastAPI, status
from typing import Optional, List
from sarge import capture_stdout


app = FastAPI()
connection = None
random.seed(34652346)


@app.get("/", include_in_schema=False)
def index():
    """
    Main index redirects to the Documentation.
    """
    return fastapi.responses.RedirectResponse(url="./docs")


@app.get("/student/")
def get_student():
    if connection is None:
        global connection
        connection = connect_to_db()
    email = add_person(
        names.get_first_name(), names.get_last_name(), random.randint(0, 9999999), connection
    )
    if email is None:
        raise fastapi.HTTPException(status_code=400, detail="person already exists")
    return email


@app.get("/class/")
def read_trace(building: str, room: str):
    return {"building": building, "room": room}


@app.post("/record_data/", status_code=status.HTTP_201_CREATED)
def store_data(email: str, room_id: str):
    if connection is None:
        global connection
        connection = connect_to_db()
    response = add_scan(email, room_id, connection)
    if response == -1:
        raise fastapi.HTTPException(status_code=400, detail="invalid email format")
    return "OK"


@app.get(
    "/versions",
    response_model=List[str],
    tags=["versions"],
    responses={200: {"success": status.HTTP_200_OK}},
)
def versions():
    output = None
    if sys.platform == "linux":
        output = capture_stdout("/usr/local/bin/pip list")
    else:
        output = capture_stdout("poetry show --no-dev --no-ansi")

    return output.stdout.text.splitlines()
