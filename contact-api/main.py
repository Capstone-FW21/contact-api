import fastapi
import sys
import names
import random
import time
import psycopg2

from fastapi import FastAPI, status, Body, HTTPException
from typing import Optional, List
from sarge import capture_stdout
from ctdb_utility_lib.utility import (
    add_person,
    add_scan,
    add_personal_scan,
    connect_to_db,
    valid_email_format,
    exists_in_people,
    exists_in_rooms,
    get_room_aspect_ratio,
)
from .models import Scan, Student, ScanType

app = FastAPI()
connection = None
random.seed(time.time() * 1000)


@app.get("/", include_in_schema=False)
def index():
    """
    Main index redirects to the Documentation.
    """
    return fastapi.responses.RedirectResponse(url="./docs")


# Check if email is valid
@app.get("/email")
def email(email: str):
    global connection
    if connection is None:
        connection = connect_to_db()

    valid_email = valid_email_format(email)
    if valid_email:
        email_exist = exists_in_people(email, connection)
        if email_exist:
            return email  # for now, return email
        else:
            raise fastapi.HTTPException(status_code=400, detail="Email doesn't exist")
    else:
        raise fastapi.HTTPException(status_code=400, detail="Invalid email format")


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
        raise HTTPException(status_code=400, detail="person already exists")

    return Student(
        **{"personal_id": personal_id, "first_name": fname, "last_name": lname, "email": email}
    )


@app.post("/record_data", status_code=status.HTTP_201_CREATED)
def record_data(xcoord: float = -1, ycoord: float = -1, scan: Scan = Body(..., embed=True)):
    global connection
    if connection is None:
        connection = connect_to_db()

    scan.email = scan.email.strip()
    scan.scanned_id = scan.scanned_id.strip()
    response = -1
    try:
        if scan.type == ScanType.PERSONAL:
            response = add_personal_scan(scan.email, scan.scanned_id, connection)
        else:
            if xcoord == -1 or ycoord == -1:
                raise HTTPException(status_code=400, detail="No X/Y Coordinate found!")
            response = add_scan(scan.email, scan.scanned_id, xcoord, ycoord, connection)
    except psycopg2.Error as err:
        connection.rollback()
        raise HTTPException(status_code=400, detail=err.pgerror)
    if response == -1:
        raise HTTPException(status_code=400, detail="invalid email format or position")
    return "OK"


@app.get("/room")
def get_room_ratio(room_id: str):
    global connection
    if connection is None:
        connection = connect_to_db()

    exists = exists_in_rooms(room_id, connection)

    if exists:
        ratio = get_room_aspect_ratio(room_id, connection)
        return {"valid": exists, "aspect_ratio": ratio}
    else:
        return {"valid": exists}


# @app.post("/personal_QR_Scan", status_code=status.HTTP_201_CREATED)
# def personal_QR_Scan(scan: Personal_QR_Scan = Body(..., embed=True)):
#     global connection
#     if connection is None:
#         connection = connect_to_db()
#     try:
#         response = add_scan(scan.scanner_email, scan.id_email, connection)
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
