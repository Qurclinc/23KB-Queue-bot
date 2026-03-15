from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Записаться в очередь", callback_data="sign_in"),
        InlineKeyboardButton(text="Выйти из очереди", callback_data="sign_out")], 
        [InlineKeyboardButton(text="Посмотреть очереди", callback_data="view_queues")], 
        [InlineKeyboardButton(text="Я сдал", callback_data="i_passed")],
        [InlineKeyboardButton(text="Изменить подпись", callback_data="change_sign")], 
    ])
    
async def back_keyboard(callback: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data=callback)]
    ])
    
async def do_enqueue_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔚 Занять конец очереди", callback_data="get_last"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="user_back")]
    ])