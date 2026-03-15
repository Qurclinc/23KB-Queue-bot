from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.models import Student, Queue
from core.schemas import StudentCreate, StudentUpdate

async def create_student(
    student_create: StudentCreate,
    session: AsyncSession
):
    try:
        student = Student(**student_create.model_dump())
        session.add(student)
        await session.commit()
        await session.refresh(student)
        return student
    except IntegrityError:
        return None

async def get_student(
    user_id: int, session: AsyncSession
):
    result = await session.execute(
        select(Student)
        .where(Student.user_id == user_id)
        .options(
            selectinload(Student.queue)
            .selectinload(Queue.discipline)
        )
    )
    return result.scalar_one_or_none()

async def get_student_by_id(
    id: int, session: AsyncSession
):
    result = await session.execute(select(Student).where(Student.id == id))
    return result.scalar_one_or_none()

async def get_all(session: AsyncSession) -> List[Student]:
    result = await session.execute(select(Student))
    return result.scalars().all()

async def update_student(
    student_update: StudentUpdate,
    session: AsyncSession
):
    student = await get_student(student_update.user_id, session)
    if student:
        for name, value in student_update.model_dump(exclude_unset=True).items():
            setattr(student, name, value)
        await session.commit()
        await session.refresh(student)
    
    return student
    

async def delete_student(
    user_id: int,
    session: AsyncSession
):
    student = await get_student(user_id, session)
    if student:
        await session.delete(student)
        await session.commit()
        return True
    return False