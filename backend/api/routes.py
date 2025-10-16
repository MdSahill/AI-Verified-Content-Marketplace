
"""API routes (Flask/FastAPI style placeholder)."""

def register_routes(app):
    @app.get("/health")
    def health():
        return {"status": "ok"}
