from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.models import Discipline, Queue
from core.schemas import DisciplineCreate, DisciplineUpdate

async def create_discipline(
    discipline_create: DisciplineCreate,
    session: AsyncSession
):
    try:
        discipline = Discipline(**discipline_create.model_dump())
        session.add(discipline)
        await session.commit()
        await session.refresh(discipline)
        return discipline
    except IntegrityError:
        return None

async def get_discipline(
    id: int, session: AsyncSession
):
    result = await session.execute(
        select(Discipline)
        .where(Discipline.id == id)
        .options(
            selectinload(Discipline.queue)
            .selectinload(Queue.student),
            selectinload(Discipline.queue)
            .selectinload(Queue.discipline)
        )
    )
    return result.scalar_one_or_none()

async def get_all(session: AsyncSession) -> List[Discipline]:
    result = await session.execute(select(Discipline))
    return result.scalars().all()

async def update_discipline(
    discipline_update: DisciplineUpdate,
    session: AsyncSession
):
    discipline = await get_discipline(discipline_update.id, session)
    if discipline:
        for name, value in discipline_update.model_dump(exclude_unset=True).items():
            if name == "id":
                continue
            setattr(discipline, name, value)
        await session.commit()
        await session.refresh(discipline)
    
    return discipline
    

async def delete_discipline(
    id: int,
    session: AsyncSession
):
    discipline = await get_discipline(id, session)
    if discipline:
        await session.delete(discipline)
        await session.commit()
        return True
    return False