"""
Endpoints de conversas
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
from src.infrastructure.repositories.conversation_repository_impl import ConversationRepositoryImpl
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.domain.entities.conversation import Conversation
from src.domain.entities.user import User
from src.domain.value_objects.conversation_status import ConversationStatus

router = APIRouter(prefix="/conversations", tags=["conversations"])

# Schemas
class ConversationResponse(BaseModel):
    id: str
    user_id: str
    user_name: str
    user_phone: str
    status: str
    created_at: str
    updated_at: str
    last_message_at: Optional[str] = None
    message_count: int = 0
    unread_count: int = 0

class ConversationCreateRequest(BaseModel):
    user_id: str

class ConversationUpdateRequest(BaseModel):
    status: Optional[str] = None

class ConversationStatsResponse(BaseModel):
    total_conversations: int
    active_conversations: int
    closed_conversations: int
    pending_conversations: int
    total_messages: int

# Dependências
def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepositoryImpl:
    return ConversationRepositoryImpl(db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    return UserRepositoryImpl(db)

# Endpoints
@router.get("/", response_model=List[ConversationResponse])
async def get_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    conversation_repo: ConversationRepositoryImpl = Depends(get_conversation_repository),
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Lista todas as conversas com filtros"""
    try:
        conversations = conversation_repo.get_all(skip=skip, limit=limit)
        
        # Aplicar filtros
        if status:
            conversations = [c for c in conversations if c.status.value == status]
        
        if user_id:
            conversations = [c for c in conversations if str(c.user_id) == user_id]
        
        # Buscar dados dos usuários
        response_conversations = []
        for conv in conversations:
            user = user_repo.get_by_id(conv.user_id)
            user_name = user.name.value if user else "Usuário não encontrado"
            user_phone = user.phone.value if user else "N/A"
            
            response_conversations.append(ConversationResponse(
                id=str(conv.id),
                user_id=str(conv.user_id),
                user_name=user_name,
                user_phone=user_phone,
                status=conv.status.value,
                created_at=conv.created_at.isoformat(),
                updated_at=conv.updated_at.isoformat(),
                last_message_at=conv.last_message_at.isoformat() if conv.last_message_at else None,
                message_count=0,  # TODO: Implementar contagem real
                unread_count=0  # TODO: Implementar contagem real
            ))
        
        return response_conversations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar conversas: {str(e)}"
        )

@router.get("/stats", response_model=ConversationStatsResponse)
async def get_conversation_stats(
    conversation_repo: ConversationRepositoryImpl = Depends(get_conversation_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém estatísticas das conversas"""
    try:
        conversations = conversation_repo.get_all()
        total_conversations = len(conversations)
        
        active_conversations = len([c for c in conversations if c.status.value == "active"])
        closed_conversations = len([c for c in conversations if c.status.value == "closed"])
        pending_conversations = len([c for c in conversations if c.status.value == "pending"])
        
        return ConversationStatsResponse(
            total_conversations=total_conversations,
            active_conversations=active_conversations,
            closed_conversations=closed_conversations,
            pending_conversations=pending_conversations,
            total_messages=0  # TODO: Implementar contagem real
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar estatísticas: {str(e)}"
        )

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    conversation_repo: ConversationRepositoryImpl = Depends(get_conversation_repository),
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém uma conversa específica"""
    try:
        conversation = conversation_repo.get_by_id(UUID(conversation_id))
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversa não encontrada"
            )
        
        user = user_repo.get_by_id(conversation.user_id)
        user_name = user.name.value if user else "Usuário não encontrado"
        user_phone = user.phone.value if user else "N/A"
        
        return ConversationResponse(
            id=str(conversation.id),
            user_id=str(conversation.user_id),
            user_name=user_name,
            user_phone=user_phone,
            status=conversation.status.value,
            created_at=conversation.created_at.isoformat(),
            updated_at=conversation.updated_at.isoformat(),
            last_message_at=conversation.last_message_at.isoformat() if conversation.last_message_at else None,
            message_count=0,  # TODO: Implementar contagem real
            unread_count=0  # TODO: Implementar contagem real
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de conversa inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar conversa: {str(e)}"
        )

@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    conversation_data: ConversationCreateRequest,
    conversation_repo: ConversationRepositoryImpl = Depends(get_conversation_repository),
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Cria uma nova conversa"""
    try:
        # Verificar se usuário existe
        user = user_repo.get_by_id(UUID(conversation_data.user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Criar conversa
        conversation = Conversation(
            user_id=user.id,
            status=ConversationStatus.PENDING
        )
        
        created_conversation = conversation_repo.add(conversation)
        
        return ConversationResponse(
            id=str(created_conversation.id),
            user_id=str(created_conversation.user_id),
            user_name=user.name.value,
            user_phone=user.phone.value,
            status=created_conversation.status.value,
            created_at=created_conversation.created_at.isoformat(),
            updated_at=created_conversation.updated_at.isoformat(),
            last_message_at=created_conversation.last_message_at.isoformat() if created_conversation.last_message_at else None,
            message_count=0,
            unread_count=0
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de usuário inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar conversa: {str(e)}"
        )

@router.put("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: str,
    conversation_data: ConversationUpdateRequest,
    conversation_repo: ConversationRepositoryImpl = Depends(get_conversation_repository),
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Atualiza uma conversa"""
    try:
        conversation = conversation_repo.get_by_id(UUID(conversation_id))
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversa não encontrada"
            )
        
        # Atualizar status se fornecido
        if conversation_data.status:
            conversation.status = ConversationStatus(conversation_data.status)
        
        updated_conversation = conversation_repo.update(conversation)
        
        user = user_repo.get_by_id(updated_conversation.user_id)
        user_name = user.name.value if user else "Usuário não encontrado"
        user_phone = user.phone.value if user else "N/A"
        
        return ConversationResponse(
            id=str(updated_conversation.id),
            user_id=str(updated_conversation.user_id),
            user_name=user_name,
            user_phone=user_phone,
            status=updated_conversation.status.value,
            created_at=updated_conversation.created_at.isoformat(),
            updated_at=updated_conversation.updated_at.isoformat(),
            last_message_at=updated_conversation.last_message_at.isoformat() if updated_conversation.last_message_at else None,
            message_count=0,
            unread_count=0
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de conversa inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar conversa: {str(e)}"
        )

@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    conversation_repo: ConversationRepositoryImpl = Depends(get_conversation_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Deleta uma conversa"""
    try:
        conversation = conversation_repo.get_by_id(UUID(conversation_id))
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversa não encontrada"
            )
        
        conversation_repo.delete(conversation.id)
        return {"message": "Conversa deletada com sucesso"}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de conversa inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar conversa: {str(e)}"
        )
