from datetime import datetime, timedelta, timezone
from uuid import uuid4


import jwt
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer

from backend.src.config import Config

MAX_BCRYPT_BYTES = 72
password_context = CryptContext(
    schemes=['bcrypt'],
    deprecated = "auto"
)

serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRETE, salt="email-configuration"
)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_access_token(user_data: dict) -> str:
    now = datetime.now(tz=timezone.utc)
    pay_load = {
        "user": user_data["email"],
        'sub': user_data["user_uid"],
        'jti': str(uuid4()),
        'type': 'access',
        'iat': now,
        'exp': now + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    return jwt.encode(
        payload=pay_load,
        key = Config.JWT_SECRETE,
        algorithm=Config.JWT_ALGORITHM
        )

def create_refresh_token(user_data: dict) -> str:
    now = datetime.now(tz=timezone.utc)
    pay_load = {
        'user': user_data['email'],
        'sub': user_data["user_uid"],
        'jti': str(uuid4()),
        'type': 'refresh',
        'iat': now,
        'exp': now + timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DAYS)
    }

    return  jwt.encode(
        payload=pay_load,
        key = Config.JWT_SECRETE,
        algorithm=Config.JWT_ALGORITHM
        )


def decode_tokens(token: str) -> dict|None:
    try:
        return jwt.decode(
            jwt = token,
            key = Config.JWT_SECRETE,
            algorithms = [Config.JWT_ALGORITHM,],
        )

    except jwt.PyJWTError as jwte:
        print(f'error occured: {jwte}')
        return None

    except Exception as e:
        print(f'error occured:{e}')
        return None

def create_url_safe_token(data: dict) -> str:
    token = serializer.dumps(data)

    return token

def decode_url_safe_token(token: str) -> dict:
    try:
        token_data = serializer.loads(token)

        return token_data
    
    except Exception as e:
        print(e)
