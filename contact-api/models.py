from pydantic import BaseModel


class Student(BaseModel):
    personal_id: int
    first_name: str
    last_name: str
    email: str


class Scan(BaseModel):
    email: str
    room_id: str
