import fastapi
import sys
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


@app.get("/demo_get/{demo_arg}/")
def demo_get(demo_arg: str):
    """
    Place holder GET request method stub.
    """
    return demo_arg


@app.post("/demo_post/{demo_arg}/")
def demo_post(demo_arg: str):
    """
    Place holder PUT request method stub.
    """
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
