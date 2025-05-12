from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
import httpx

app = FastAPI()

# Mapeo de prefijos de ruta a microservicios
SERVICE_MAP = {
    "users": "http://localhost:8001",
    "orders": "http://localhost:8002",
    "payments": "http://localhost:8003",
}

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service: str, path: str, request: Request):
    if service not in SERVICE_MAP:
        return JSONResponse(status_code=404, content={"detail": "Servicio no encontrado"})

    target_url = f"{SERVICE_MAP[service]}/{path}"

    try:
        # Extrae datos de la solicitud original
        body = await request.body()
        headers = dict(request.headers)

        # Envía la solicitud al microservicio correspondiente
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                content=body,
                headers=headers,
                params=request.query_params
            )

        # Devuelve la respuesta original
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type")
        )

    except httpx.RequestError as e:
        return JSONResponse(status_code=500, content={"detail": f"Error en la conexión con el microservicio: {str(e)}"})
