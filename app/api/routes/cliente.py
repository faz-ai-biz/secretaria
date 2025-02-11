from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.schemas.cliente import ClienteCreate, ClienteResponse, ClienteUpdate
from app.services.cliente_service import ClienteService

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"]
)

@router.post("/{email}", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def create_cliente(
    email: str,
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    return await ClienteService.create_cliente(db=db, cliente=cliente)

@router.get("/{email}", response_model=ClienteResponse)
async def get_cliente(
    email: str,
    db: Session = Depends(get_db)
):
    return await ClienteService.get_cliente_by_email(db=db, email=email)

@router.get("/", response_model=List[ClienteResponse])
async def list_clientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return await ClienteService.list_clientes(db=db, skip=skip, limit=limit)

@router.put("/{email}", response_model=ClienteResponse)
async def update_cliente(
    email: str,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db)
):
    return await ClienteService.update_cliente(db=db, email=email, cliente=cliente)

@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(
    email: str,
    db: Session = Depends(get_db)
):
    await ClienteService.delete_cliente(db=db, email=email)
    return None 