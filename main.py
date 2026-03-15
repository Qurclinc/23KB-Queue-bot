import asyncio
from aiogram import Dispatcher

from bot.handlers import reg_router, admin_router, user_router
from config import bot, session_factory
from bot.middleware.database_middleware import DatabaseMiddleware

database_middleware = DatabaseMiddleware(session_factory=session_factory)


async def main():
    dp = Dispatcher()
    dp.message.middleware(database_middleware)
    dp.callback_query.middleware(database_middleware)
    dp.include_routers(reg_router, admin_router, user_router)
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())