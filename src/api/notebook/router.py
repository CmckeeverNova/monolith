import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.api.notebook.models import NotebookStep
from src.api.notebook.schemas import (
    CreateNotebook,
    CreateNotebookStep,
    NotebookResponse,
    NotebookStepResponse,
    ReorderStepsRequest,
    ReorderStepsResponse,
)
from src.api.notebook.service import NotebookService

router = APIRouter()


@router.get("/", response_model=list[NotebookResponse])
def get_notebooks(notebook_service: NotebookService = Depends()):
    """
    Retrieve a list of all notebooks.

    Args:
        notebook_service (NotebookService): The service handling notebook operations.

    Returns:
        A list of all notebooks.
    """
    notebooks = notebook_service.get_notebooks()
    return [NotebookResponse(**notebook.model_dump()) for notebook in notebooks]


@router.post("/", response_model=NotebookResponse, status_code=201)
def create_notebook(
    input: CreateNotebook, notebook_service: NotebookService = Depends()
):
    """
    Create a new notebook with the specified name.

    Args:
        input (CreateNotebook): The input data containing the notebook name.
        notebook_service (NotebookService): The service handling notebook creation.

    Returns:
        The newly created notebook.
    """
    notebook = notebook_service.create_notebook(input.name)
    return NotebookResponse(**notebook.model_dump())


@router.get("/{notebook_id}", response_model=NotebookResponse)
def get_notebook(notebook_id: str, notebook_service: NotebookService = Depends()):
    """
    Retrieve a notebook by its unique ID.

    Args:
        notebook_id (str): The unique identifier for the notebook.
        notebook_service (NotebookService): The service handling notebook retrieval.

    Returns:
        The notebook with the specified ID.

    Raises:
        HTTPException: If the notebook with the specified ID is not found.
    """
    notebook = notebook_service.get_notebook_by_id(notebook_id)
    if notebook is None:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return NotebookResponse(**notebook.model_dump())


@router.post(
    "/{notebook_id}/steps", response_model=NotebookStepResponse, status_code=201
)
def add_notebook_step(
    input: CreateNotebookStep,
    notebook_id: str,
    notebook_service: NotebookService = Depends(),
):
    """
    Add a new step to a notebook.

    Args:
        input (CreateNotebookStep): The input data containing the order ID for the new step.
        notebook_id (str): The unique identifier for the notebook.
        notebook_service (NotebookService): The service handling notebook steps.

    Returns:
        The newly created notebook step.

    Raises:
        HTTPException: If the notebook already has 100 steps.
    """
    notebook_step = notebook_service.add_notebook_step(input.order_id, notebook_id)
    return NotebookStepResponse(**notebook_step.model_dump())


@router.put("/{notebook_id}/steps/reorder", response_model=ReorderStepsResponse)
def reorder_notebook_steps(
    notebook_id: str,
    reorder_request: ReorderStepsRequest,
    notebook_service: NotebookService = Depends(),
):
    """
    Reorder steps within a notebook based on the new order provided.

    Args:
        notebook_id (str): The ID of the notebook.
        reorder_request (ReorderStepsRequest): The new ordering of steps.
        notebook_service (NotebookService): The service handling notebook steps.

    Returns:
        List[NotebookStep]: The list of steps with updated order.
    
    Raises:
        HTTPException: If there are duplicate order IDs in the request.
    """

    reordered_steps = notebook_service.reorder_notebook_steps(
        reorder_request.steps, notebook_id
    )
    response = [NotebookStepResponse(**step.model_dump()) for step in reordered_steps]

    logging.error(response)
    return ReorderStepsResponse(steps=response)
