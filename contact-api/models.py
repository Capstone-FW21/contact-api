from pydantic import BaseModel
from enum import Enum


class Student(BaseModel):
    personal_id: int
    first_name: str
    last_name: str
    email: str


class ScanType(Enum):
    PERSONAL = "PERSONAL"
    ROOM = "ROOM"


class Scan(BaseModel):
    type: ScanType
    email: str
    scanned_id: str
