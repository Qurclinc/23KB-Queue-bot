from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from bot.states import Change
from bot.keyboards import (
    main_keyboard as main_kb,
    back_keyboard as back_kb,
    disciplines_keyboard as disciplines_kb,
    do_enqueue_keyboard as enqueue_kb
)
from core.crud import student_crud, discipline_crud, queue_crud
from core.schemas import StudentUpdate
from core.models import Discipline, Queue

router = Router()

@router.callback_query(F.data == "user_back")
async def start_menu(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    student = await student_crud.get_student(callback.from_user.id, session)
    await callback.message.edit_text(
        f"Имя: `{student.username}`",
        parse_mode="Markdown",
        reply_markup=await main_kb()
    )
    await state.clear()

@router.callback_query(F.data == "change_sign")
async def change_sign(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    text = (
        "Введите ваше имя, которое будет отображаться в очереди.\n\n"
        "(<b>Настоятельно рекомендую</b> использовать <i>настоящие имена</i>, в противном случае могу <u>снести аккаунт</u>)"
    )
    await callback.message.edit_text(text=text, parse_mode="HTML", reply_markup=await back_kb("user_back"))
    await state.set_state(Change.username)
    
@router.message(Change.username)
async def read_sign(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    res = await student_crud.update_student(StudentUpdate(
        user_id=message.from_user.id,
        usertag=message.from_user.username,
        username=message.text
    ), session)
    if res:
        await message.answer("✅ Успешно изменено", reply_markup=await main_kb())
    else:
        await message.answer("❌ Не удалось изменить имя", reply_markup=await main_kb())
    await state.clear()
    

# Enqueue
@router.callback_query(F.data == "sign_in")
async def sign_in_step_1(
    callback: types.CallbackQuery,
    session: AsyncSession
):
    disciplines: List[Discipline] = await discipline_crud.get_all(session)
    await callback.message.edit_text(
        text="Выберите дисципилну:",
        reply_markup=await disciplines_kb(prefix="enqueue", disciplines=disciplines)
    )
    
@router.callback_query(F.data.startswith("enqueue_discipline"))
async def sign_in_step_2(
    callback: types.CallbackQuery,
    session: AsyncSession
):
    id = int(callback.data.split("_")[-1])
    student = await student_crud.get_student(callback.from_user.id, session)
    discipline = await discipline_crud.get_discipline(id, session)
    
    try:
        res = await queue_crud.enqueue(student.id, discipline.id, session)
    except KeyError:
        await callback.message.edit_text(
            text="❌ Не удалось встать в очередь: Вы <b>уже</b> стоите в очереди!",
            parse_mode="HTML",
            reply_markup=await back_kb("user_back"))
    if res:
        await callback.message.edit_text("✅ Вы успешно встали в очередь", reply_markup=await back_kb("user_back"))
    else:
        await callback.message.edit_text("❌ Не удалось встать в очередь", reply_markup=await back_kb("user_back"))
        
# View queues
@router.callback_query(F.data == "view_queues")
async def view_queues_list(
    callback: types.CallbackQuery,
    session: AsyncSession
):
    disciplines: List[Discipline] = await discipline_crud.get_all(session)
    await callback.message.edit_text(
        text="Выберите дисципилну:",
        reply_markup=await disciplines_kb(prefix="view_queue", disciplines=disciplines)
    )
    
@router.callback_query(F.data.startswith("view_queue"))
async def view_queue_for_discipline(
    callback: types.CallbackQuery,
    session: AsyncSession
):
    id = int(callback.data.split("_")[-1])
    discipline = await discipline_crud.get_discipline(id, session)
    # queue_entries: List[Queue] = await queue_crud.get_queue_by_discipline(discipline.id, session)
    queue_entries: List[Queue] = discipline.queue
    
    members = []
    for i, entry in enumerate(queue_entries):
        student = entry.student
        line = f"{i + 1}. {student.username.strip()}" + (f"(@{student.usertag.strip()})" if student.usertag else "")
        if student.user_id == callback.from_user.id:
            line = "<b><u>" + line + "</u></b>"
        members.append(line)
    
    await callback.message.edit_text(
        text=f"Очередь на <u>{discipline.name}</u>:\n\n{'\n'.join(members)}",
        parse_mode="HTML",
        reply_markup=await back_kb("user_back")
    )
    
    
# Leave queue (Dequeue)
@router.callback_query(F.data == "sign_out")
@router.callback_query(F.data == "i_passed")
async def dequeue(
    callback: types.CallbackQuery,
    session: AsyncSession
):
    student = await student_crud.get_student(callback.from_user.id, session)
    queues: List[Queue] = student.queue
    prefix = "dequeue" if callback.data == "sign_out" else "passed"
    await callback.message.edit_text(
        text="Выберите дисципилну:",
        reply_markup=await disciplines_kb(prefix=prefix, disciplines=[q.discipline for q in queues])
    )
    
@router.callback_query(F.data.startswith("sign_out"))
async def sign_out(
    callback: types.CallbackQuery,
    session: AsyncSession
):
    id = int(callback.data.split("_")[2])
    res = await discipline_crud.delete_discipline(id, session)
    if res:
        await callback.message.edit_text("✅ Вы успешно вышли из очереди", reply_markup=await back_kb("user_back"))
    else:
        await callback.message.edit_text("❌ Не удалось выйти из очереди", reply_markup=await back_kb("user_back"))

@router.callback_query(F.data.startswith("passed"))
async def passed_step_1(
    callback: types.CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    id = int(callback.data.split("_")[2])
    student = await student_crud.get_student(callback.from_user.id, session)
    await state.set_data({"student_id": student.id, "discipline_id": id})
    
    res = await queue_crud.dequeue(student.id, id, session)
    if res:
        await callback.message.edit_text("✅ Вы успешно вышли из очереди", reply_markup=await enqueue_kb())
    else:
        await callback.message.edit_text("❌ Не удалось выйти из очереди", reply_markup=await enqueue_kb())
        
@router.callback_query(F.data == "get_last")
async def get_last(
    callback: types.CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    data = await state.get_data()
    res = await queue_crud.enqueue(
        data.get("student_id"),
        data.get("discipline_id"),
        session
    )
    
    if res:
        await callback.message.edit_text("✅ Вы снова в конце очереди", reply_markup=await back_kb("user_back"))
    else:
        await callback.message.edit_text("❌ Не удалось встать в конец очереди", reply_markup=await back_kb("user_back"))
    await state.clear()