import fastapi
import sys
from fastapi import FastAPI, status
from typing import List
from sarge import capture_stdout
from enum import Enum


app = FastAPI()

#to ensure only valid types are passed in
class StatTypes(str, Enum):
    students = "students"
    records = "records"
    buildings = "buildings"
    rooms = "rooms"



@app.get("/", include_in_schema=False)
def index():
    """
    Main index redirects to the Documentation.
    """
    return fastapi.responses.RedirectResponse(url="./docs")


@app.get("/records/")
def read_trace():
    return

#check the /class/ in main.py to see how to add query parameters "/breakout/?email=bob@gmail.com&data=<....>"
@app.get("/breakout/")
def read_trace():
    return


@app.get("/stats/")
def read_trace(type: StatTypes):
    #access database for valid stats
    #stats = databasefunction(StatTypes)
    #return stats
    return


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