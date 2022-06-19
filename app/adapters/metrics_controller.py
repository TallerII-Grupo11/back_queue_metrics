from fastapi import APIRouter, status, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from typing import List

router = APIRouter(tags=["metrics"])


@router.post(
    "/metrics/user",
    response_description="Add new user"
)
async def create_song(
):
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="metric")


@router.get(
    "/metrics/{id}",
    response_description="Get a metric for new user",
    status_code=status.HTTP_200_OK,
)
async def show_song(id: str):
    try:
        return "HOLA"
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
