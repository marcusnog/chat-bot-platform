"""
Use Cases para mensagens
"""
from typing import List, Optional
from uuid import UUID

from ...domain.entities.message import Message
from ...domain.entities.conversation import Conversation
from ...domain.repositories.message_repository import MessageRepository
from ...domain.repositories.conversation_repository import ConversationRepository
from ...domain.repositories.user_repository import UserRepository
from ...domain.services.message_processing_service import MessageProcessingService
from ...domain.value_objects.message_content import MessageContent, MessageType, MessageDirection
from ..dtos.message_dto import (
    CreateMessageDTO, 
    SendMessageDTO, 
    MessageResponseDTO, 
    MessageListDTO,
    ProcessMessageDTO
)


class CreateMessageUseCase:
    """
    Use Case para criar uma nova mensagem
    """
    
    def __init__(self, message_repository: MessageRepository):
        self._message_repository = message_repository
    
    async def execute(self, dto: CreateMessageDTO) -> MessageResponseDTO:
        """Executa a criação de mensagem"""
        # Cria o conteúdo da mensagem
        content = MessageContent(
            text=dto.content,
            message_type=MessageType(dto.message_type),
            direction=MessageDirection(dto.direction),
            metadata=dto.metadata
        )
        
        # Cria a mensagem
        message = Message.create_new(
            conversation_id=dto.conversation_id,
            user_id=dto.user_id,
            whatsapp_message_id=dto.whatsapp_message_id,
            content=content
        )
        
        # Salva no repositório
        saved_message = await self._message_repository.save(message)
        
        return MessageResponseDTO.from_entity(saved_message)


class ProcessIncomingMessageUseCase:
    """
    Use Case para processar mensagem recebida
    """
    
    def __init__(
        self,
        message_repository: MessageRepository,
        conversation_repository: ConversationRepository,
        user_repository: UserRepository,
        message_processing_service: MessageProcessingService
    ):
        self._message_repository = message_repository
        self._conversation_repository = conversation_repository
        self._user_repository = user_repository
        self._message_processing_service = message_processing_service
    
    async def execute(self, dto: CreateMessageDTO) -> ProcessMessageDTO:
        """Executa o processamento de mensagem recebida"""
        # Busca a mensagem
        message = await self._message_repository.find_by_whatsapp_id(dto.whatsapp_message_id)
        if not message:
            raise ValueError("Mensagem não encontrada")
        
        # Busca a conversa
        conversation = await self._conversation_repository.find_by_id(message.conversation_id)
        if not conversation:
            raise ValueError("Conversa não encontrada")
        
        # Busca histórico de mensagens
        message_history = await self._message_repository.find_by_conversation_id(
            conversation.id, limit=10
        )
        
        # Analisa sentimento e intenção
        sentiment = await self._message_processing_service.analyze_sentiment(message.content.text)
        intent = await self._message_processing_service.extract_intent(message.content.text)
        
        # Verifica se deve escalar
        should_escalate = await self._message_processing_service.should_escalate_to_human(
            message, conversation, message_history
        )
        
        # Gera resposta com IA se não escalar
        ai_response = None
        if not should_escalate:
            ai_response = await self._message_processing_service.generate_ai_response(
                message, conversation, message_history
            )
        
        # Marca como processada
        message.mark_as_processed()
        await self._message_repository.save(message)
        
        return ProcessMessageDTO(
            message_id=message.id,
            should_escalate=should_escalate,
            ai_response=ai_response,
            sentiment=sentiment,
            intent=intent
        )


class SendMessageUseCase:
    """
    Use Case para enviar mensagem
    """
    
    def __init__(
        self,
        message_repository: MessageRepository,
        conversation_repository: ConversationRepository,
        user_repository: UserRepository
    ):
        self._message_repository = message_repository
        self._conversation_repository = conversation_repository
        self._user_repository = user_repository
    
    async def execute(self, dto: SendMessageDTO) -> MessageResponseDTO:
        """Executa o envio de mensagem"""
        from ...domain.value_objects.phone_number import PhoneNumber
        
        # Busca ou cria usuário
        phone_number = PhoneNumber(dto.phone_number)
        user = await self._user_repository.find_by_phone_number(phone_number)
        
        if not user:
            from ...domain.entities.user import User
            user = User.create_new(
                phone_number=phone_number,
                name=f"Usuário {phone_number.to_display_format()}"
            )
            user = await self._user_repository.save(user)
        
        # Busca ou cria conversa ativa
        conversation = await self._conversation_repository.find_active_by_user_id(user.id)
        
        if not conversation:
            conversation = Conversation.create_new(
                user_id=user.id,
                whatsapp_conversation_id=f"{phone_number.to_whatsapp_format()}_{int(datetime.utcnow().timestamp())}"
            )
            conversation = await self._conversation_repository.save(conversation)
        
        # Cria mensagem de saída
        content = MessageContent(
            text=dto.message,
            message_type=MessageType(dto.message_type),
            direction=MessageDirection.OUTGOING
        )
        
        message = Message.create_new(
            conversation_id=conversation.id,
            user_id=user.id,
            whatsapp_message_id=f"outgoing_{int(datetime.utcnow().timestamp())}",
            content=content
        )
        
        # Salva mensagem
        saved_message = await self._message_repository.save(message)
        
        return MessageResponseDTO.from_entity(saved_message)


class GetMessagesByConversationUseCase:
    """
    Use Case para obter mensagens de uma conversa
    """
    
    def __init__(self, message_repository: MessageRepository):
        self._message_repository = message_repository
    
    async def execute(
        self, 
        conversation_id: UUID, 
        skip: int = 0, 
        limit: int = 50
    ) -> MessageListDTO:
        """Executa a busca de mensagens por conversa"""
        messages = await self._message_repository.find_by_conversation_id(
            conversation_id, skip=skip, limit=limit
        )
        
        message_dtos = [MessageResponseDTO.from_entity(message) for message in messages]
        
        return MessageListDTO(
            messages=message_dtos,
            total=len(message_dtos),
            skip=skip,
            limit=limit
        )


class GetUnprocessedMessagesUseCase:
    """
    Use Case para obter mensagens não processadas
    """
    
    def __init__(self, message_repository: MessageRepository):
        self._message_repository = message_repository
    
    async def execute(self) -> List[MessageResponseDTO]:
        """Executa a busca de mensagens não processadas"""
        messages = await self._message_repository.find_unprocessed_messages()
        
        return [MessageResponseDTO.from_entity(message) for message in messages]
