from pydantic import BaseModel


class CreateNotebook(BaseModel):
    """
    Schema for notebook creation input.
    """
    name: str


class NotebookResponse(BaseModel):
    """
    Schema for notebook output representation.
    """
    id: str
    name: str
