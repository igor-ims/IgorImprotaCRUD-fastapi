from fastapi import HTTPException, APIRouter
from db.db import collection
from modelos.libro import Libro

# Agregar libros : Aqui debemos incluir una regla de negocio que valide que no existe otro libro con el mismo ISBN. 
#   Si existe, muestra un mensaje de error y no lo agrega. 
# Borrar libros
# Buscar libros : puede ser por nombre o ISBN
# Actualizar libro

router = APIRouter()

@router.post('/', response_description="Crear un nuevo libro", response_model=Libro)
async def create_libro(Libro : Libro):
    libro_existente = await collection.find_one({'isbn': Libro.isbn})

    if libro_existente != None:
        raise HTTPException(status_code=404, detail=f'ISBN {Libro.isbn} ya existe.')
    
    result = await collection.insert_one(Libro.model_dump())
    Libro._id = str(result.inserted_id)

    return Libro

@router.get('/', response_description="Listar todos los libros", response_model=list[Libro])
async def read_libros():
    libros = await collection.find().to_list(100)

    if not libros:
        raise HTTPException(status_code=404, detail="No hay libros disponibles")
    
    for l in libros:
        l['_id'] = str(l['_id'])

    return libros

@router.get('/find-isbn/{isbn}', response_description= 'Busca un libro por su ISBN', response_model=Libro)
async def find_libro_by_isbn(isbn: str):
    libro = await collection.find_one({'isbn': isbn})

    if libro:
        return libro
    
    raise HTTPException(status_code=404, detail=f'Libro con ISBN {isbn} no encontrado.')

@router.get('/find-nombre/{nombre}', response_description= 'Busca un libro por su nombre', response_model=Libro)
async def find_libro_by_nombre(nombre: str):
    libro = await collection.find_one({'nombre': nombre})

    if libro:
        return libro
    
    raise HTTPException(status_code=404, detail=f'Libro con nombre {nombre} no encontrado.')

@router.put('/{isbn}', response_description='Actualiza un Libro, buscandolo por su ISBN', response_model=Libro)
async def update_libro(isbn: str, libro: Libro):
    if isbn != libro.isbn:
        libro_existente = await collection.find_one({'isbn': libro.isbn})
        if libro_existente:
            raise HTTPException(status_code=400, detail=f'El ISBN {libro.isbn} ya existe en otro libro.')

    updated_libro = await collection.find_one_and_update({'isbn': isbn}, {'$set': libro.dict()})

    if updated_libro:
        return Libro(**updated_libro)

    raise HTTPException(status_code=404, detail=f'Libro con ISBN {isbn} no encontrado.')


@router.delete('/{isbn}', response_description='Borra un Libro por su ISBN', response_model=Libro)
async def delete_libro(isbn: str):
    deleted_libro = await collection.find_one_and_delete({'isbn': isbn})

    if deleted_libro:
        return deleted_libro
    
    raise HTTPException(status_code=404, detail=f'Libro con ISBN {isbn} no encontrado.')