from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def admin_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
    ])

async def admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Управление пользователями", callback_data="user_management")],
        [InlineKeyboardButton(text="📚 Управление дисциплинами", callback_data="discipline_management")],
        [InlineKeyboardButton(text="👥👥 Управление очередями", callback_data="queue_management")],
    ])
    

async def user_management_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚫 Забанить негодяя", callback_data="ban_badguy"),
        InlineKeyboardButton(text="✅ Разбанить негодяя", callback_data="unban_badguy")],
        [InlineKeyboardButton(text="🧾 Получить список", callback_data="list_users")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")],
    ])

async def discipline_management_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить дисциплину", callback_data="add_discipline"),
        InlineKeyboardButton(text="➖ Удалить дисциплину", callback_data="remove_discipline")],
        [InlineKeyboardButton(text="〰️ Переименовать дисциплину", callback_data="rename_discipline")],
        [InlineKeyboardButton(text="📚 Все дисциплины", callback_data="list_disciplines")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")],
    ])
    
    
async def queue_management_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить в конец", callback_data="add_in_queue"),
        InlineKeyboardButton(text="➖ Выгнать из очереди", callback_data="kick_from_queue")],
    ])