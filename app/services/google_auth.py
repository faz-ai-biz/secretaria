from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from fastapi import HTTPException
from app.core.config import settings
import json

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleAuthService:
    @staticmethod
    def create_authorization_url() -> tuple[str, str]:
        """Cria URL de autorização e state"""
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GOOGLE_CALENDAR_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CALENDAR_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uri": settings.GOOGLE_CALENDAR_REDIRECT_URI,
                }
            },
            scopes=SCOPES
        )
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        return authorization_url, state

    @staticmethod
    def get_credentials_from_code(code: str) -> dict:
        """Obtém credenciais a partir do código de autorização"""
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GOOGLE_CALENDAR_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CALENDAR_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uri": settings.GOOGLE_CALENDAR_REDIRECT_URI,
                }
            },
            scopes=SCOPES
        )
        
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        return {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes
        }

    @staticmethod
    def credentials_to_dict(credentials: Credentials) -> dict:
        """Converte objeto Credentials para dicionário"""
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        } 