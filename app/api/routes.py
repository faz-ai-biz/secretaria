from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from . import models, schemas
from datetime import datetime
from pydantic import EmailStr

router = APIRouter(tags=["clientes"])

@router.post("/clientes/{email}", response_model=schemas.ClienteResponse, status_code=status.HTTP_201_CREATED)
async def create_cliente(
    email: EmailStr,
    cliente: schemas.ClienteCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo cliente.
    
    - **email**: Email único do cliente (obrigatório)
    - **credentials**: Credenciais do cliente
    - **expiry**: Data de expiração
    """
    if db.query(models.Cliente).filter(models.Cliente.email == email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    
    db_cliente = models.Cliente(
        email=email,
        credentials=cliente.credentials,
        expiry=cliente.expiry
    )
    
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/clientes", response_model=List[schemas.ClienteResponse])
async def list_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todos os clientes.
    """
    clientes = db.query(models.Cliente).offset(skip).limit(limit).all()
    return clientes

@router.get("/clientes/{cliente_id}", response_model=schemas.ClienteResponse)
async def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Obtém um cliente específico pelo ID.
    """
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.patch("/clientes/{cliente_id}", response_model=schemas.ClienteResponse)
async def update_cliente(cliente_id: int, cliente: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    """
    Atualiza as informações de credentials e expiry de um cliente.
    """
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    update_data = cliente.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cliente, field, value)
    
    db_cliente.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Remove um cliente.
    """
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db.delete(cliente)
    db.commit() 