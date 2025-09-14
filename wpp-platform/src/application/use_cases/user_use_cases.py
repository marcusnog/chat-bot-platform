"""
Use Cases para usuários
"""
from typing import List, Optional
from uuid import UUID

from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from ...domain.value_objects.phone_number import PhoneNumber
from ..dtos.user_dto import CreateUserDTO, UpdateUserDTO, UserResponseDTO, UserListDTO


class CreateUserUseCase:
    """
    Use Case para criar um novo usuário
    """
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, dto: CreateUserDTO) -> UserResponseDTO:
        """Executa a criação de usuário"""
        # Valida se usuário já existe
        phone_number = PhoneNumber(dto.phone_number)
        
        existing_user = await self._user_repository.find_by_phone_number(phone_number)
        if existing_user:
            return UserResponseDTO.from_entity(existing_user)
        
        # Cria novo usuário
        user = User.create_new(
            phone_number=phone_number,
            name=dto.name,
            email=dto.email
        )
        
        # Salva no repositório
        saved_user = await self._user_repository.save(user)
        
        return UserResponseDTO.from_entity(saved_user)


class GetUserUseCase:
    """
    Use Case para obter usuário por ID
    """
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, user_id: UUID) -> Optional[UserResponseDTO]:
        """Executa a busca de usuário"""
        user = await self._user_repository.find_by_id(user_id)
        
        if not user:
            return None
        
        return UserResponseDTO.from_entity(user)


class GetUserByPhoneUseCase:
    """
    Use Case para obter usuário por número de telefone
    """
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, phone_number: str) -> Optional[UserResponseDTO]:
        """Executa a busca de usuário por telefone"""
        phone = PhoneNumber(phone_number)
        user = await self._user_repository.find_by_phone_number(phone)
        
        if not user:
            return None
        
        return UserResponseDTO.from_entity(user)


class UpdateUserUseCase:
    """
    Use Case para atualizar usuário
    """
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, user_id: UUID, dto: UpdateUserDTO) -> Optional[UserResponseDTO]:
        """Executa a atualização de usuário"""
        user = await self._user_repository.find_by_id(user_id)
        
        if not user:
            return None
        
        # Atualiza campos fornecidos
        if dto.name is not None:
            user.update_name(dto.name)
        
        if dto.email is not None:
            user.update_email(dto.email)
        
        if dto.is_active is not None:
            if dto.is_active:
                user.activate()
            else:
                user.deactivate()
        
        # Salva alterações
        updated_user = await self._user_repository.save(user)
        
        return UserResponseDTO.from_entity(updated_user)


class ListUsersUseCase:
    """
    Use Case para listar usuários
    """
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, skip: int = 0, limit: int = 100) -> UserListDTO:
        """Executa a listagem de usuários"""
        users = await self._user_repository.find_all(skip=skip, limit=limit)
        
        user_dtos = [UserResponseDTO.from_entity(user) for user in users]
        
        return UserListDTO(
            users=user_dtos,
            total=len(user_dtos),
            skip=skip,
            limit=limit
        )


class DeleteUserUseCase:
    """
    Use Case para deletar usuário
    """
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, user_id: UUID) -> bool:
        """Executa a remoção de usuário"""
        return await self._user_repository.delete(user_id)
