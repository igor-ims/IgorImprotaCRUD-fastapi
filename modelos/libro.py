from pydantic import BaseModel

class Libro(BaseModel):
    nombre : str
    autor : str
    isbn : str