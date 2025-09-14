"""
Endpoints de analytics
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from uuid import UUID

from src.infrastructure.database.database import get_db
from src.infrastructure.database.auth_models import AuthUser
from src.presentation.controllers.auth_controller import get_current_user
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.repositories.conversation_repository_impl import ConversationRepositoryImpl
from src.infrastructure.repositories.message_repository_impl import MessageRepositoryImpl

router = APIRouter(prefix="/analytics", tags=["analytics"])

# Schemas
class AnalyticsOverviewResponse(BaseModel):
    total_users: int
    active_users: int
    total_conversations: int
    active_conversations: int
    total_messages: int
    messages_today: int
    response_time_avg: float
    satisfaction_score: float

class MessageTrendResponse(BaseModel):
    date: str
    inbound_messages: int
    outbound_messages: int
    total_messages: int

class UserActivityResponse(BaseModel):
    date: str
    new_users: int
    active_users: int
    returning_users: int

class ConversationMetricsResponse(BaseModel):
    total_conversations: int
    active_conversations: int
    closed_conversations: int
    pending_conversations: int
    avg_conversation_duration: float
    avg_messages_per_conversation: float

class ResponseTimeResponse(BaseModel):
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    response_time_percentiles: dict

# Dependências
def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    return UserRepositoryImpl(db)

def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepositoryImpl:
    return ConversationRepositoryImpl(db)

def get_message_repository(db: Session = Depends(get_db)) -> MessageRepositoryImpl:
    return MessageRepositoryImpl(db)

# Endpoints
@router.get("/overview", response_model=AnalyticsOverviewResponse)
async def get_analytics_overview(
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    conversation_repo: ConversationRepositoryImpl = Depends(get_conversation_repository),
    message_repo: MessageRepositoryImpl = Depends(get_message_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém visão geral das métricas"""
    try:
        # Buscar dados básicos
        users = user_repo.get_all()
        conversations = conversation_repo.get_all()
        messages = message_repo.get_all()
        
        # Calcular métricas
        total_users = len(users)
        active_users = len([u for u in users if u.is_active])
        total_conversations = len(conversations)
        active_conversations = len([c for c in conversations if c.status.value == "active"])
        total_messages = len(messages)
        
        # Mensagens de hoje
        today = datetime.now().date()
        messages_today = len([m for m in messages if m.timestamp.date() == today])
        
        # Métricas calculadas (mockadas por enquanto)
        response_time_avg = 2.5  # minutos
        satisfaction_score = 4.2  # de 5
        
        return AnalyticsOverviewResponse(
            total_users=total_users,
            active_users=active_users,
            total_conversations=total_conversations,
            active_conversations=active_conversations,
            total_messages=total_messages,
            messages_today=messages_today,
            response_time_avg=response_time_avg,
            satisfaction_score=satisfaction_score
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar métricas: {str(e)}"
        )

@router.get("/message-trends", response_model=List[MessageTrendResponse])
async def get_message_trends(
    days: int = Query(7, ge=1, le=30),
    message_repo: MessageRepositoryImpl = Depends(get_message_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém tendências de mensagens por período"""
    try:
        messages = message_repo.get_all()
        
        # Agrupar mensagens por data
        trends = {}
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        
        # Inicializar todas as datas no período
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.isoformat()
            trends[date_str] = {
                'inbound_messages': 0,
                'outbound_messages': 0,
                'total_messages': 0
            }
            current_date += timedelta(days=1)
        
        # Contar mensagens por data
        for message in messages:
            message_date = message.timestamp.date()
            if start_date <= message_date <= end_date:
                date_str = message_date.isoformat()
                if date_str in trends:
                    if message.direction.value == "inbound":
                        trends[date_str]['inbound_messages'] += 1
                    else:
                        trends[date_str]['outbound_messages'] += 1
                    trends[date_str]['total_messages'] += 1
        
        # Converter para lista ordenada
        result = []
        for date_str in sorted(trends.keys()):
            result.append(MessageTrendResponse(
                date=date_str,
                inbound_messages=trends[date_str]['inbound_messages'],
                outbound_messages=trends[date_str]['outbound_messages'],
                total_messages=trends[date_str]['total_messages']
            ))
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar tendências: {str(e)}"
        )

@router.get("/user-activity", response_model=List[UserActivityResponse])
async def get_user_activity(
    days: int = Query(7, ge=1, le=30),
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém atividade dos usuários por período"""
    try:
        users = user_repo.get_all()
        
        # Agrupar usuários por data de criação
        activity = {}
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        
        # Inicializar todas as datas no período
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.isoformat()
            activity[date_str] = {
                'new_users': 0,
                'active_users': 0,
                'returning_users': 0
            }
            current_date += timedelta(days=1)
        
        # Contar usuários por data
        for user in users:
            user_date = user.created_at.date()
            if start_date <= user_date <= end_date:
                date_str = user_date.isoformat()
                if date_str in activity:
                    activity[date_str]['new_users'] += 1
            
            # Usuários ativos (mockado por enquanto)
            if user.is_active:
                # Simular atividade recente
                activity_date = (datetime.now() - timedelta(days=1)).date()
                if start_date <= activity_date <= end_date:
                    date_str = activity_date.isoformat()
                    if date_str in activity:
                        activity[date_str]['active_users'] += 1
        
        # Converter para lista ordenada
        result = []
        for date_str in sorted(activity.keys()):
            result.append(UserActivityResponse(
                date=date_str,
                new_users=activity[date_str]['new_users'],
                active_users=activity[date_str]['active_users'],
                returning_users=activity[date_str]['returning_users']
            ))
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar atividade: {str(e)}"
        )

@router.get("/conversation-metrics", response_model=ConversationMetricsResponse)
async def get_conversation_metrics(
    conversation_repo: ConversationRepositoryImpl = Depends(get_conversation_repository),
    message_repo: MessageRepositoryImpl = Depends(get_message_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém métricas das conversas"""
    try:
        conversations = conversation_repo.get_all()
        messages = message_repo.get_all()
        
        total_conversations = len(conversations)
        active_conversations = len([c for c in conversations if c.status.value == "active"])
        closed_conversations = len([c for c in conversations if c.status.value == "closed"])
        pending_conversations = len([c for c in conversations if c.status.value == "pending"])
        
        # Calcular métricas (mockadas por enquanto)
        avg_conversation_duration = 15.5  # minutos
        avg_messages_per_conversation = total_messages / total_conversations if total_conversations > 0 else 0
        
        return ConversationMetricsResponse(
            total_conversations=total_conversations,
            active_conversations=active_conversations,
            closed_conversations=closed_conversations,
            pending_conversations=pending_conversations,
            avg_conversation_duration=avg_conversation_duration,
            avg_messages_per_conversation=avg_messages_per_conversation
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar métricas: {str(e)}"
        )

@router.get("/response-times", response_model=ResponseTimeResponse)
async def get_response_times(
    message_repo: MessageRepositoryImpl = Depends(get_message_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém métricas de tempo de resposta"""
    try:
        # Por enquanto, retornar dados mockados
        # TODO: Implementar cálculo real de tempo de resposta
        
        return ResponseTimeResponse(
            avg_response_time=2.5,
            min_response_time=0.5,
            max_response_time=15.0,
            response_time_percentiles={
                "p50": 2.0,
                "p75": 3.5,
                "p90": 5.0,
                "p95": 7.0,
                "p99": 12.0
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar tempos de resposta: {str(e)}"
        )
