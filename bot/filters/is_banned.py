from aiogram import types
from aiogram.filters import BaseFilter
from core.crud import blacklist_crud

from config import session_factory

class IsBanned(BaseFilter):
    async def __call__(self, message: types.Message):
        async with session_factory() as session:
            user = await blacklist_crud.get(message.from_user.id, session)
            return True if user else False