import datetime
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from src.api.notebook.schemas import NotebookResponse
from src.api.notebook.service import NotebookService
from src.main import app

client = TestClient(app)


@pytest.fixture
def mock_notebook_service():
    """Fixture for mocking NotebookService"""
    service = MagicMock(spec=NotebookService)
    return service


@pytest.fixture
def override_dependency(mock_notebook_service):
    """Fixture to override the NotebookService dependency in the router"""
    app.dependency_overrides[NotebookService] = lambda: mock_notebook_service
    yield
    app.dependency_overrides = {}


def test_get_notebooks(mock_notebook_service, override_dependency):
    """Test the GET /notebooks route"""
    mock_notebook_service.get_notebooks.return_value = [
        NotebookResponse(
            id="1",
            name="Notebook 1",
            created_at=datetime.datetime.now(tz=datetime.timezone.utc),
            modified_at=datetime.datetime.now(tz=datetime.timezone.utc),
        ),
        NotebookResponse(
            id="2",
            name="Notebook 2",
            created_at=datetime.datetime.now(tz=datetime.timezone.utc),
            modified_at=datetime.datetime.now(tz=datetime.timezone.utc),
        ),
    ]

    response = client.get("/notebooks/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": "1", "name": "Notebook 1"},
        {"id": "2", "name": "Notebook 2"},
    ]

    mock_notebook_service.get_notebooks.assert_called_once()


def test_create_notebook(mock_notebook_service, override_dependency):
    """Test the POST /notebooks route"""
    mock_notebook_service.create_notebook.return_value = NotebookResponse(
        id="1", name="New Notebook"
    )

    input_data = {"name": "New Notebook"}
    response = client.post("/notebooks/", json=input_data)

    assert response.status_code == 201
    assert response.json() == {"id": "1", "name": "New Notebook"}

    mock_notebook_service.create_notebook.assert_called_once_with("New Notebook")


def test_get_notebook_by_id_success(mock_notebook_service, override_dependency):
    """Test the GET /notebooks/{notebook_id} route for a valid notebook"""
    mock_notebook_service.get_notebook_by_id.return_value = NotebookResponse(
        id="1", name="Notebook 1"
    )

    response = client.get("/notebooks/1")
    assert response.status_code == 200
    assert response.json() == {"id": "1", "name": "Notebook 1"}

    mock_notebook_service.get_notebook_by_id.assert_called_once_with("1")


def test_get_notebook_by_id_not_found(mock_notebook_service, override_dependency):
    """Test the GET /notebooks/{notebook_id} route for a non-existent notebook"""
    mock_notebook_service.get_notebook_by_id.return_value = None

    response = client.get("/notebooks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Notebook not found"}

    mock_notebook_service.get_notebook_by_id.assert_called_once_with("999")
