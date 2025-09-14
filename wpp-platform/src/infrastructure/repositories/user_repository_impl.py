"""
Implementação do repositório de usuários
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from ...domain.value_objects.phone_number import PhoneNumber
from ..database.models import UserModel


class UserRepositoryImpl(UserRepository):
    """
    Implementação do repositório de usuários usando SQLAlchemy
    """
    
    def __init__(self, db_session: Session):
        self._db = db_session
    
    async def save(self, user: User) -> User:
        """Salva um usuário"""
        if user.id:
            # Atualização
            db_user = await self._get_by_id(user.id)
            if db_user:
                db_user.name = user.name
                db_user.email = user.email
                db_user.is_active = user.is_active
                db_user.updated_at = user.updated_at
            else:
                raise ValueError("Usuário não encontrado")
        else:
            # Criação
            db_user = UserModel(
                phone_number=str(user.phone_number),
                name=user.name,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            self._db.add(db_user)
        
        self._db.commit()
        self._db.refresh(db_user)
        
        return self._to_entity(db_user)
    
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Busca usuário por ID"""
        db_user = await self._get_by_id(user_id)
        return self._to_entity(db_user) if db_user else None
    
    async def find_by_phone_number(self, phone_number: PhoneNumber) -> Optional[User]:
        """Busca usuário por número de telefone"""
        db_user = self._db.query(UserModel).filter(
            UserModel.phone_number == str(phone_number)
        ).first()
        
        return self._to_entity(db_user) if db_user else None
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Lista todos os usuários"""
        db_users = self._db.query(UserModel).offset(skip).limit(limit).all()
        return [self._to_entity(db_user) for db_user in db_users]
    
    async def find_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Lista usuários ativos"""
        db_users = self._db.query(UserModel).filter(
            UserModel.is_active == True
        ).offset(skip).limit(limit).all()
        
        return [self._to_entity(db_user) for db_user in db_users]
    
    async def delete(self, user_id: UUID) -> bool:
        """Remove um usuário"""
        db_user = await self._get_by_id(user_id)
        if db_user:
            self._db.delete(db_user)
            self._db.commit()
            return True
        return False
    
    async def exists_by_phone_number(self, phone_number: PhoneNumber) -> bool:
        """Verifica se usuário existe pelo número de telefone"""
        count = self._db.query(UserModel).filter(
            UserModel.phone_number == str(phone_number)
        ).count()
        return count > 0
    
    async def _get_by_id(self, user_id: UUID) -> Optional[UserModel]:
        """Busca usuário por ID no banco"""
        return self._db.query(UserModel).filter(UserModel.id == user_id).first()
    
    def _to_entity(self, db_user: UserModel) -> User:
        """Converte modelo do banco para entidade do domínio"""
        return User(
            id=db_user.id,
            phone_number=PhoneNumber(db_user.phone_number),
            name=db_user.name,
            email=db_user.email,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
