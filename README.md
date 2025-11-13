# Airline Route Planner — Frontend + Flask Backend + Docker

## What I added
- A small Flask backend that provides:
  - `GET /api/sample` — returns a sample nodes list and weight matrix.
  - `POST /api/compute` — accepts JSON `{ "nodes": [...], "weights": [[...]] }` and returns shortest distances computed by Floyd–Warshall.
- Backend also serves the existing static frontend files (index.html, styles.css).
- Dockerfile + docker-compose for easy deployment.

## Run locally (VS Code)
1. Open this folder in VS Code.
2. (Optional) Create and activate a Python virtualenv.
3. Install requirements:
   ```
   pip install -r backend/requirements.txt
   ```
4. Run:
   ```
   python backend/app.py
   ```
   Then open http://localhost:5000

## Run with Docker
Build and run:
```
docker build -t airline-planner .
docker run -p 5000:5000 airline-planner
```
Or with docker-compose:
```
docker-compose up --build
```

## API examples
Sample compute request:
```
POST /api/compute
Content-Type: application/json
{
  "nodes": ["JFK","LHR","CDG"],
  "weights": [
    [0, 5540, 5836],
    [null, 0, 344],
    [null, null, 0]
  ]
}
```

Response will include `distances` matrix and `next_hop` for path reconstruction.
