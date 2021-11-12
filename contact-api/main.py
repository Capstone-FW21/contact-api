import fastapi
import sys
import names
from fastapi import FastAPI, status
from typing import Optional, List
from sarge import capture_stdout


app = FastAPI()

@app.get("/", include_in_schema=False)
def index():
    """
    Main index redirects to the Documentation.
    """
    return fastapi.responses.RedirectResponse(url="./docs")

@app.get("/student/")
async def get_student():
    return names.get_first_name() , names.get_last_name()

@app.get("/class/")
async def read_trace(building: str, room: str):
    return {"building": building, "room": room}

@app.post("/record_data/")
async def store_data(building: str, room: str, first: str, last: str, student_id: int): #seat data and date/time maybe?
    #write to database/invoke method to write to database
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
