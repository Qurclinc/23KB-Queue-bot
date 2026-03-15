from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.filters.is_admin import IsAdmin
from bot.states import ReadUID, Discipline
from bot.keyboards import (
    admin_keyboard as admin_kb,
    user_management_keyboard as user_kb,
    discipline_management_keyboard as discipline_kb,
    admin_back_keyboard as back_kb,
    disciplines_keyboard as dis_kb,
    queue_management_keyboard as queue_kb
)
from core.crud import student_crud, discipline_crud, blacklist_crud, queue_crud
from core.schemas import DisciplineCreate, DisciplineUpdate

router = Router()

@router.message(Command("admin"), IsAdmin())
async def show_admin_panel(message: types.Message):
    await message.answer(
        ">👑 Панель администратора 👑",
        parse_mode="MarkdownV2",
        reply_markup=await admin_kb()
    )
    
@router.callback_query(F.data == "admin_back")
async def go_back(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=">👑 Панель администратора 👑",
        parse_mode="MarkdownV2",
        reply_markup=await admin_kb()
    )
    await state.clear()
    
# Users management
# ------------------------------------------------------------------------
@router.callback_query(F.data == "user_management")
async def show_user_management_panel(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=await user_kb())

# Ban    
@router.callback_query(F.data == "ban_badguy")
async def read_id_ban_guy(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Введите ID негодяя:",
        reply_markup=await back_kb()
    )
    await state.set_state(ReadUID.ban)
    
@router.message(ReadUID.ban)
async def ban_guy(message: types.Message, state: FSMContext, session: AsyncSession):
    try:
        user_id = int(message.text)
        res = await blacklist_crud.ban(user_id, session)
        if res:
            await message.answer("✅ Негодяй успешно забанен. :)")
            await student_crud.delete_student(user_id, session)
        else:
            await message.answer("Не удалось забанить негодяя. :с")
        await state.clear()
    except IntegrityError:
        await message.answer("Негодяй уже забанен.")
    except Exception as ex:
        print(str(ex))
        await message.answer("Введеён неверный ID!")
    
# Unban    
@router.callback_query(F.data == "unban_badguy")
async def read_id_ban_guy(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Введите ID негодяя:",
        reply_markup=await back_kb()
    )
    await state.set_state(ReadUID.unban)
    
@router.message(ReadUID.unban)
async def ban_guy(message: types.Message, state: FSMContext, session: AsyncSession):
    try:
        user_id = int(message.text)
        res = await blacklist_crud.unban(user_id, session)
        if res:
            await message.answer("✅ Негодяй успешно разбанен. :)")
        else:
            await message.answer("Не удалось разбанить негодяя. :с")
        await state.clear()
    except IntegrityError:
        await message.answer("Негодяй уже разбанен.")
    except Exception:
        await message.answer("Введеён неверный ID!")
    
@router.callback_query(F.data == "list_users")
async def get_users_list(callback: types.CallbackQuery, session: AsyncSession):
    all_users = await student_crud.get_all(session)
    users_list = []
    for user in all_users:
        line = f"{user.username}" + (f"(@{user.usertag})" if user.usertag else "") + f" - <code>{user.user_id}</code>"
        users_list.append(line)
    await callback.message.edit_text(
        text=f"Пользователи:\n\n{'\n'.join(users_list)}",
        parse_mode="HTML"
    )
    
# Discipline management
# ------------------------------------------------------------------------
@router.callback_query(F.data == "discipline_management")
async def show_discipline_management_panel(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=await discipline_kb())
    
# Add Discipline
@router.callback_query(F.data == "add_discipline")
async def add_discipline(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Введите название дисциплины:",
        reply_markup=await back_kb()
    )
    await state.set_state(Discipline.add)
    
    
@router.message(Discipline.add)
async def read_add_discipline(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    name = message.text
    discipline_create = DisciplineCreate(
        name=name
    )
    res = await discipline_crud.create_discipline(discipline_create, session)
    if res:
        await message.answer("✅ Дисциплина успешно добавлена")
    else:
        await message.answer("❌ Не удалось добавить дисциплину")
    await state.clear()

# Remove Discipline
@router.callback_query(F.data == "remove_discipline")
async def remove_discipline(callback: types.CallbackQuery, session: AsyncSession):
    disciplines: List[Discipline] = await discipline_crud.get_all(session)
    await callback.message.edit_text(
        text="Выберите дисциплину для удаления",
        reply_markup=await dis_kb(prefix="remove", disciplines=disciplines, callback="admin_back")
    )
    
@router.callback_query(F.data.startswith("remove_discipline"))
async def do_remove_discipline(callback: types.CallbackQuery, session: AsyncSession):
    id = callback.data.split("_")[-1]
    res = await discipline_crud.delete_discipline(id, session)
    if res:
        await callback.message.answer("✅ Дисциплина успешно удалена")
    else:
        await callback.message.answer("❌ Не удалось удалить дисциплину")

# Rename Discipline
@router.callback_query(F.data == "rename_discipline")
async def rename_discipline(callback: types.CallbackQuery, session: AsyncSession):
    disciplines: List[Discipline] = await discipline_crud.get_all(session)
    await callback.message.edit_text(
        text="Выберите дисциплину для переименования",
        reply_markup=await dis_kb(prefix="rename", disciplines=disciplines, callback="admin_back")
    )
    
@router.callback_query(F.data.startswith("rename_discipline"))
async def do_rename_discipline(
    callback: types.CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    id = callback.data.split("_")[-1]
    discipline = await discipline_crud.get_discipline(id, session)
    await state.set_data({"id": id})
    await callback.message.edit_text(
        text=(
            f">{discipline.name}\n"
            "Введите новое название"
        ),
        reply_markup=await back_kb(),
        parse_mode="MarkdownV2"
    )
    await state.set_state(Discipline.rename)
    
@router.message(Discipline.rename)
async def read_rename_discipline(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    data = await state.get_data()
    name = message.text
    discipline_update = DisciplineUpdate(
        id=int(data.get("id")),
        name=name
    )
    res = await discipline_crud.update_discipline(discipline_update, session)
    if res:
        await message.answer("✅ Дисциплина успешно обновлена")
    else:
        await message.answer("❌ Не удалось обновить дисциплину")
    await state.clear()
    
# Just view
@router.callback_query(F.data == "list_disciplines")
async def view_list_disciplines(callback: types.CallbackQuery, session: AsyncSession):
    disciplines: List[Discipline] = await discipline_crud.get_all(session)
    await callback.message.edit_text(
        text=">Список дисциплин:",
        parse_mode="MarkdownV2",
        reply_markup=await dis_kb(prefix="", disciplines=disciplines, callback="admin_back")
    )
    
# Queue management
# ------------------------------------------------------------------------
@router.callback_query(F.data == "queue_management")
async def show_user_management_panel(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=await queue_kb())

@router.callback_query(F.data == "add_in_queue")
@router.callback_query(F.data == "kick_from_queue")
async def queues(
    callback: types.CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    disciplines: List[Discipline] = await discipline_crud.get_all(session)
    await state.set_data({"action": callback.data.split("_")[0]})
    await callback.message.edit_text(
        text=">Список дисциплин:",
        parse_mode="MarkdownV2",
        reply_markup=await dis_kb(prefix="queue", disciplines=disciplines, callback="admin_back")
    )
    
@router.callback_query(F.data.startswith("queue_discipline"))
async def read_uid_queue(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    id = int(callback.data.split("_")[-1])
    await callback.message.edit_text(
        "Введите ID пользователя:",
        reply_markup=await back_kb()
    )
    await state.update_data({"discipline_id": id})
    await state.set_state(ReadUID.queue)
    
@router.message(ReadUID.queue)
async def perform_action(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    data = await state.get_data()
    action = data.get("action")
    student = await student_crud.get_student(int(message.text), session)
    discipline_id = data.get("discipline_id")
    try:
        if action == "add":
            res = await queue_crud.enqueue(student.id, discipline_id, session)
        elif action == "kick":
            res = await queue_crud.dequeue(student.id, discipline_id, session)
            
            
        if res:
            await message.answer("✅ Успех.", reply_markup=await back_kb())
        else:
            await message.answer("❌ Не вышло.", reply_markup=await back_kb())
    except Exception as ex:
        print(str(ex))
        await message.answer("❌ Не удалось выполнить действие.", reply_markup=await back_kb())
    
    await state.clear()