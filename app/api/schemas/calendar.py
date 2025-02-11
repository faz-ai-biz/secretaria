from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime

class EventTime(BaseModel):
    dateTime: datetime
    timeZone: str = "America/Sao_Paulo"

class EventCreate(BaseModel):
    summary: str
    description: Optional[str] = None
    start: EventTime
    end: EventTime
    attendees: Optional[List[Dict[str, str]]] = None
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "summary": "Reunião de Projeto",
            "description": "Discussão sobre novo projeto",
            "start": {
                "dateTime": "2024-01-20T10:00:00",
                "timeZone": "America/Sao_Paulo"
            },
            "end": {
                "dateTime": "2024-01-20T11:00:00",
                "timeZone": "America/Sao_Paulo"
            },
            "attendees": [
                {"email": "participante@exemplo.com"}
            ]
        }
    })

class EventResponse(BaseModel):
    id: str
    summary: str
    description: Optional[str] = None
    start: EventTime
    end: EventTime
    attendees: Optional[List[Dict[str, str]]] = None
    htmlLink: str
    
    model_config = ConfigDict(from_attributes=True)

class ConflictCheck(BaseModel):
    has_conflict: bool
    conflicting_events: List[EventResponse] = [] 