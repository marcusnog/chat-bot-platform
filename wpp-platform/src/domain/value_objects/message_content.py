"""
Value Object para conteúdo de mensagem
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class MessageType(Enum):
    """Tipos de mensagem suportados"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    DOCUMENT = "document"
    VIDEO = "video"
    LOCATION = "location"
    CONTACT = "contact"
    TEMPLATE = "template"
    INTERACTIVE = "interactive"


class MessageDirection(Enum):
    """Direção da mensagem"""
    INCOMING = "incoming"
    OUTGOING = "outgoing"


@dataclass(frozen=True)
class MessageContent:
    """
    Value Object para representar o conteúdo de uma mensagem
    """
    text: str
    message_type: MessageType
    direction: MessageDirection
    metadata: Optional[dict] = None
    
    def __post_init__(self):
        """Valida o conteúdo da mensagem"""
        if not self.text or not self.text.strip():
            raise ValueError("Conteúdo da mensagem não pode ser vazio")
        
        if len(self.text) > 4096:
            raise ValueError("Conteúdo da mensagem muito longo (máximo 4096 caracteres)")
    
    def is_text_message(self) -> bool:
        """Verifica se é uma mensagem de texto"""
        return self.message_type == MessageType.TEXT
    
    def is_media_message(self) -> bool:
        """Verifica se é uma mensagem de mídia"""
        return self.message_type in [
            MessageType.IMAGE, 
            MessageType.AUDIO, 
            MessageType.DOCUMENT, 
            MessageType.VIDEO
        ]
    
    def get_display_text(self) -> str:
        """
        Retorna texto para exibição baseado no tipo de mensagem
        """
        if self.is_text_message():
            return self.text
        
        type_display = {
            MessageType.IMAGE: "[Imagem]",
            MessageType.AUDIO: "[Áudio]",
            MessageType.DOCUMENT: "[Documento]",
            MessageType.VIDEO: "[Vídeo]",
            MessageType.LOCATION: "[Localização]",
            MessageType.CONTACT: "[Contato]",
            MessageType.TEMPLATE: "[Template]",
            MessageType.INTERACTIVE: "[Interativo]"
        }
        
        base_text = type_display.get(self.message_type, "[Mensagem]")
        
        # Adiciona legenda se disponível
        if self.metadata and 'caption' in self.metadata:
            return f"{base_text}: {self.metadata['caption']}"
        
        return base_text
    
    def __str__(self) -> str:
        return self.get_display_text()
    
    def __repr__(self) -> str:
        return f"MessageContent(text='{self.text[:50]}...', type={self.message_type.value}, direction={self.direction.value})"
