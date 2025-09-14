"""
Modelos SQLAlchemy para a camada de infraestrutura
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
import uuid

Base = declarative_base()


class UserModel(Base):
    """Modelo SQLAlchemy para usuários"""
    __tablename__ = "users"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    conversations = relationship("ConversationModel", back_populates="user")
    messages = relationship("MessageModel", back_populates="user")


class ConversationModel(Base):
    """Modelo SQLAlchemy para conversas"""
    __tablename__ = "conversations"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    whatsapp_conversation_id = Column(String(100), unique=True, index=True)
    status = Column(String(20), default="active")
    status_reason = Column(String(200))
    agent_id = Column(PostgresUUID(as_uuid=True))
    context = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    user = relationship("UserModel", back_populates="conversations")
    messages = relationship("MessageModel", back_populates="conversation")


class MessageModel(Base):
    """Modelo SQLAlchemy para mensagens"""
    __tablename__ = "messages"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    conversation_id = Column(PostgresUUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    whatsapp_message_id = Column(String(100), unique=True, index=True)
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")
    direction = Column(String(10), nullable=False)
    is_processed = Column(Boolean, default=False)
    message_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    conversation = relationship("ConversationModel", back_populates="messages")
    user = relationship("UserModel", back_populates="messages")


class BotResponseModel(Base):
    """Modelo SQLAlchemy para respostas automáticas"""
    __tablename__ = "bot_responses"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    trigger_keywords = Column(JSON)
    response_text = Column(Text, nullable=False)
    response_type = Column(String(20), default="text")
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    response_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AgentModel(Base):
    """Modelo SQLAlchemy para agentes"""
    __tablename__ = "agents"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone_number = Column(String(20))
    is_active = Column(Boolean, default=True)
    max_conversations = Column(Integer, default=10)
    current_conversations = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
