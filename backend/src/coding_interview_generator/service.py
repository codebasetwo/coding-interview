from datetime import datetime, timedelta

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.src.databases.models import ChallengeQuota, Challenge


class ChallengeService:
    async def get_challenge_quota(session: AsyncSession, user_id: str) -> ChallengeQuota:
        statement = (select(ChallengeQuota)
                     .where(ChallengeQuota.user_id == user_id)
                     )
        result = await session.exec(statement)
        return result.first()


    async def create_challenge_quota(session: AsyncSession, user_id: str)-> ChallengeQuota:
        db_quota = ChallengeQuota(user_id=user_id)
        session.add(db_quota)
        await session.commit()
        return db_quota


    async def reset_quota_if_needed(session: AsyncSession, quota: ChallengeQuota) -> ChallengeQuota:
        now = datetime.now()
        if now - quota.last_reset_date > timedelta(hours=24):
            quota.quota_remaining = 10
            quota.last_reset_date = now
            await session.commit()
        return quota


    async def create_challenge(
        session: AsyncSession,
        difficulty: str,
        created_by: str,
        title: str,
        options: str,
        correct_answer_id: int,
        explanation: str
    ) -> Challenge:
        db_challenge = Challenge(
            difficulty=difficulty,
            created_by=created_by,
            title=title,
            options=options,
            correct_answer_id=correct_answer_id,
            explanation=explanation
        )
        session.add(db_challenge)
        await session.commit()
        return db_challenge


    async def get_user_challenges(session: AsyncSession, user_id: str) -> Challenge:
        statement = (select(Challenge)
                     .where(Challenge.created_by == user_id)
                     )
        result = await session.exec(statement)
        return result.all()