"""
Schemas Pydantic para usuários
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class CreateUserRequest(BaseModel):
    """Schema para criação de usuário"""
    phone_number: str = Field(..., description="Número de telefone do WhatsApp")
    name: str = Field(..., min_length=1, max_length=100, description="Nome do usuário")
    email: Optional[EmailStr] = Field(None, description="Email do usuário")


class UpdateUserRequest(BaseModel):
    """Schema para atualização de usuário"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nome do usuário")
    email: Optional[EmailStr] = Field(None, description="Email do usuário")
    is_active: Optional[bool] = Field(None, description="Status ativo/inativo")


class UserResponse(BaseModel):
    """Schema de resposta para usuário"""
    id: UUID
    phone_number: str
    name: str
    email: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema de resposta para lista de usuários"""
    users: list[UserResponse]
    total: int
    skip: int
    limit: int
