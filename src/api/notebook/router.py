from fastapi import APIRouter, Depends, HTTPException

from src.api.notebook.schemas import CreateNotebook, NotebookResponse
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
    return [NotebookResponse(**notebook.dict()) for notebook in notebooks]


@router.post("/", response_model=NotebookResponse, status_code=201)
def create_notebook(input: CreateNotebook, notebook_service: NotebookService = Depends()):
    """
    Create a new notebook with the specified name.

    Args:
        input (CreateNotebook): The input data containing the notebook name.
        notebook_service (NotebookService): The service handling notebook creation.

    Returns:
        The newly created notebook.
    """
    notebook = notebook_service.create_notebook(input.name)
    return NotebookResponse(**notebook.dict())


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
    return NotebookResponse(**notebook.dict())
