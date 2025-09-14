"""
Controller para mensagens
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from ...application.use_cases.message_use_cases import (
    CreateMessageUseCase,
    ProcessIncomingMessageUseCase,
    SendMessageUseCase,
    GetMessagesByConversationUseCase,
    GetUnprocessedMessagesUseCase
)
from ...application.dtos.message_dto import (
    CreateMessageDTO,
    SendMessageDTO
)
from ..schemas.message_schemas import (
    CreateMessageRequest,
    SendMessageRequest,
    MessageResponse,
    MessageListResponse,
    ProcessMessageResponse
)
from ..dependencies import (
    get_message_repository,
    get_conversation_repository,
    get_user_repository,
    get_message_processing_service
)

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    request: CreateMessageRequest,
    message_repository = Depends(get_message_repository)
):
    """Cria uma nova mensagem"""
    try:
        dto = CreateMessageDTO(
            conversation_id=request.conversation_id,
            user_id=request.user_id,
            whatsapp_message_id=request.whatsapp_message_id,
            content=request.content,
            message_type=request.message_type,
            direction=request.direction,
            metadata=request.metadata
        )
        
        use_case = CreateMessageUseCase(message_repository)
        result = await use_case.execute(dto)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno")


@router.post("/send", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    request: SendMessageRequest,
    message_repository = Depends(get_message_repository),
    conversation_repository = Depends(get_conversation_repository),
    user_repository = Depends(get_user_repository)
):
    """Envia uma mensagem via WhatsApp"""
    try:
        dto = SendMessageDTO(
            phone_number=request.phone_number,
            message=request.message,
            message_type=request.message_type
        )
        
        use_case = SendMessageUseCase(
            message_repository,
            conversation_repository,
            user_repository
        )
        result = await use_case.execute(dto)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno")


@router.post("/process/{message_id}", response_model=ProcessMessageResponse)
async def process_message(
    message_id: UUID,
    message_repository = Depends(get_message_repository),
    conversation_repository = Depends(get_conversation_repository),
    user_repository = Depends(get_user_repository),
    message_processing_service = Depends(get_message_processing_service)
):
    """Processa uma mensagem recebida"""
    try:
        # Busca a mensagem
        message = await message_repository.find_by_id(message_id)
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensagem não encontrada")
        
        # Cria DTO para processamento
        dto = CreateMessageDTO(
            conversation_id=message.conversation_id,
            user_id=message.user_id,
            whatsapp_message_id=message.whatsapp_message_id,
            content=message.content.text,
            message_type=message.content.message_type.value,
            direction=message.content.direction.value,
            metadata=message.content.metadata
        )
        
        use_case = ProcessIncomingMessageUseCase(
            message_repository,
            conversation_repository,
            user_repository,
            message_processing_service
        )
        result = await use_case.execute(dto)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno")


@router.get("/conversation/{conversation_id}", response_model=MessageListResponse)
async def get_messages_by_conversation(
    conversation_id: UUID,
    skip: int = 0,
    limit: int = 50,
    message_repository = Depends(get_message_repository)
):
    """Lista mensagens de uma conversa"""
    use_case = GetMessagesByConversationUseCase(message_repository)
    result = await use_case.execute(conversation_id, skip=skip, limit=limit)
    
    return result


@router.get("/unprocessed", response_model=List[MessageResponse])
async def get_unprocessed_messages(
    message_repository = Depends(get_message_repository)
):
    """Lista mensagens não processadas"""
    use_case = GetUnprocessedMessagesUseCase(message_repository)
    result = await use_case.execute()
    
    return result
