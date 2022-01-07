from ctdb_utility_lib.utility import add_room, connect_to_db
import fastapi
import sys
from fastapi import FastAPI, status
from typing import List
from sarge import capture_stdout
from enum import Enum


app = FastAPI()
connection = None


# to ensure only valid types are passed in
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
def read_trace(email: str, limit: int):  # Could add limitation
    #records = get_records(email, limit)
    # SQL: SELECT * FROM scan WHERE person_email = '{email}' ORDER BY scan_time DESC LIMIT '{limit}'
    # if records == -1:
    # raise fastapi.HTTPException(
    # status_code=400, detail="person doesn't exists")
    # return records
    return

# check the /class/ in main.py to see how to add query parameters "/breakout/?email=bob@gmail.com&data=<....>"


@app.get("/breakout/")
def read_trace(email: str, date: str):
    # contacted = breakout(email, contacted_date)
    # In breakout():
    # find the rooms of the person had been in last 7 days
    # SQL: rooms = SELCET room_id FROM scan WHERE person_email = '{email}'

    # find the time from last 7 days
    # bottom_range = contacted_date - datetime.timedelta(days=7)
    # SOL: SELECT person_email FROM scan WHERE person_email =! '{email}'
    #     AND room_id = '{rooms}'
    #     AND scan_time.date() >= bottom_range.date()

    # return contacted
    return


@app.get("/stats/")
def read_trace(type: StatTypes):
    # access database for valid stats
    # stats = databasefunction(StatTypes)

    # 'student type'
    # return a list of student, # of student, record of each student
    # list of student & record of each = SELECT person_email, count(person_email)
    #                                    FROM scan
    #                                    GROUP by person_email
    # # of student = SELECT COUNT(*) FROM people

    # 'records type'
    # return # of records
    # SQL: SELECT count(*) FROM scan

    # 'buildings type'
    # return a list of buildings, # of rooms in each building, # of records of each building, # of student visited each building
    # list of building & # of rooms:
    # SELECT building_name, count(building_name) FROM room GROUP by building_name
    #
    # # of records of each building:
    # SELECT r.building_name, count(s.room_id) FROM scan s, room r WHERE s.room_id == r.room_id GROUP by r.building_name
    #
    # # of students has visited this building:
    # SELECT r.building_name, count(DISTINCT s.person_email) FROM scan s, room r WHERE s.room_id == r.room_id GROUP by r.building_name

    # 'rooms type'
    # return a list of rooms with # of student visited, # of records in each room & the building it belongs
    # a list of rooms with # of student visited:
    # SELECT r.room_id, count(DISTINCT s.person_email) FROM scan s, room r WHERE s.room_id == r.room_id GROUP by r.room_id
    # # of record in each room:
    # SELECT r.building_name, r.room_id, count(s.room_id) FROM scan s, room r WHERE s.room_id == r.room_id GROUP by r.room_id

    # return stats
    return

@app.get("/add_room/")
def room(room_id: str, capacity: int, building_name: str):
    global connection
    if connection is None:
        connection = connect_to_db()
    response = add_room(room_id, capacity, building_name)
    if response == -1:
        raise fastapi.HTTPException(status_code=400, detail="Room Id/Building name invalid, or room already exists")
    return "Room Added"


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
