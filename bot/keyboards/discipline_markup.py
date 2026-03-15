from typing import List, Literal
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.models import Discipline

async def disciplines_keyboard(
    prefix: str,
    disciplines: List[Discipline],
    callback: Literal["user_back", "admin_back"] = "user_back"
):
    builder = InlineKeyboardBuilder()
    for discipline in disciplines:
        button = InlineKeyboardButton(
            text=discipline.name,
            callback_data=f"{prefix}_discipline_{discipline.id}"
        )
        builder.add(button)
    builder.adjust(3)
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data=callback))
    return builder.as_markup()