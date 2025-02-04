from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboard as kb
import app.yt_script as yt

class StateMachine(StatesGroup):
    btn_clicked = State()


router = Router(name = "main_router")


#/start
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(StateMachine.btn_clicked)

    await message.answer(
    f"""Hello, {message.from_user.full_name}!
Choose option from keyboard below.""", reply_markup=kb.keyboard_main)


#/name
@router.message(lambda message: message.text.lower() == '/name')
async def cmd_name(message: Message, state: FSMContext) -> None:
    await state.update_data(btn_clicked = "Name")

    await message.answer("Cool, send me name of song.", reply_markup=ReplyKeyboardRemove())


#/link
@router.message(lambda message: message.text.lower() == '/link')
async def cmd_link(message: Message, state: FSMContext) -> None:
    await state.update_data(btn_clicked = "Link")

    await message.answer("Cool, send me YT link.", reply_markup=ReplyKeyboardRemove())


#/credits
@router.message(lambda message: message.text.lower() == '/credits')
async def cmd_link(message: Message, state: FSMContext) -> None:
    await state.update_data(btn_clicked = "Credits")
    await message.answer("Credits: ", reply_markup=kb.keyboard_contact)



#name process
@router.message(lambda message: 'youtube.com' not in message.text.lower())
async def search_install_name(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    if user_data.get("btn_clicked") == "Name":
        await message.answer(f"Searching for '{message.text}'...")


#link process
@router.message(lambda message: 'youtube.com' in message.text.lower())
async def search_install_link(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    if user_data.get("btn_clicked") == "Link":
        await message.answer(f"Searching for LINK '{message.text}'...")


#callback for /credits
@router.callback_query(F.data == 'kb_back')
async def away_from_credits(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(btn_clicked = '_')
    await callback.message.delete()
    await callback.message.answer('Choose option from keyboard below.', reply_markup=kb.keyboard_main)