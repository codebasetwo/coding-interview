
import time
from typing import Optional

import redis.asyncio as aioredis

from backend.src.config import Config

# Default TTL (seconds) to use if no token expiry is provided
JTI_EXPIRY = 3600

token_blocklist = aioredis.from_url(Config.REDIS_URL)


async def add_jti_to_blocklist(jti: str, expires_at: Optional[int] = None) -> None:
    """
    Add a JTI to the Redis blocklist.

    If `expires_at` (unix timestamp) is provided the key TTL will be set to the
    remaining lifetime of the token (expires_at - now). Otherwise the default
    `JTI_EXPIRY` is used.
    """
    ttl = JTI_EXPIRY
    if expires_at is not None:
        remaining = int(expires_at) - int(time.time())
        # If the token already expired, keep a short TTL (1s) so the key will be removed soon.
        if remaining > 0:
            ttl = remaining
        else:
            ttl = 1

    # store a non-empty value so GET/EXISTS behave predictably
    await token_blocklist.set(name=jti, value="", ex=ttl)


async def token_in_blocklist(jti: str) -> bool:
    """Return True if `jti` exists in the blocklist."""
    jti = await token_blocklist.get(jti)
    return jti is not None