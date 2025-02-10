from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.api.schemas import calendar as schemas
from app.services.google_calendar import GoogleCalendarService
from app.services.google_auth import GoogleAuthService
from app.api.models import Cliente

router = APIRouter(tags=["calendar"])

@router.get("/calendar/authorize/{email}")
async def authorize_google_calendar(email: str, db: Session = Depends(get_db)):
    """
    Inicia o processo de autorização do Google Calendar
    """
    cliente = db.query(Cliente).filter(Cliente.email == email).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    auth_url, state = GoogleAuthService.create_authorization_url()
    
    # Retornar a URL de autorização
    return {
        "authorization_url": auth_url,
        "state": state
    }

@router.get("/calendar/oauth2callback")
async def oauth2callback(
    code: str,
    state: str,  # Adicionado parâmetro state
    email: str,
    db: Session = Depends(get_db)
):
    """
    Callback para processar a resposta do Google OAuth2
    """
    try:
        cliente = db.query(Cliente).filter(Cliente.email == email).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        # Obter credenciais do código
        credentials = GoogleAuthService.get_credentials_from_code(code)
        
        # Atualizar credenciais no banco
        cliente.credentials = credentials
        cliente.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Autorização concluída com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro na autorização: {str(e)}"
        )

async def get_calendar_service(email: str, db: Session = Depends(get_db)) -> GoogleCalendarService:
    """
    Dependency para obter o serviço do Google Calendar com credenciais do banco
    """
    cliente = db.query(Cliente).filter(Cliente.email == email).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    if not cliente.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cliente não autorizado para Google Calendar"
        )
    
    service = GoogleCalendarService(cliente.credentials)
    
    # Atualizar credenciais se necessário
    updated_credentials = service.get_updated_credentials()
    if updated_credentials:
        cliente.credentials = updated_credentials
        cliente.updated_at = datetime.utcnow()
        db.commit()
    
    return service

@router.get("/calendar/{email}/events/{date}", response_model=List[schemas.EventResponse])
async def list_events(
    email: str,
    date: str,
    service: GoogleCalendarService = Depends(get_calendar_service)
):
    """
    Lista todos os eventos de uma data específica.
    """
    try:
        event_date = datetime.strptime(date, "%Y-%m-%d")
        events = await service.list_events(event_date)
        return events
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato de data inválido. Use YYYY-MM-DD"
        )

@router.post("/calendar/{email}/events", response_model=schemas.EventResponse)
async def create_event(
    email: str,
    event: schemas.EventCreate,
    service: GoogleCalendarService = Depends(get_calendar_service)
):
    """
    Cria um novo evento no calendário.
    """
    event_data = event.model_dump()
    created_event = await service.create_event(event_data)
    return created_event

@router.delete("/calendar/{email}/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    email: str,
    event_id: str,
    service: GoogleCalendarService = Depends(get_calendar_service)
):
    """
    Remove um evento do calendário.
    """
    await service.delete_event(event_id)

@router.post("/calendar/{email}/check-conflicts", response_model=schemas.ConflictCheck)
async def check_conflicts(
    email: str,
    event: schemas.EventCreate,
    service: GoogleCalendarService = Depends(get_calendar_service)
):
    """
    Verifica conflitos de horário para um evento.
    """
    conflicts = await service.check_conflicts(
        event.start.dateTime,
        event.end.dateTime
    )
    
    return {
        "has_conflict": len(conflicts) > 0,
        "conflicting_events": conflicts
    } 