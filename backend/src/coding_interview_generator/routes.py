from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import ChallengeRequest
from .service import ChallengeService
from .utils import generate_challenge_with_ai
from backend.src.databases.main import get_db_session
from backend.src.auth.dependencies import AccessTokenBearer
from backend.src.auth.service import UserService
from backend.src.databases.models import User
import json
from datetime import datetime


challenge_router = APIRouter()
challenge_service = ChallengeService()


@challenge_router.post("/generate-challenge")
async def generate_challenge(
    request: ChallengeRequest, 
    token_data: dict = Depends(AccessTokenBearer()),
    db: AsyncSession = Depends(get_db_session)
    ):
    try:
        user: User = UserService().get_user_by_email(token_data['emaiil'], session=db)
        user_id = user.model_dump()['uid']
        

        quota = challenge_service.get_challenge_quota(db, user_id)
        if not quota:
            quota = challenge_service.create_challenge_quota(db, user_id)

        quota = challenge_service.reset_quota_if_needed(db, quota)

        if quota.quota_remaining <= 0:
            raise HTTPException(status_code=429, detail="Quota exhausted")

        challenge_data = generate_challenge_with_ai(request.difficulty)

        new_challenge = challenge_service.create_challenge(
            db=db,
            difficulty=request.difficulty,
            created_by=user_id,
            title=challenge_data["title"],
            options=json.dumps(challenge_data["options"]),
            correct_answer_id=challenge_data["correct_answer_id"],
            explanation=challenge_data["explanation"]
        )

        quota.quota_remaining -= 1
        db.commit()

        return {
            "id": new_challenge.id,
            "difficulty": request.difficulty,
            "title": new_challenge.title,
            "options": json.loads(new_challenge.options),
            "correct_answer_id": new_challenge.correct_answer_id,
            "explanation": new_challenge.explanation,
            "timestamp": new_challenge.date_created.isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@challenge_router.get("/my-history")
async def my_history(
    token_data: dict = Depends(AccessTokenBearer), 
    db: AsyncSession = Depends(get_db_session)
    ):
    user: User = UserService().get_user_by_email(token_data['email'], session=db)
    user_id = user.model_dump()['uid']

    challenges = challenge_service.get_user_challenges(db, user_id)
    return {"challenges": challenges}


@challenge_router.get("/quota")
async def get_quota(token_data: dict = Depends(AccessTokenBearer),
                     db: AsyncSession = Depends(get_db_session)
                     ):
    
    user: User = UserService().get_user_by_email(token_data['emaiil'], session=db)
    user_id = user.model_dump()['uid']
    quota = challenge_service.get_challenge_quota(db, user_id)
    if not quota:
        return {
            "user_id": user_id,
            "quota_remaining": 0,
            "last_reset_date": datetime.now()
        }

    quota = challenge_service.reset_quota_if_needed(db, quota)
    return quota