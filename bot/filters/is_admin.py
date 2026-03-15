from aiogram.filters import BaseFilter
from aiogram import types

from config import settings

class IsAdmin(BaseFilter):
    
    def __init__(self):
        super().__init__()
        self.ADMINS = settings.ADMINS
    
    async def __call__(self, message: types.Message):
        return message.from_user.id in self.ADMINS