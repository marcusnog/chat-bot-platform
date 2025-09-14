"""
Endpoints de usuários
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from src.infrastructure.database.database import get_db
from src.infrastructure.database.auth_models import AuthUser
from src.presentation.controllers.auth_controller import get_current_user
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.domain.entities.user import User
from src.domain.value_objects.phone_number import PhoneNumber
from src.domain.value_objects.user_name import UserName
from src.domain.value_objects.email import Email
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])

# Schemas
class UserResponse(BaseModel):
    id: str
    name: str
    phone: str
    email: str
    is_active: bool
    created_at: str
    updated_at: str
    last_activity: Optional[str] = None
    conversation_count: int = 0
    total_messages: int = 0

class UserCreateRequest(BaseModel):
    name: str
    phone: str
    email: EmailStr

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserStatsResponse(BaseModel):
    total_users: int
    active_users: int
    total_conversations: int
    total_messages: int

# Dependências
def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    return UserRepositoryImpl(db)

# Endpoints
@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Lista todos os usuários com filtros"""
    try:
        users = user_repo.get_all(skip=skip, limit=limit)
        
        # Aplicar filtros
        if search:
            users = [u for u in users if 
                    search.lower() in u.name.value.lower() or 
                    search in u.phone.value or 
                    search.lower() in u.email.value.lower()]
        
        if is_active is not None:
            users = [u for u in users if u.is_active == is_active]
        
        # Converter para response
        return [
            UserResponse(
                id=str(user.id),
                name=user.name.value,
                phone=user.phone.value,
                email=user.email.value,
                is_active=user.is_active,
                created_at=user.created_at.isoformat(),
                updated_at=user.updated_at.isoformat(),
                last_activity=user.last_activity.isoformat() if user.last_activity else None,
                conversation_count=0,  # TODO: Implementar contagem real
                total_messages=0  # TODO: Implementar contagem real
            )
            for user in users
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar usuários: {str(e)}"
        )

@router.get("/stats", response_model=UserStatsResponse)
async def get_user_stats(
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém estatísticas dos usuários"""
    try:
        users = user_repo.get_all()
        total_users = len(users)
        active_users = len([u for u in users if u.is_active])
        
        return UserStatsResponse(
            total_users=total_users,
            active_users=active_users,
            total_conversations=0,  # TODO: Implementar contagem real
            total_messages=0  # TODO: Implementar contagem real
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar estatísticas: {str(e)}"
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém um usuário específico"""
    try:
        user = user_repo.get_by_id(UUID(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return UserResponse(
            id=str(user.id),
            name=user.name.value,
            phone=user.phone.value,
            email=user.email.value,
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
            last_activity=user.last_activity.isoformat() if user.last_activity else None,
            conversation_count=0,  # TODO: Implementar contagem real
            total_messages=0  # TODO: Implementar contagem real
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de usuário inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar usuário: {str(e)}"
        )

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreateRequest,
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Cria um novo usuário"""
    try:
        # Criar entidade de domínio
        user = User(
            name=UserName(user_data.name),
            phone=PhoneNumber(user_data.phone),
            email=Email(user_data.email),
            is_active=True
        )
        
        # Salvar no repositório
        created_user = user_repo.add(user)
        
        return UserResponse(
            id=str(created_user.id),
            name=created_user.name.value,
            phone=created_user.phone.value,
            email=created_user.email.value,
            is_active=created_user.is_active,
            created_at=created_user.created_at.isoformat(),
            updated_at=created_user.updated_at.isoformat(),
            last_activity=created_user.last_activity.isoformat() if created_user.last_activity else None,
            conversation_count=0,
            total_messages=0
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar usuário: {str(e)}"
        )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdateRequest,
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Atualiza um usuário"""
    try:
        user = user_repo.get_by_id(UUID(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Atualizar campos fornecidos
        if user_data.name is not None:
            user.name = UserName(user_data.name)
        if user_data.phone is not None:
            user.phone = PhoneNumber(user_data.phone)
        if user_data.email is not None:
            user.email = Email(user_data.email)
        if user_data.is_active is not None:
            user.is_active = user_data.is_active
        
        # Salvar alterações
        updated_user = user_repo.update(user)
        
        return UserResponse(
            id=str(updated_user.id),
            name=updated_user.name.value,
            phone=updated_user.phone.value,
            email=updated_user.email.value,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at.isoformat(),
            updated_at=updated_user.updated_at.isoformat(),
            last_activity=updated_user.last_activity.isoformat() if updated_user.last_activity else None,
            conversation_count=0,
            total_messages=0
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de usuário inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar usuário: {str(e)}"
        )

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    current_user: AuthUser = Depends(get_current_user)
):
    """Deleta um usuário"""
    try:
        user = user_repo.get_by_id(UUID(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        user_repo.delete(user.id)
        return {"message": "Usuário deletado com sucesso"}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de usuário inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar usuário: {str(e)}"
        )
