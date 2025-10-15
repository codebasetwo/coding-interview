import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import ChallengeRequest
from .service import ChallengeService
from .utils import generate_challenge_with_ai
from backend.src.databases.main import get_db_session
from backend.src.auth.dependencies import AccessTokenBearer

challenge_router = APIRouter()
challenge_service = ChallengeService()


@challenge_router.post("/generate-challenge")
async def generate_challenge(
    request: ChallengeRequest, 
    token_data: dict = Depends(AccessTokenBearer()),
    db: AsyncSession = Depends(get_db_session)
    ):
    try:
        user_id = token_data['sub']
        
        quota = await challenge_service.get_challenge_quota(db, user_id)
        if not quota:
            quota = await challenge_service.create_challenge_quota(db, user_id)

        quota = await challenge_service.reset_quota_if_needed(db, quota)

        if quota.quota_remaining <= 0:
            raise HTTPException(status_code=429, detail="Quota exhausted")

        challenge_data = generate_challenge_with_ai(request.difficulty)

        new_challenge = await challenge_service.create_challenge(
            session=db,
            difficulty=request.difficulty,
            created_by=user_id,
            title=challenge_data["question"],
            options=json.dumps(challenge_data["options"]),
            correct_answer_id=challenge_data["correct_answer_id"],
            explanation=challenge_data["explanation"]
        )

        quota.quota_remaining -= 1
        await db.commit()

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
    token_data: dict = Depends(AccessTokenBearer()), 
    db: AsyncSession = Depends(get_db_session)
    ):
    user_id = token_data['sub']

    challenges = await challenge_service.get_user_challenges(db, user_id)
    return {"challenges": challenges}


@challenge_router.get("/quota")
async def get_quota(token_data: dict = Depends(AccessTokenBearer()),
                     db: AsyncSession = Depends(get_db_session)
                     ):
    
    user_id = token_data['sub']
    quota = await challenge_service.get_challenge_quota(db, user_id)
    if not quota:
        return {
            "user_id": user_id,
            "quota_remaining": 0,
            "last_reset_date": datetime.now()
        }

    quota = await challenge_service.reset_quota_if_needed(db, quota)
    return quota