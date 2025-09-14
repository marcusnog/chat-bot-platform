"""
Implementação do repositório de conversas
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from ...domain.entities.conversation import Conversation
from ...domain.repositories.conversation_repository import ConversationRepository
from ...domain.value_objects.conversation_status import ConversationStatus, ConversationStatusValue
from ..database.models import ConversationModel


class ConversationRepositoryImpl(ConversationRepository):
    """
    Implementação do repositório de conversas usando SQLAlchemy
    """
    
    def __init__(self, db_session: Session):
        self._db = db_session
    
    async def save(self, conversation: Conversation) -> Conversation:
        """Salva uma conversa"""
        if conversation.id:
            # Atualização
            db_conversation = await self._get_by_id(conversation.id)
            if db_conversation:
                db_conversation.status = conversation.status.status.value
                db_conversation.status_reason = conversation.status.reason
                db_conversation.agent_id = conversation.agent_id
                db_conversation.context = conversation.context
                db_conversation.updated_at = conversation.updated_at
            else:
                raise ValueError("Conversa não encontrada")
        else:
            # Criação
            db_conversation = ConversationModel(
                user_id=conversation.user_id,
                whatsapp_conversation_id=conversation.whatsapp_conversation_id,
                status=conversation.status.status.value,
                status_reason=conversation.status.reason,
                agent_id=conversation.agent_id,
                context=conversation.context,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at
            )
            self._db.add(db_conversation)
        
        self._db.commit()
        self._db.refresh(db_conversation)
        
        return self._to_entity(db_conversation)
    
    async def find_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Busca conversa por ID"""
        db_conversation = await self._get_by_id(conversation_id)
        return self._to_entity(db_conversation) if db_conversation else None
    
    async def find_by_whatsapp_id(self, whatsapp_conversation_id: str) -> Optional[Conversation]:
        """Busca conversa por ID do WhatsApp"""
        db_conversation = self._db.query(ConversationModel).filter(
            ConversationModel.whatsapp_conversation_id == whatsapp_conversation_id
        ).first()
        
        return self._to_entity(db_conversation) if db_conversation else None
    
    async def find_by_user_id(self, user_id: UUID) -> List[Conversation]:
        """Busca conversas de um usuário"""
        db_conversations = self._db.query(ConversationModel).filter(
            ConversationModel.user_id == user_id
        ).all()
        
        return [self._to_entity(db_conversation) for db_conversation in db_conversations]
    
    async def find_active_by_user_id(self, user_id: UUID) -> Optional[Conversation]:
        """Busca conversa ativa de um usuário"""
        db_conversation = self._db.query(ConversationModel).filter(
            ConversationModel.user_id == user_id,
            ConversationModel.status == ConversationStatus.ACTIVE.value
        ).first()
        
        return self._to_entity(db_conversation) if db_conversation else None
    
    async def find_by_status(
        self, 
        status: ConversationStatus, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Conversation]:
        """Busca conversas por status"""
        db_conversations = self._db.query(ConversationModel).filter(
            ConversationModel.status == status.value
        ).offset(skip).limit(limit).all()
        
        return [self._to_entity(db_conversation) for db_conversation in db_conversations]
    
    async def find_by_agent_id(self, agent_id: UUID) -> List[Conversation]:
        """Busca conversas de um agente"""
        db_conversations = self._db.query(ConversationModel).filter(
            ConversationModel.agent_id == agent_id
        ).all()
        
        return [self._to_entity(db_conversation) for db_conversation in db_conversations]
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Conversation]:
        """Lista todas as conversas"""
        db_conversations = self._db.query(ConversationModel).offset(skip).limit(limit).all()
        return [self._to_entity(db_conversation) for db_conversation in db_conversations]
    
    async def delete(self, conversation_id: UUID) -> bool:
        """Remove uma conversa"""
        db_conversation = await self._get_by_id(conversation_id)
        if db_conversation:
            self._db.delete(db_conversation)
            self._db.commit()
            return True
        return False
    
    async def count_by_user_id(self, user_id: UUID) -> int:
        """Conta conversas de um usuário"""
        return self._db.query(ConversationModel).filter(
            ConversationModel.user_id == user_id
        ).count()
    
    async def _get_by_id(self, conversation_id: UUID) -> Optional[ConversationModel]:
        """Busca conversa por ID no banco"""
        return self._db.query(ConversationModel).filter(ConversationModel.id == conversation_id).first()
    
    def _to_entity(self, db_conversation: ConversationModel) -> Conversation:
        """Converte modelo do banco para entidade do domínio"""
        status = ConversationStatusValue(
            status=ConversationStatus(db_conversation.status),
            timestamp=db_conversation.created_at,  # Usar created_at como fallback
            reason=db_conversation.status_reason,
            agent_id=db_conversation.agent_id
        )
        
        return Conversation(
            id=db_conversation.id,
            user_id=db_conversation.user_id,
            whatsapp_conversation_id=db_conversation.whatsapp_conversation_id,
            status=status,
            context=db_conversation.context or {},
            agent_id=db_conversation.agent_id,
            created_at=db_conversation.created_at,
            updated_at=db_conversation.updated_at
        )
