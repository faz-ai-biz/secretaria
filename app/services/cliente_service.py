from sqlalchemy.orm import Session
from app.api.models import Cliente
from app.api.schemas.cliente import ClienteCreate, ClienteUpdate
from fastapi import HTTPException, status
from datetime import datetime
from typing import List, Optional

class ClienteService:
    @staticmethod
    async def create_cliente(db: Session, cliente: ClienteCreate) -> Cliente:
        db_cliente = Cliente(
            email=cliente.email,
            credentials=cliente.credentials
        )
        try:
            db.add(db_cliente)
            db.commit()
            db.refresh(db_cliente)
            return db_cliente
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao criar cliente: {str(e)}"
            )

    @staticmethod
    async def get_cliente_by_email(db: Session, email: str) -> Cliente:
        cliente = db.query(Cliente).filter(Cliente.email == email).first()
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
        return cliente

    @staticmethod
    async def list_clientes(db: Session, skip: int = 0, limit: int = 100) -> List[Cliente]:
        return db.query(Cliente).offset(skip).limit(limit).all()

    @staticmethod
    async def update_cliente(db: Session, email: str, cliente: ClienteUpdate) -> Cliente:
        db_cliente = await ClienteService.get_cliente_by_email(db, email)
        
        update_data = cliente.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cliente, field, value)
        
        db_cliente.updated_at = datetime.utcnow()
        try:
            db.commit()
            db.refresh(db_cliente)
            return db_cliente
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao atualizar cliente: {str(e)}"
            )

    @staticmethod
    async def delete_cliente(db: Session, email: str) -> None:
        db_cliente = await ClienteService.get_cliente_by_email(db, email)
        try:
            db.delete(db_cliente)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao deletar cliente: {str(e)}"
            ) 