import datetime
from typing import List

from sqlmodel import Field, Relationship, SQLModel


class NotebookStep(SQLModel, table=True):
    """
    Represents a notebook step in the database.

    Attributes:
        step_id (int): Unique identifier for the notebook step(primary key).
        order_id (int): The order id for the step.
        notebook_id (int): The associated notebook id for the step.
        created_at (datetime.datetime): Timestamp when the notebook was created.
                                        Defaults to the current UTC time.
        modified_at (datetime.datetime): Timestamp when the notebook was last modified.
                                         Defaults to the current UTC time.
    """

    step_id: int = Field(primary_key=True, index=True)
    order_id: int
    notebook_id: int = Field(foreign_key="notebook.id")
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc),
        description="Timestamp when the notebook step was created. Defaults to the current UTC time.",
    )
    modified_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc),
        description="Timestamp when the notebook step was last modified. Defaults to the current UTC time.",
    )

    notebook: "Notebook" = Relationship(back_populates="steps")


class Notebook(SQLModel, table=True):
    """
    Represents a notebook record in the database.

    Attributes:
        id (str): Unique identifier for the notebook (primary key).
        name (str): Name of the notebook.
        created_at (datetime.datetime): Timestamp when the notebook was created.
                                        Defaults to the current UTC time.
        modified_at (datetime.datetime): Timestamp when the notebook was last modified.
                                         Defaults to the current UTC time.
    """

    id: str = Field(
        primary_key=True, index=True, description="Unique identifier for the notebook."
    )
    name: str = Field(description="Name of the notebook.")
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc),
        description="Timestamp when the notebook was created. Defaults to the current UTC time.",
    )
    modified_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc),
        description="Timestamp when the notebook was last modified. Defaults to the current UTC time.",
    )
    steps: List[NotebookStep] = Relationship(back_populates="notebook")
