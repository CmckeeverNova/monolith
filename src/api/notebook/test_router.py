import datetime
import logging
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from src.api.notebook.schemas import (
    NotebookResponse,
    NotebookStepResponse,
    ReorderStepsRequest,
)
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


def test_add_step_to_notebook(mock_notebook_service, override_dependency):
    """Test the POST /notebooks/{notebook_id}/steps route"""
    mock_notebook_service.add_notebook_step.return_value = NotebookStepResponse(
        step_id=1, order_id=1, notebook_id="1"
    )

    step_data = {"order_id": 1}

    response = client.post(f"/notebooks/1/steps/", json=step_data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["order_id"] == step_data["order_id"]

    mock_notebook_service.add_notebook_step.assert_called_once_with(
        step_data["order_id"], "1"
    )


def test_reorder_steps_in_notebook_success(mock_notebook_service, override_dependency):
    """Test successful reordering of notebook steps"""
    notebook_id = "1"
    reorder_payload = ReorderStepsRequest(
        steps=[
            {"step_id": 1, "order_id": 2},
            {"step_id": 2, "order_id": 3},
            {"step_id": 3, "order_id": 1},
        ]
    )

    expected_response = [
        NotebookStepResponse(step_id=1, order_id=1, notebook_id="1"),
        NotebookStepResponse(step_id=2, order_id=2, notebook_id="1"),
        NotebookStepResponse(step_id=3, order_id=3, notebook_id="1"),
    ]

    mock_notebook_service.reorder_notebook_steps.return_value = expected_response

    response = client.put(
        f"/notebooks/{notebook_id}/steps/reorder", json=reorder_payload.model_dump()
    )

    assert response.status_code == 200
    response_data = response.json()
    expected_response_data = {
        "steps": [step.model_dump() for step in expected_response]
    }

    assert response_data == expected_response_data

    mock_notebook_service.reorder_notebook_steps.assert_called_once_with(
        reorder_payload.steps, notebook_id
    )


def test_reorder_steps_in_notebook_failure_duplicate_order_id(
    mock_notebook_service, override_dependency
):
    """Test failure for duplicate order IDs in reordering notebook steps"""
    notebook_id = "1"
    reorder_payload = ReorderStepsRequest(
        steps=[
            {"step_id": 1, "order_id": 1},
            {"step_id": 2, "order_id": 1},
            {"step_id": 3, "order_id": 3},
        ]
    )
    mock_notebook_service.reorder_notebook_steps.side_effect = HTTPException(
        status_code=400, detail="Duplicate order IDs found in the provided steps order."
    )

    response = client.put(
        f"/notebooks/{notebook_id}/steps/reorder", json=reorder_payload.model_dump()
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Duplicate order IDs found in the provided steps order."
    }

    mock_notebook_service.reorder_notebook_steps.assert_called_once_with(
        reorder_payload.steps, notebook_id
    )
