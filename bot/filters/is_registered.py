from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import types
from aiogram.filters import BaseFilter
from core.crud import student_crud

from config import session_factory

class IsRegistered(BaseFilter):
    async def __call__(self, message: types.Message):
        async with session_factory() as session:
            user = await student_crud.get_student(message.from_user.id, session)
            return True if user else False