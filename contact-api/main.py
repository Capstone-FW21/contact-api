import fastapi
from fastapi import FastAPI
from typing import Optional


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


@app.put("/demo_put/{demo_arg}/")
def demo_put(demo_arg: str):
    """
    Place holder PUT request method stub.
    """
    return "OK"