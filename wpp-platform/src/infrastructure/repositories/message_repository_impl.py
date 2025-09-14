"""
Implementação do repositório de mensagens
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.entities.message import Message
from src.domain.repositories.message_repository import MessageRepository
from src.infrastructure.database.models import MessageModel


class MessageRepositoryImpl(MessageRepository):
    """Implementação do repositório de mensagens"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, message: Message) -> Message:
        """Salva uma mensagem"""
        message_model = MessageModel(
            id=message.id,
            conversation_id=message.conversation_id,
            sender_phone=message.sender_phone.value,
            content=message.content.value,
            message_type=message.message_type,
            timestamp=message.timestamp,
            is_from_bot=message.is_from_bot,
            metadata=message.metadata
        )
        
        self.db.add(message_model)
        self.db.commit()
        self.db.refresh(message_model)
        
        return self._to_domain(message_model)
    
    def find_by_id(self, message_id: str) -> Optional[Message]:
        """Busca mensagem por ID"""
        message_model = self.db.query(MessageModel).filter(
            MessageModel.id == message_id
        ).first()
        
        if message_model:
            return self._to_domain(message_model)
        return None
    
    def find_by_conversation_id(self, conversation_id: str) -> List[Message]:
        """Busca mensagens por ID da conversa"""
        message_models = self.db.query(MessageModel).filter(
            MessageModel.conversation_id == conversation_id
        ).order_by(MessageModel.timestamp).all()
        
        return [self._to_domain(model) for model in message_models]
    
    def find_by_sender_phone(self, phone: str) -> List[Message]:
        """Busca mensagens por telefone do remetente"""
        message_models = self.db.query(MessageModel).filter(
            MessageModel.sender_phone == phone
        ).order_by(MessageModel.timestamp).all()
        
        return [self._to_domain(model) for model in message_models]
    
    def _to_domain(self, model: MessageModel) -> Message:
        """Converte modelo para entidade de domínio"""
        from src.domain.value_objects.phone_number import PhoneNumber
        from src.domain.value_objects.message_content import MessageContent
        
        return Message(
            id=model.id,
            conversation_id=model.conversation_id,
            sender_phone=PhoneNumber(model.sender_phone),
            content=MessageContent(model.content),
            message_type=model.message_type,
            timestamp=model.timestamp,
            is_from_bot=model.is_from_bot,
            metadata=model.metadata or {}
        )
