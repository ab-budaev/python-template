from fastapi import APIRouter
from pydantic import BaseModel, Field

health_router = APIRouter()


class HealthResponse(BaseModel):
    status: str = Field(default="ok")


@health_router.get(
    "/health",
    response_model=HealthResponse,
    summary="Liveness probe",
)
def health() -> HealthResponse:
    return HealthResponse()
