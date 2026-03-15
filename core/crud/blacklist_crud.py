from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Blacklist

async def get(
    user_id: int,
    session: AsyncSession
):
    badguy = await session.execute(select(Blacklist).where(Blacklist.user_id == user_id))
    return badguy.scalar_one_or_none()

async def ban(
    user_id: int,
    session: AsyncSession
):
    try:
        user = Blacklist(user_id=user_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return True
    except IntegrityError:
        await session.rollback()
        return False
    except Exception as e:
        await session.rollback()
        print(f"Error in ban: {e}")
        return False
    
async def unban(
    user_id: int,
    session: AsyncSession
):
    user = await get(user_id, session)
    try:
        await session.delete(user)
        await session.commit()
        return True
    except Exception:
        return False