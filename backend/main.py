
"""Entrypoint for the backend application (FastAPI example)."""
from fastapi import FastAPI
from .api import routes, middleware

app = FastAPI()
middleware.attach_middlewares(app)
routes.register_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
