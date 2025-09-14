"""
Interface para serviço do WhatsApp
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class WhatsAppService(ABC):
    """
    Interface para serviços do WhatsApp
    """
    
    @abstractmethod
    async def send_message(
        self, 
        phone_number: str, 
        message: str, 
        message_type: str = "text"
    ) -> Dict[str, Any]:
        """Envia uma mensagem via WhatsApp"""
        pass
    
    @abstractmethod
    async def send_template_message(
        self, 
        phone_number: str, 
        template_name: str,
        language_code: str = "pt_BR",
        components: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Envia uma mensagem de template"""
        pass
    
    @abstractmethod
    async def send_interactive_message(
        self, 
        phone_number: str, 
        interactive_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Envia uma mensagem interativa"""
        pass
    
    @abstractmethod
    async def mark_message_as_read(self, message_id: str) -> Dict[str, Any]:
        """Marca uma mensagem como lida"""
        pass
    
    @abstractmethod
    async def get_media_url(self, media_id: str) -> str:
        """Obtém a URL de download de uma mídia"""
        pass
    
    @abstractmethod
    async def download_media(self, media_url: str) -> bytes:
        """Baixa uma mídia do WhatsApp"""
        pass
