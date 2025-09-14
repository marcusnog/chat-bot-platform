"""
Implementação do serviço do WhatsApp
"""
import httpx
import json
from typing import Dict, List, Optional, Any
from config import settings
import logging

from ...application.interfaces.whatsapp_service import WhatsAppService

logger = logging.getLogger(__name__)


class WhatsAppServiceImpl(WhatsAppService):
    """
    Implementação do serviço do WhatsApp usando a API oficial
    """
    
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v18.0"
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.access_token = settings.WHATSAPP_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    async def send_message(
        self, 
        phone_number: str, 
        message: str, 
        message_type: str = "text"
    ) -> Dict[str, Any]:
        """Envia uma mensagem via WhatsApp Business API"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": message_type,
            "text": {"body": message} if message_type == "text" else message
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Erro ao enviar mensagem WhatsApp: {e}")
            raise
    
    async def send_template_message(
        self, 
        phone_number: str, 
        template_name: str,
        language_code: str = "pt_BR",
        components: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Envia uma mensagem de template"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
                "components": components or []
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Erro ao enviar template WhatsApp: {e}")
            raise
    
    async def send_interactive_message(
        self, 
        phone_number: str, 
        interactive_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Envia uma mensagem interativa"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "interactive",
            "interactive": interactive_data
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Erro ao enviar mensagem interativa WhatsApp: {e}")
            raise
    
    async def mark_message_as_read(self, message_id: str) -> Dict[str, Any]:
        """Marca uma mensagem como lida"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Erro ao marcar mensagem como lida: {e}")
            raise
    
    async def get_media_url(self, media_id: str) -> str:
        """Obtém a URL de download de uma mídia"""
        url = f"{self.base_url}/{media_id}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                return data.get("url", "")
        except httpx.HTTPError as e:
            logger.error(f"Erro ao obter URL da mídia: {e}")
            raise
    
    async def download_media(self, media_url: str) -> bytes:
        """Baixa uma mídia do WhatsApp"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(media_url, headers=self.headers)
                response.raise_for_status()
                return response.content
        except httpx.HTTPError as e:
            logger.error(f"Erro ao baixar mídia: {e}")
            raise
    
    def create_button_message(self, body_text: str, buttons: List[Dict[str, str]]) -> Dict[str, Any]:
        """Cria uma mensagem com botões"""
        return {
            "type": "button",
            "body": {"text": body_text},
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": button["id"],
                            "title": button["title"]
                        }
                    } for button in buttons
                ]
            }
        }
    
    def create_list_message(self, body_text: str, button_text: str, 
                          sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Cria uma mensagem com lista"""
        return {
            "type": "list",
            "body": {"text": body_text},
            "action": {
                "button": button_text,
                "sections": sections
            }
        }
