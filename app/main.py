from fastapi import FastAPI
from app.db import test_connection, get_postulaciones, get_stats

app = FastAPI(title="MVP DataOps API")

@app.get("/")
def read_root():
    return {"message": "API Operativa"}

@app.get("/db-health")
def db_health():
    return test_connection()

@app.get("/postulaciones-demo")
def read_postulaciones(limit: int = 20):
    return get_postulaciones(limit)

@app.get("/postulaciones-demo/stats")
def read_stats():
    return get_stats()