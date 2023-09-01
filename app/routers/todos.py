""" Route definitions for ToDos"""

from typing import Any, List

from fastapi import APIRouter, Request, Response
from fastapi.encoders import jsonable_encoder

from app.models.todos import ToDoItem

router = APIRouter()


@router.post("", response_model=ToDoItem, description="Create a ToDo")
async def create_todo(request: Request, todo_item: ToDoItem) -> Any:
    """
    Create a ToDo

    Parameters:
    - **todo_item**: ToDoItem

    Returns:
    - **200**: ToDoItem
    """
    todo_item = jsonable_encoder(todo_item)
    new_item = await request.app.state.container.create_item(todo_item)
    return new_item


@router.get(
    "/{username}", response_model=List[ToDoItem], description="Get ToDos by user"
)
async def read_todos(request: Request, username: str) -> Any:
    """
    Get ToDos by user

    Parameters:
    - **username**: str

    Returns:
    - **200**: List[ToDoItem]
    """

    query = "SELECT * FROM c WHERE c.username = @username"
    params = [dict(name="@username", value=username)]

    todos = [
        todo
        async for todo in request.app.state.container.query_items(
            query=query, parameters=params
        )
    ]

    if todos:
        return todos

    return Response(status_code=404)


@router.get(
    "/{username}/{id_todo}",
    response_model=ToDoItem,
    description="Get ToDos by user and id",
)
async def read_todo(request: Request, username: str, id_todo: str) -> Any:
    """
    Get ToDos by user and id

    Parameters:
    - **username**: str
    - **id_todo**: str

    Returns:
    - **200**: ToDoItem
    """

    query = "SELECT * FROM c WHERE c.username = @username and c.id = @id"
    params = [dict(name="@username", value=username), dict(name="@id", value=id_todo)]

    todos = [
        todo
        async for todo in request.app.state.container.query_items(
            query=query, parameters=params
        )
    ]

    if todos:
        return todos[0]

    return Response(status_code=404)


@router.put("", response_model=ToDoItem, description="Update a ToDo")
async def update_todo(request: Request, todo_item: ToDoItem) -> Any:
    """
    Update a ToDo

    Parameters:
    - **todo_item**: ToDoItem

    Returns:
    - **200**: ToDoItem
    """

    todo_item = jsonable_encoder(todo_item)

    username = todo_item["username"]
    id_todo = todo_item["id"]

    query = "SELECT * FROM c WHERE c.username = @username and c.id = @id"
    params = [dict(name="@username", value=username), dict(name="@id", value=id_todo)]

    todos = [
        todo
        async for todo in request.app.state.container.query_items(
            query=query, parameters=params
        )
    ]

    if todos:
        new_item = await request.app.state.container.replace_item(
            todo_item["id"], todo_item
        )

        if new_item:
            return new_item

    return Response(status_code=404)


@router.delete("/{id_todo}", description="Delete ToDo by id")
async def delete_todo(request: Request, id_todo: str) -> Any:
    """
    Delete a ToDo

    Parameters:
    - **todo_id**: str

    Returns:
    - **204**: No Content
    """

    query = "SELECT * FROM c WHERE c.id = @id"
    params = [dict(name="@id", value=id_todo)]

    todos = [
        todo
        async for todo in request.app.state.container.query_items(
            query=query, parameters=params
        )
    ]

    if todos:
        await request.app.state.container.delete_item(
            id_todo, partition_key=id_todo
        )
        return Response(status_code=204)

    return Response(status_code=404)
