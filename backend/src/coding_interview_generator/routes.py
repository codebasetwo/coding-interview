from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request
from sqlmodel.ext.asyncio.session import AsyncSession


from ..ai_generator import generate_challenge_with_ai
from .schemas import ChallengeRequest
from .service import ChallengeService
from ..utils import authenticate_and_get_user_details
from src.databases.main import get_db_session
import json
from datetime import datetime


router = APIRouter()
challenge_service = ChallengeService()



@router.post("/generate-challenge")
async def generate_challenge(
    request: ChallengeRequest, 
    request_obj: Request, 
    db: AsyncSession = Depends(get_db_session)
    ):
    try:
        user_details = authenticate_and_get_user_details(request_obj)
        user_id = user_details.get("user_id")

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


@router.get("/my-history")
async def my_history(request: Request, db: AsyncSession = Depends(get_db_session)):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    challenges = challenge_service.get_user_challenges(db, user_id)
    return {"challenges": challenges}


@router.get("/quota")
async def get_quota(request: Request, db: AsyncSession = Depends(get_db_session)):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    quota = challenge_service.get_challenge_quota(db, user_id)
    if not quota:
        return {
            "user_id": user_id,
            "quota_remaining": 0,
            "last_reset_date": datetime.now()
        }

    quota = challenge_service.reset_quota_if_needed(db, quota)
    return quota