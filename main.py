from fastapi import FastAPI, HTTPException
from db.db import client
from controladores.libroCRUD import router as libros_router

# Para correr el server:
# uvicorn main:app --reload

app = FastAPI()
app.include_router(libros_router, tags=["libros"], prefix="/libros")
# MongoDB connection URL
@app.on_event("shutdown")
def shutdown_db_client():
    client.close()