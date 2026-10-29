from fastapi import FastAPI
from sqlalchemy import text
from .database import engine


app = FastAPI()

@app.get("/")
def home():
  return{"message": "FastAPI is running"}


@app.get("/todos")
def get_todos():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM public.todos ORDER BY id")
        )

        todos = [dict(row) for row in result.mappings()]

    return todos