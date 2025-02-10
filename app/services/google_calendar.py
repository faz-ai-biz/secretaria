from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os
import pickle
from typing import List, Dict
from app.core.config import settings

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarService:
    def __init__(self, credentials_json: Dict):
        """
        Inicializa o serviço com as credenciais armazenadas no banco
        """
        credentials = Credentials(
            token=credentials_json.get('token'),
            refresh_token=credentials_json.get('refresh_token'),
            token_uri=credentials_json.get('token_uri'),
            client_id=credentials_json.get('client_id'),
            client_secret=credentials_json.get('client_secret'),
            scopes=credentials_json.get('scopes')
        )

        # Atualiza o token se necessário
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            self.updated_credentials = credentials
        else:
            self.updated_credentials = None

        self.service = build('calendar', 'v3', credentials=credentials)

    def get_updated_credentials(self) -> Dict:
        """Retorna as credenciais atualizadas se houver"""
        if self.updated_credentials:
            return {
                'token': self.updated_credentials.token,
                'refresh_token': self.updated_credentials.refresh_token,
                'token_uri': self.updated_credentials.token_uri,
                'client_id': self.updated_credentials.client_id,
                'client_secret': self.updated_credentials.client_secret,
                'scopes': self.updated_credentials.scopes
            }
        return None

    async def list_events(self, date: datetime) -> List[dict]:
        time_min = datetime.combine(date, datetime.min.time())
        time_max = datetime.combine(date, datetime.max.time())
        
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=time_min.isoformat() + 'Z',
            timeMax=time_max.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])

    async def create_event(self, event_data: dict) -> dict:
        event = self.service.events().insert(
            calendarId='primary',
            body=event_data
        ).execute()
        return event

    async def delete_event(self, event_id: str):
        self.service.events().delete(
            calendarId='primary',
            eventId=event_id
        ).execute()

    async def check_conflicts(self, start_time: datetime, end_time: datetime) -> List[dict]:
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=start_time.isoformat() + 'Z',
            timeMax=end_time.isoformat() + 'Z',
            singleEvents=True
        ).execute()
        
        return events_result.get('items', []) 