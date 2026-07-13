from fastapi import FastAPI

from app.routes.query_routes import router as query_router


app = FastAPI(
    title="SQL Automation API",
    description="Natural Language to SQL automation using LangChain",
    version="1.0.0",
)


app.include_router(query_router)


@app.get("/")
def root():
    return {
        "message": "SQL Automation API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }