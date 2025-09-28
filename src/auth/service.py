
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.databases.models import User
from .schemas import SignupRequest
from .utils import hash_password

class UserService:

    async def get_user_by_email(self, email: str, session: AsyncSession,) -> User:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)

        return result.first()
    
    async def get_user_by_user_name(self, user_name: str, session: AsyncSession,) -> User:
        statement = select(User).where(User.user_name == user_name)
        result = await session.exec(statement)
        return result.first()
    
    async def user_exist(self, email: str, user_name: str, session: AsyncSession) -> bool:
        user_by_email = await self.get_user_by_email(email, session)
        user_by_name = await self.get_user_by_user_name(user_name, session)

        return (user_by_email is not None) or (user_by_name is not None)

    async def create_user(self, request: SignupRequest, session: AsyncSession) -> User:
        user = request.model_dump()
        new_user = User(
            **user,
        )

        # hash the password.
        print(user['password'])
        new_user.hashed_password = hash_password(user['password'])
        session.add(new_user)
        await session.commit()

        return new_user
    
    async def update_user(self, user: User, user_data: dict, session: AsyncSession)-> User:
        for k, v in user_data.items():
            setattr(user, k, v)

        await session.commit()

        return user