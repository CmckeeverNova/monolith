# Monolith Notebook API Exercise
This is a simple API that allows you to create, read.

## Setting up the project
1. Install the dependencies by executing `poetry install`
2. Run the database by executing `docker compose up`
3. Run the migrations by executing `make run-migrations`
4. Run the server by executing `make run-server`

### Adding a new notebook using the API
```bash
curl -X POST http://localhost:8000/notebooks/ -d '{"name": "Notebook 1"}' -H 'Content-Type: application/json'
```

### Retrieving all notebooks using the API
```bash
curl -X GET http://localhost:8000/notebooks/
```

### Retrieving a notebook using the API
```bash
curl -X GET http://localhost:8000/notebooks/INSERT_ID_HERE/
```

### Adding a new step to a notebook using the API
```bash
curl -X POST http://localhost:8000/notebooks/INSERT_ID_HERE/steps -d '{"order_id": "1"}' -H 'Content-Type: application/json'
```

### Reordering steps in a notebook using the API
```bash
curl -X PUT http://localhost:8000/notebooks/INSERT_ID_HERE/steps/reorder \
-H 'Content-Type: application/json' \
-d '{
  "steps": [
    {"step_id": 1, "order_id": 2},
    {"step_id": 2, "order_id": 3},
    {"step_id": 3, "order_id": 1}
  ]
}'
```

#### Notes
- dict() is now deprecated so changed to model_dump()
- Had to change some versions in the poetry.lock file in order to get it working