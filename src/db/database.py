from sqlmodel import Session, create_engine

from src.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_session():
    """
    Provide a SQLModel session generator for dependency injection.

    This function yields a database session object using a context manager, ensuring
    that the session is properly closed after use. It can be injected into FastAPI
    endpoints or services.

    Example:
        session: Session = Depends(get_session)

    Yields:
        Session: The SQLModel session object.
    """
    with Session(engine) as session:
        yield session
