from typing import Any, Callable

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

class InterviewAppExceptions(Exception):
    """Base exception of all app exceptions."""
    ...

class UserAlreadyExists(InterviewAppExceptions):
    "exception when use already exists."
    ...

class UserNotFound(InterviewAppExceptions):
    """User not found."""
    ...

class InvalidToken(InterviewAppExceptions):
    """error when the provided token is not valid."""
    ...

class RefreshTokenRequired(InterviewAppExceptions):
    """User has provided an access token when a refresh token is needed"""
    ...

class RevokedToken(InterviewAppExceptions):
    """user has provided a token that has been revoked."""
    ...

class AccessTokenRequired(InterviewAppExceptions):
    """User has provided a refresh token when an access token is needed"""
    ...

class AccountNotVerified(InterviewAppExceptions):
    """if User is not verified"""
    ...

class InsufficientPermission(InterviewAppExceptions):
    """ if user is not allowed to access certain endpoints."""
    ...


def create_exception_handler(
        status_code: int,
        details: Any,
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: InterviewAppExceptions)-> JSONResponse:
        return JSONResponse(content=details, status_code=status_code)
    
    return exception_handler


def register_errors(app: FastAPI) -> None:
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            details={"message": "user already exists"},
        )
    )

    app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        details={"message": "user not found",},
        )
    )

    app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        details={
            "message": "Invalid token.",
            "resolution": " Please provide a valid token",
            },
        )
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            details={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account Not verified",
                "error_code": "account_not_verified",
                "resolution":"Please check your email for verification details"
            },
        ),
    )