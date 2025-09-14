"""
Endpoints de mensagens
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from src.infrastructure.database.database import get_db
from src.infrastructure.database.auth_models import AuthUser
from src.presentation.controllers.auth_controller import get_current_user
from src.infrastructure.repositories.message_repository_impl import MessageRepositoryImpl
from src.infrastructure.repositories.conversation_repository_impl import ConversationRepositoryImpl
from src.domain.entities.message import Message
from src.domain.entities.conversation import Conversation
from src.domain.value_objects.message_content import MessageContent
from src.domain.value_objects.phone_number import PhoneNumber
from src.domain.value_objects.message_direction import MessageDirection
from src.domain.value_objects.message_status import MessageStatus

router = APIRouter(prefix="/messages", tags=["messages"])

# Schemas
class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender_id: Optional[str] = None
    recipient_id: Optional[str] = None
    content: str
    direction: str
    status: str
    timestamp: str
    metadata: Optional[dict] = None

class MessageCreateRequest(BaseModel):
    conversation_id: str
    content: str
    direction: str = "outbound"
    recipient_phone: Optional[str] = None

class MessageUpdateRequest(BaseModel):
    status: Optional[str] = None
    metadata: Optional[dict] = None

class MessageStatsResponse(BaseModel):
    total_messages: int
    inbound_messages: int
    outbound_messages: int
    delivered_messages: int
    failed_messages: int
    pending_messages: int

# Dependências
def get_message_repository(db: Session = Depends(get_db)) -> MessageRepositoryImpl:
    return MessageRepositoryImpl(db)

def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepositoryImpl:
    return ConversationRepositoryImpl(db)

# Endpoints
@router.get("/", response_model=List[MessageResponse])
async def get_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    conversation_id: Optional[str] = Query(None),
    direction: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    message_repo: MessageRepositoryImpl = Depends(get_message_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Lista todas as mensagens com filtros"""
    try:
        if conversation_id:
            messages = message_repo.get_by_conversation_id(UUID(conversation_id))
        else:
            messages = message_repo.get_all(skip=skip, limit=limit)
        
        # Aplicar filtros
        if direction:
            messages = [m for m in messages if m.direction.value == direction]
        
        if status:
            messages = [m for m in messages if m.status.value == status]
        
        return [
            MessageResponse(
                id=str(message.id),
                conversation_id=str(message.conversation_id),
                sender_id=str(message.sender_id) if message.sender_id else None,
                recipient_id=str(message.recipient_id) if message.recipient_id else None,
                content=message.content.value,
                direction=message.direction.value,
                status=message.status.value,
                timestamp=message.timestamp.isoformat(),
                metadata=message.message_metadata
            )
            for message in messages
        ]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de conversa inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar mensagens: {str(e)}"
        )

@router.get("/stats", response_model=MessageStatsResponse)
async def get_message_stats(
    message_repo: MessageRepositoryImpl = Depends(get_message_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém estatísticas das mensagens"""
    try:
        messages = message_repo.get_all()
        total_messages = len(messages)
        
        inbound_messages = len([m for m in messages if m.direction.value == "inbound"])
        outbound_messages = len([m for m in messages if m.direction.value == "outbound"])
        delivered_messages = len([m for m in messages if m.status.value == "delivered"])
        failed_messages = len([m for m in messages if m.status.value == "failed"])
        pending_messages = len([m for m in messages if m.status.value == "pending"])
        
        return MessageStatsResponse(
            total_messages=total_messages,
            inbound_messages=inbound_messages,
            outbound_messages=outbound_messages,
            delivered_messages=delivered_messages,
            failed_messages=failed_messages,
            pending_messages=pending_messages
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar estatísticas: {str(e)}"
        )

@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: str,
    message_repo: MessageRepositoryImpl = Depends(get_message_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém uma mensagem específica"""
    try:
        message = message_repo.get_by_id(UUID(message_id))
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensagem não encontrada"
            )
        
        return MessageResponse(
            id=str(message.id),
            conversation_id=str(message.conversation_id),
            sender_id=str(message.sender_id) if message.sender_id else None,
            recipient_id=str(message.recipient_id) if message.recipient_id else None,
            content=message.content.value,
            direction=message.direction.value,
            status=message.status.value,
            timestamp=message.timestamp.isoformat(),
            metadata=message.message_metadata
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de mensagem inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar mensagem: {str(e)}"
        )

@router.post("/", response_model=MessageResponse)
async def create_message(
    message_data: MessageCreateRequest,
    message_repo: MessageRepositoryImpl = Depends(get_message_repository),
    conversation_repo: ConversationRepositoryImpl = Depends(get_conversation_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Cria uma nova mensagem"""
    try:
        # Verificar se conversa existe
        conversation = conversation_repo.get_by_id(UUID(message_data.conversation_id))
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversa não encontrada"
            )
        
        # Criar mensagem
        message = Message(
            conversation_id=conversation.id,
            content=MessageContent(message_data.content),
            direction=MessageDirection(message_data.direction),
            status=MessageStatus.PENDING
        )
        
        # Se for mensagem outbound, definir recipient_id
        if message_data.direction == "outbound" and message_data.recipient_phone:
            message.recipient_id = conversation.user_id
        
        created_message = message_repo.add(message)
        
        return MessageResponse(
            id=str(created_message.id),
            conversation_id=str(created_message.conversation_id),
            sender_id=str(created_message.sender_id) if created_message.sender_id else None,
            recipient_id=str(created_message.recipient_id) if created_message.recipient_id else None,
            content=created_message.content.value,
            direction=created_message.direction.value,
            status=created_message.status.value,
            timestamp=created_message.timestamp.isoformat(),
            metadata=created_message.message_metadata
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de conversa inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar mensagem: {str(e)}"
        )

@router.put("/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: str,
    message_data: MessageUpdateRequest,
    message_repo: MessageRepositoryImpl = Depends(get_message_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Atualiza uma mensagem"""
    try:
        message = message_repo.get_by_id(UUID(message_id))
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensagem não encontrada"
            )
        
        # Atualizar campos fornecidos
        if message_data.status:
            message.status = MessageStatus(message_data.status)
        
        if message_data.metadata is not None:
            message.message_metadata = message_data.metadata
        
        updated_message = message_repo.update(message)
        
        return MessageResponse(
            id=str(updated_message.id),
            conversation_id=str(updated_message.conversation_id),
            sender_id=str(updated_message.sender_id) if updated_message.sender_id else None,
            recipient_id=str(updated_message.recipient_id) if updated_message.recipient_id else None,
            content=updated_message.content.value,
            direction=updated_message.direction.value,
            status=updated_message.status.value,
            timestamp=updated_message.timestamp.isoformat(),
            metadata=updated_message.message_metadata
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de mensagem inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar mensagem: {str(e)}"
        )

@router.delete("/{message_id}")
async def delete_message(
    message_id: str,
    message_repo: MessageRepositoryImpl = Depends(get_message_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Deleta uma mensagem"""
    try:
        message = message_repo.get_by_id(UUID(message_id))
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensagem não encontrada"
            )
        
        message_repo.delete(message.id)
        return {"message": "Mensagem deletada com sucesso"}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de mensagem inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar mensagem: {str(e)}"
        )
