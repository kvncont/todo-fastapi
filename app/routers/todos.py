import uuid

from fastapi import APIRouter

router = APIRouter()


@router.get("/todos/", tags=["todos"])
async def read_todos():
    return [
        {"id": "c303282d-f2e6-46ca-a04a-35d3d873712d", "username": "Rick", "description": "Todo#1", "isCompleted": False},
        {"id": "c5032822-f2e6-46cb-a04a-36d3dd73f134", "username": "Morty", "description": "Todo#1", "isCompleted": False},
    ]


@router.get("/todos/{username}/{id_todo}", tags=["todos"])
async def read_todo(username: str, id_todo: str):
    return {"id": id_todo, "username": username, "description": "Todo#1", "isCompleted": False}
