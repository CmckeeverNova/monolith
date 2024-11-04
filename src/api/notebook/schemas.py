from typing import List

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


class CreateNotebookStep(BaseModel):
    """
    Schema for notebook step creation input.
    """

    order_id: int


class NotebookStepResponse(BaseModel):
    """
    Schema for notebook step output representation.
    """

    step_id: int
    order_id: int
    notebook_id: str


class ReorderStepsRequest(BaseModel):
    """
    Schema for reordering notebook steps request.
    """

    steps: List[dict]


class ReorderStepsResponse(BaseModel):
    """
    Schema for reordering notebook steps response.
    """

    steps: List[NotebookStepResponse]
