"""This class represent the ToDoItem model"""

from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ToDoItem(BaseModel):
    """Class representing a ToDo item"""
    id: UUID = Field(default_factory=uuid4)
    username : str
    description : str
    is_complete : bool = Field(alias="isComplete", default=False)
