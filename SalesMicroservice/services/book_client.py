import httpx
from httpx import ConnectError, HTTPStatusError, RequestError
from fastapi import HTTPException, status

BOOKS_SERVICE_URL = "http://127.0.0.1:8002/books"

async def get_book(book_id: int):
    try:
        async with httpx.AsyncClient() as client:
            print(f"Consultando el libro con ID: {book_id}")
            print(f"Consultando: {BOOKS_SERVICE_URL}/{book_id}")
            response = await client.get(f"{BOOKS_SERVICE_URL}/{book_id}")
            print(f"Respuesta completa: {response.text}") 
            response.raise_for_status()
            data = response.json()

            # Validar formato esperado
            if not isinstance(data, dict):
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Respuesta inesperada del servicio de libros: {data}"
                )
            return data

    except ConnectError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar al servicio de libros."
        )
    except HTTPStatusError as he:
        raise HTTPException(
            status_code=he.response.status_code,
            detail=f"Error desde el servicio de libros: {he.response.text}"
        )
    except RequestError as re:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error en la solicitud al servicio de libros: {re}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al obtener el libro: {str(e)}"
        )

async def reduce_stock(book_id: int, quantity: int, token: str):
    try:
        async with httpx.AsyncClient() as client:
            print("Aca estoy")
            response = await client.put(
                f"{BOOKS_SERVICE_URL}/update/{book_id}?new_stock={quantity}",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )
            response.raise_for_status()

    except ConnectError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar al servicio de libros."
        )
    except HTTPStatusError as he:
        raise HTTPException(
            status_code=he.response.status_code,
            detail=f"Error desde el servicio de libros: {he.response.text}"
        )
    except RequestError as re:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error en la solicitud al servicio de libros: {re}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al reducir stock: {str(e)}"
        )
