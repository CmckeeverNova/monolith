import datetime
import logging
import uuid
from typing import Dict, List

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

        # Ideally we would slot the new step in the correct order, but for now we'll make sure the order_id is unique
        if any(step.order_id == order_id for step in steps):
            raise HTTPException(
                status_code=400,
                detail=f"Order ID {order_id} already exists in this notebook.",
            )

        new_step = NotebookStep(
            order_id=order_id,
            notebook_id=notebook_id,
        )

        self.session.add(new_step)
        self.session.commit()
        self.session.refresh(new_step)

        return new_step

    def reorder_notebook_steps(
        self, steps_order: List[Dict[str, int]], notebook_id: str
    ) -> List[NotebookStep]:
        statement = select(NotebookStep).where(NotebookStep.notebook_id == notebook_id)
        current_steps = {
            step.step_id: step for step in self.session.exec(statement).all()
        }

        # Ensure there are no order_ids greater than 100
        if any(step["order_id"] > 100 for step in steps_order):
            raise HTTPException(status_code=400, detail="Order ID cannot exceed 100.")

        # Check for duplicate order IDs
        order_ids = [step["order_id"] for step in steps_order]
        if len(order_ids) != len(set(order_ids)):
            raise HTTPException(
                status_code=400,
                detail="Duplicate order IDs found in the provided steps order.",
            )

        # Ensure all step IDs are valid
        provided_step_ids = {step["step_id"] for step in steps_order}
        if not provided_step_ids.issubset(current_steps.keys()):
            missing_steps = current_steps.keys() - provided_step_ids
            raise HTTPException(
                status_code=400,
                detail=f"Missing valid step IDs in the new order: {missing_steps}",
            )

        for new_step in steps_order:
            step_id, new_order_id = new_step["step_id"], new_step["order_id"]
            if step_id in current_steps:
                current_steps[step_id].order_id = new_order_id
                current_steps[step_id].modified_at = datetime.datetime.now(
                    tz=datetime.timezone.utc
                )

        self.session.commit()
        return list(current_steps.values())
