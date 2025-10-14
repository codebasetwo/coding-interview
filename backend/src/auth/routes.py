from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from .dependencies import (AccessTokenBearer, 
                           RefreshTokenBearer,
                           get_current_user,
                           RoleChecker)
from .schemas import (SignupRequest, 
                      SigninRequest, 
                      PasswordResetConfirmModel, 
                      PasswordResetRequestModel)
from .service import UserService
from .utils import (create_url_safe_token,
                    create_refresh_token,
                    create_access_token,
                    decode_url_safe_token,
                    hash_password,
                    verify_password)

from backend.src.databases.main import get_db_session
from backend.src.databases.models import User
from backend.src.databases.redis import add_jti_to_blocklist
from backend.src.celery_tasks import send_email_task
from backend.src.config import Config
from backend.src.errors import UserAlreadyExists, UserNotFound, InvalidToken
from backend.src.utils.mail import (email_verification_message,
                            password_message_template
                            )


auth_router = APIRouter()

user_service = UserService()

@auth_router.post("/signup")
async def create_account(request: SignupRequest, 
                         session: AsyncSession = Depends(get_db_session)
                         ) -> JSONResponse:
    
    email = request.email
    user_name = request.user_name

    user_exist = await user_service.user_exist(email, user_name, session)
    print(user_exist)
    if user_exist:
        raise UserAlreadyExists()
    
    _ = await user_service.create_user(request, session)
    token = create_url_safe_token({"email": email})
    url = f"{Config.VERIFICATION_LINK}/{token}"
    verification_message = email_verification_message.format(
        full_name=request.full_name,
        verification_link=url
    )
    send_email_task.delay("VERIFY YOUR ACCOUNT", [email], body=verification_message)

    return JSONResponse(
        content={
            "user": request.first_name,
            "message": "Account created check your email to verify",
            },
        status_code=status.HTTP_201_CREATED    
    )


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, 
                              session: AsyncSession = Depends(get_db_session)
                              ) -> JSONResponse:
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        user = await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={
                "message": "Account verified successfully",
                "user": user.full_name,
                },
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.post("/signin")
async def login(request: SigninRequest, 
                session: AsyncSession = Depends(get_db_session)

                ) -> JSONResponse:
    email = request.email
    password = request.password

    user = await user_service.get_user_by_email(email, session)
    if user:
        is_valid_passwd = verify_password(password, user.hashed_password)
        if is_valid_passwd:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),

                }
            )

            refresh_token = create_refresh_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid)
                },
              )

            return JSONResponse(
                content={
                    "message": "Login Successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Invalid email or password")


@auth_router.get("/logout")
async def logout(token_details: dict = Depends(AccessTokenBearer())) -> JSONResponse:

    jti = token_details["jti"]
    await add_jti_to_blocklist(jti, token_details["exp"])

    return JSONResponse(
        content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
    )



@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel) -> JSONResponse:
    email = email_data.email

    token = create_url_safe_token({"email": email})
    message = password_message_template.format(url=f"{Config.PASSWORD_RESET_VERIFICATION_LINK}/{token}")

    subject = "Reset Your Password"

    send_email_task.delay(subject, [email], message)
    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password",
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/confirm-password-request/{token}")
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    new_password = passwords.new_password
    confirm_password = passwords.confirm_new_password

    if new_password != confirm_password:
        raise HTTPException(
            detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
        )

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        passwd_hash = hash_password(new_password)
        await user_service.update_user(user, {"hashed_password": passwd_hash}, session)

        return JSONResponse(
            content={"message": "Password reset Successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during password reset."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())) -> JSONResponse:
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        email = token_details.get('user')
        uid = token_details.get('sub')
        new_access_token = create_access_token(user_data={'email': email, 'user_uid': uid})

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()


@auth_router.get("/me")
async def get_current_user(
    user: User = Depends(get_current_user),
    _: bool = Depends(RoleChecker(['user', 'admin'])) 
) -> User:
    return user
    

@auth_router.delete('/close-account')
async def delete_user(
    user: User = Depends(get_current_user),
    _: bool = Depends(RoleChecker(['user', 'admin'])),
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    """Delete the current user's account and revoke the current access token.

    The access token's JTI is added to the Redis blocklist so the token cannot
    be reused. The user record is then removed from the database.
    """
    # Revoke the current access token
    jti = token_details.get("jti")
    exp = token_details.get("exp")

    if jti:
        await add_jti_to_blocklist(jti, exp)

    # Delete the user from the database
    await user_service.delete_user(user, session)

    return JSONResponse(
        content={"message": "Account closed and access token revoked."},
        status_code=status.HTTP_200_OK,
    )
