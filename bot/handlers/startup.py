from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import types, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from bot.filters.is_registered import IsRegistered
from bot.filters.is_banned import IsBanned
from bot.states import Register
from bot.keyboards import main_keyboard as main_kb
from core.crud import student_crud
from core.schemas import StudentCreate

router = Router()

@router.message(~IsRegistered(), CommandStart())
async def start_reg(message: types.Message, state: FSMContext):
    text = (
        "Введите ваше имя, которое будет отображаться в очереди.\n\n"
        "(<b>Настоятельно рекомендую</b> использовать <i>настоящие имена</i>, в противном случае могу <u>снести аккаунт</u>)"
    )
    await message.answer(text=text, parse_mode="HTML")
    await state.set_state(Register.username)
    
@router.message(Register.username)
async def fetch_username(message: types.Message, state: FSMContext, session: AsyncSession):
    username = message.text
    user_id = message.from_user.id
    usertag = message.from_user.username
    student_create = StudentCreate(
        user_id=user_id,
        usertag=usertag[:32],
        username=username
    )
    res = await student_crud.create_student(student_create, session)
    if res:
        await message.answer("✅ Успешно зарегистрированы")
        student = await student_crud.get_student(message.from_user.id, session)
        await message.answer(
            f"Имя: `{student.username}`",
            parse_mode="Markdown",
            reply_markup=await main_kb()
        )
    else:
        await message.answer("❌ Не удалось зарегистрироваться")
    await state.clear()
    
    
@router.message(~IsBanned(), IsRegistered(), CommandStart())
async def start_reg(message: types.Message, session: AsyncSession):
    student = await student_crud.get_student(message.from_user.id, session)
    await message.answer(
        f"Имя: `{student.username}`",
        parse_mode="Markdown",
        reply_markup=await main_kb()
    )
    
@router.message(IsBanned())
async def ban_message(message: types.Message):
    await message.answer("Забанен, откисай.\nЕсли думаешь, что это ошибка - свяжись с админами.")