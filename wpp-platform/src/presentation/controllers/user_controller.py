"""
Controller para usuários
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    GetUserByPhoneUseCase,
    UpdateUserUseCase,
    ListUsersUseCase,
    DeleteUserUseCase
)
from src.application.dtos.user_dto import CreateUserDTO, UpdateUserDTO
from src.presentation.schemas.user_schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
    UserListResponse
)
from src.presentation.dependencies import get_user_repository

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    user_repository = Depends(get_user_repository)
):
    """Cria um novo usuário"""
    try:
        dto = CreateUserDTO(
            phone_number=request.phone_number,
            name=request.name,
            email=request.email
        )
        
        use_case = CreateUserUseCase(user_repository)
        result = await use_case.execute(dto)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    user_repository = Depends(get_user_repository)
):
    """Obtém um usuário por ID"""
    use_case = GetUserUseCase(user_repository)
    result = await use_case.execute(user_id)
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    return result


@router.get("/phone/{phone_number}", response_model=UserResponse)
async def get_user_by_phone(
    phone_number: str,
    user_repository = Depends(get_user_repository)
):
    """Obtém um usuário por número de telefone"""
    use_case = GetUserByPhoneUseCase(user_repository)
    result = await use_case.execute(phone_number)
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    return result


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
    user_repository = Depends(get_user_repository)
):
    """Atualiza um usuário"""
    try:
        dto = UpdateUserDTO(
            name=request.name,
            email=request.email,
            is_active=request.is_active
        )
        
        use_case = UpdateUserUseCase(user_repository)
        result = await use_case.execute(user_id, dto)
        
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno")


@router.get("/", response_model=UserListResponse)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    user_repository = Depends(get_user_repository)
):
    """Lista usuários"""
    use_case = ListUsersUseCase(user_repository)
    result = await use_case.execute(skip=skip, limit=limit)
    
    return result


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    user_repository = Depends(get_user_repository)
):
    """Remove um usuário"""
    use_case = DeleteUserUseCase(user_repository)
    success = await use_case.execute(user_id)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
