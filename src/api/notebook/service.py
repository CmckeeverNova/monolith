import logging
import uuid

from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from src.api.notebook.models import Notebook, NotebookStep
from src.db.database import get_session


class NotebookService:
    """
    Service class for managing notebooks in the database.

    This service provides methods for retrieving, creating, and managing notebooks.
    It uses the provided SQLModel session to interact with the database.
    """

    def __init__(self, session: Session = Depends(get_session)) -> None:
        """
        Initialize the NotebookService with a database session.

        Args:
            session (Session): The SQLModel session dependency injected by FastAPI.
        """
        self.session = session

    def get_notebooks(self) -> list[Notebook]:
        """
        Retrieve all notebooks from the database.

        Returns:
            List[Notebook]: A list of all notebooks.
        """
        statement = select(Notebook)
        notebooks = self.session.exec(statement).all()
        return notebooks

    def get_notebook_by_id(self, notebook_id: str) -> Notebook | None:
        """
        Retrieve a notebook by its ID from the database.

        Args:
            notebook_id (str): The unique identifier of the notebook.

        Returns:
            Notebook | None: The notebook with the specified ID, or None if not found.
        """
        statement = select(Notebook).where(Notebook.id == notebook_id)
        notebook = self.session.exec(statement).first()
        return notebook

    def create_notebook(self, name: str) -> Notebook:
        """
        Create a new notebook and save it to the database.

        Args:
            name (str): The name of the notebook to be created.

        Returns:
            Notebook: The newly created notebook with its generated ID.
        """
        with self.session.begin():
            notebook = Notebook(id=str(uuid.uuid4()), name=name)
            self.session.add(notebook)

        self.session.refresh(notebook)

        return notebook

    def add_notebook_step(self, order_id: int, notebook_id: str) -> NotebookStep:
        query = select(NotebookStep).where(NotebookStep.notebook_id == notebook_id)
        steps = self.session.exec(query).all()

        if len(steps) >= 100:
            raise HTTPException(
                status_code=400, detail="Cannot exceed 100 steps per notebook."
            )
        # Could be better to just check in the last step_id in the table is 100?

        new_step = NotebookStep(
            order_id=order_id,
            notebook_id=notebook_id,
        )

        self.session.add(new_step)
        self.session.commit()

        self.session.refresh(new_step)

        return new_step
