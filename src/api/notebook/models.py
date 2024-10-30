import datetime

from sqlmodel import Field, SQLModel


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
    id: str = Field(primary_key=True, index=True, description="Unique identifier for the notebook.")
    name: str = Field(description="Name of the notebook.")
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc),
        description="Timestamp when the notebook was created. Defaults to the current UTC time."
    )
    modified_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc),
        description="Timestamp when the notebook was last modified. Defaults to the current UTC time."
    )
