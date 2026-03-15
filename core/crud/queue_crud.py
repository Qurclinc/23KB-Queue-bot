from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Queue

async def get_queue_by_discipline(
    discipline_id: int,
    session: AsyncSession
):
    queue = await session.execute(
        select(Queue)
        .where(Queue.discipline_id == discipline_id)
        .order_by(Queue.added_at)
    )
    return queue.scalars().all()

async def get_entry(
    student_id: int,
    discipline_id: int,
    session: AsyncSession
):
    res = await session.execute(
        select(Queue)
        .where(
            (Queue.student_id == student_id) 
            &
            (Queue.discipline_id == discipline_id)
        )
    )
    return res.scalar_one_or_none()

async def enqueue(
    student_id: int,
    discipline_id: int,
    session: AsyncSession
):
    try:
        entry = await get_entry(student_id, discipline_id, session)
        if entry:
            raise KeyError
        queue = Queue(
            student_id=student_id,
            discipline_id=discipline_id
        )
        session.add(queue)
        await session.commit()
        await session.refresh(queue)
        return True
    except Exception as e:
        await session.rollback()
        print(f"Error in ban: {e}")
        return False
    
async def dequeue(
    student_id: int,
    discipline_id: int,
    session: AsyncSession
):
    
    entry = await get_entry(student_id, discipline_id, session)
    try:
        await session.delete(entry)
        await session.commit()
        return True
    except Exception:
        return False