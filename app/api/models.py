from sqlalchemy import Column, Integer, String, JSON, DateTime, func, Sequence
from app.core.database import Base

class Cliente(Base):
    __tablename__ = "cliente"
    
    id = Column(Integer, Sequence('cliente_id_seq'), primary_key=True)
    email = Column(String(255), unique=True, index=True)
    credentials = Column(JSON, nullable=True)
    expiry = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.current_timestamp())

    def __repr__(self):
        return f"<Cliente(id={self.id}, email={self.email})>" 