from typing import NoReturn

from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.requests import Request
from sqlmodel.ext.asyncio.session import AsyncSession

from .utils import decode_tokens
from .service import UserService
from src.databases.main import get_db_session
from src.databases.models import User
from src.errors import (
    InvalidToken, 
    RefreshTokenRequired, 
    AccessTokenRequired, 
    RevokedToken,
    InsufficientPermission,
    AccountNotVerified)
from src.databases.redis import token_in_blocklist


class TokenBearer(HTTPBearer):
    def __init__(self, *, bearerFormat = None, scheme_name = None, description = None, auto_error = True):
        super().__init__(bearerFormat=bearerFormat, scheme_name=scheme_name, description=description, auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials
        print(token)
        token_data_with_bool = self.token_valid(token)
        token_data = token_data_with_bool["token_data"]

        if not token_data_with_bool["is_token"]:
            raise InvalidToken()
        
        if await token_in_blocklist(token_data["jti"]):
            raise RevokedToken()

        self.verify_token_data(token_data)

        return token_data
    
    def token_valid(self, token: str) -> dict:
        token_data = decode_tokens(token)
        is_token = token_data is not None
        print(token_data, is_token)

        return {
            "token_data": token_data,
            "is_token": is_token,
        }

    def verify_token_data(self, token_data) -> NoReturn:
        raise NotImplementedError("Please Override this method in child classes")
    

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data) -> NoReturn:
        if token_data and token_data["type"] == "refresh":
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data) -> NoReturn:
        if token_data and token_data["type"] == "access":
            raise RefreshTokenRequired()


async def get_current_user(
        token_deta: TokenBearer = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db_session)
) -> User:
    
    user = await UserService().get_user_by_email(token_deta['user'], session=session)

    return user
    


class RoleChecker:
    def __init__(self, allowed_roles: list[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> bool:
        if not current_user.is_verified:
            raise AccountNotVerified()
        if current_user.role in self.allowed_roles:
            return True

        raise InsufficientPermission()