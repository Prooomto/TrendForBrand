from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from app.models.users import UserRole


# Базовые схемы
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    full_name: Optional[str] = Field(None, max_length=100)
    role: UserRole


# Схема для создания пользователя
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    
    # Дополнительные поля для бизнеса
    company_name: Optional[str] = Field(None, max_length=200)
    company_description: Optional[str] = Field(None, max_length=1000)
    
    # Дополнительные поля для креатора
    bio: Optional[str] = Field(None, max_length=500)
    social_media_links: Optional[Dict[str, str]] = None
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов')
        if not any(c.isupper() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not any(c.islower() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        if not any(c.isdigit() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v
    
    @field_validator('social_media_links')
    @classmethod
    def validate_social_media_links(cls, v):
        if v is not None:
            allowed_platforms = ['instagram', 'tiktok', 'youtube', 'twitter', 'facebook']
            for platform, link in v.items():
                if platform not in allowed_platforms:
                    raise ValueError(f'Неподдерживаемая платформа: {platform}')
                if not link.startswith(('http://', 'https://')):
                    raise ValueError(f'Ссылка должна начинаться с http:// или https://')
        return v


# Схема для обновления пользователя
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    full_name: Optional[str] = Field(None, max_length=100)
    
    # Дополнительные поля для бизнеса
    company_name: Optional[str] = Field(None, max_length=200)
    company_description: Optional[str] = Field(None, max_length=1000)
    
    # Дополнительные поля для креатора
    bio: Optional[str] = Field(None, max_length=500)
    social_media_links: Optional[Dict[str, str]] = None
    
    @field_validator('social_media_links')
    @classmethod
    def validate_social_media_links(cls, v):
        if v is not None:
            allowed_platforms = ['instagram', 'tiktok', 'youtube', 'twitter', 'facebook']
            for platform, link in v.items():
                if platform not in allowed_platforms:
                    raise ValueError(f'Неподдерживаемая платформа: {platform}')
                if not link.startswith(('http://', 'https://')):
                    raise ValueError(f'Ссылка должна начинаться с http:// или https://')
        return v


# Схема для смены пароля
class UserChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        """Проверка сложности нового пароля"""
        if len(v) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов')
        if not any(c.isupper() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not any(c.islower() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        if not any(c.isdigit() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v


# Схема для ответа (без пароля)
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    # Дополнительные поля для бизнеса
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    
    # Дополнительные поля для креатора
    bio: Optional[str] = None
    social_media_links: Optional[Dict[str, str]] = None


# Схема для списка пользователей (сокращенная информация)
class UserListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: EmailStr
    username: str
    full_name: Optional[str]
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    # Дополнительные поля в зависимости от роли
    company_name: Optional[str] = None
    bio: Optional[str] = None


# Схема для аутентификации
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Схема для токена
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # время жизни токена в секундах


# Схема для данных токена
class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[UserRole] = None


# Схема для верификации email
class EmailVerification(BaseModel):
    email: EmailStr
    verification_code: str = Field(..., min_length=6, max_length=6)


# Схема для сброса пароля
class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    email: EmailStr
    reset_code: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        """Проверка сложности нового пароля"""
        if len(v) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов')
        if not any(c.isupper() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not any(c.islower() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        if not any(c.isdigit() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v 