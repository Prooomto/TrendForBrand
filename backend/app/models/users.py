from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import JSON

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    BUSINESS = "business"  # владелец бизнеса
    CREATOR = "creator"    # инфлюенсер


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(Enum(UserRole), nullable=False)
    
    # Дополнительные поля для бизнеса
    company_name = Column(String, nullable=True)
    company_description = Column(String, nullable=True)
    
    # Дополнительные поля для креатора
    bio = Column(String, nullable=True)
    social_media_links = Column(JSON, nullable=True)  # JSON строка с ссылками
    
    # Общие поля
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Отношения
    #campaigns = relationship("Campaign", back_populates="owner", foreign_keys="Campaign.owner_id")
    #applications = relationship("Application", back_populates="creator")

    def __repr__(self) -> str:
        return f"<User {self.email}>" 