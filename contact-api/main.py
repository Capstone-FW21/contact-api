import fastapi
import sys
import names
import random
import time
import psycopg2

from fastapi import FastAPI, status, Body
from typing import Optional, List
from sarge import capture_stdout
from ctdb_utility_lib.utility import add_person, add_scan, connect_to_db, validate_email_format, exists_in_people
from .models import Scan, Student, Personal_QR_Scan

app = FastAPI()
connection = None
random.seed(time.time() * 1000)


@app.get("/", include_in_schema=False)
def index():
    """
    Main index redirects to the Documentation.
    """
    return fastapi.responses.RedirectResponse(url="./docs")


#Check if email is valid
@app.get("/email/")
def email(email:str):
    global connection
    if connection is None:
        connection = connect_to_db()
    
    valid_email = validate_email_format(email)
    if valid_email:
        email_exist = exists_in_people(email, connection)
        if email_exist:
            return email #for now, return email
        else:
            raise fastapi.HTTPException(
            status_code=400, detail="Email doesn't exist")
    else:
        raise fastapi.HTTPException(
            status_code=400, detail="Invalid email format")


@app.get("/student", response_model=Student)
def get_student() -> Student:
    global connection
    names.random.seed(time.time() * 1000)

    if connection is None:
        connection = connect_to_db()
    fname = names.get_first_name()
    lname = names.get_last_name()
    personal_id = random.randint(0, 9999999)
    email = add_person(fname, lname, personal_id, connection)
    if email is None:
        raise fastapi.HTTPException(status_code=400, detail="person already exists")

    return Student(**{"personal_id": personal_id, "first_name": fname, "last_name": lname, "email": email})


@app.post("/record_data", status_code=status.HTTP_201_CREATED)
def record_data(scan: Scan = Body(..., embed=True)):
    global connection
    if connection is None:
        connection = connect_to_db()
    try:
        response = add_scan(scan.email, scan.room_id, connection)
    except psycopg2.Error as err:
        connection.rollback()
        raise fastapi.HTTPException(status_code=400, detail=err.pgerror)
    if response == -1:
        raise fastapi.HTTPException(status_code=400, detail="invalid email format")
    return "OK"


# @app.post("/personal_QR_Scan", status_code=status.HTTP_201_CREATED)
# def personal_QR_Scan(scan: Personal_QR_Scan = Body(..., embed=True)):
#     global connection
#     if connection is None:
#         connection = connect_to_db()
#     try:
#         response = add_scan(scan.email, scan.personal_id, connection)
#     except psycopg2.Error as err:
#         connection.rollback()
#         raise fastapi.HTTPException(status_code=400, detail=err.pgerror)
#     if response == -1:
#         raise fastapi.HTTPException(status_code=400, detail="invalid email format")
#     return "OK"


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
