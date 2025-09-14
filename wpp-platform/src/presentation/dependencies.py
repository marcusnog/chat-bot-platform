"""
Dependências para injeção de dependência
"""
import sys
import os
from functools import lru_cache
from sqlalchemy.orm import Session
from fastapi import Depends

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.repositories.conversation_repository_impl import ConversationRepositoryImpl
from src.infrastructure.repositories.message_repository_impl import MessageRepositoryImpl
from src.infrastructure.external_services.whatsapp_service_impl import WhatsAppServiceImpl
from src.infrastructure.external_services.ai_service_impl import AIServiceImpl
from src.domain.services.message_processing_service import DefaultMessageProcessingService


def get_user_repository(db: Session = Depends(get_db)):
    """Dependency para repositório de usuários"""
    return UserRepositoryImpl(db)


def get_conversation_repository(db: Session = Depends(get_db)):
    """Dependency para repositório de conversas"""
    return ConversationRepositoryImpl(db)


def get_message_repository(db: Session = Depends(get_db)):
    """Dependency para repositório de mensagens"""
    return MessageRepositoryImpl(db)


@lru_cache()
def get_whatsapp_service():
    """Dependency para serviço do WhatsApp"""
    return WhatsAppServiceImpl()


@lru_cache()
def get_ai_service():
    """Dependency para serviço de IA"""
    return AIServiceImpl()


@lru_cache()
def get_message_processing_service():
    """Dependency para serviço de processamento de mensagens"""
    return DefaultMessageProcessingService()
