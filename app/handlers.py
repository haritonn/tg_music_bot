from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import app.keyboard as kb
import app.yt_script as yt

import os 

class StateMachine(StatesGroup):
    btn_clicked = State()


router = Router(name = "main_router")


#/start
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(StateMachine.btn_clicked)

    await message.answer(
    f"""Hello, <em>{message.from_user.full_name}</em>!
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

        try:
            filenames = await yt.install_from_name(message.text)
            builder_results = InlineKeyboardBuilder()
            for i in filenames:
                builder_results.add(InlineKeyboardButton(text = i[1], callback_data= f'install_{i[0][32:]}'))

            kb_results = builder_results.adjust(1).as_markup()

            await message.answer(f"What i found by query {message.text}:", reply_markup = kb_results)

        except Exception as e:
            await message.answer(f"Something went wrong (name/): {e}")


#link process
@router.message(lambda message: 'youtube.com' in message.text.lower())
async def search_install_link(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()

    if user_data.get("btn_clicked") == "Link":
        await message.answer(f"Searching for LINK '{message.text}'...")

        try:
            file_name = await yt.install_from_link(message.text)
            await message.answer_audio(FSInputFile(file_name))

            os.remove(file_name)

        except Exception as e:
            await message.answer('Something went wrong. (link/)')

#callback for /credits
@router.callback_query(F.data == 'kb_back')
async def away_from_credits(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(btn_clicked = '_')
    await callback.message.delete()

    await callback.message.answer('Choose option from keyboard below.', reply_markup=kb.keyboard_main)

#callback for selected /name
@router.callback_query('install_' == F.data[:8])
async def install_selected(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(btn_clicked = '_')

    id = callback.data[:8]
    install_url = f'https://www.youtube.com/watch?v={id}'

    try:
        file_name = await yt.install_from_link(install_url)

        await callback.message.delete()
        await callback.message.answer_audio(FSInputFile(file_name))

        os.remove(file_name)
    except Exception as e:
        await callback.message.answer('Something went wrong (name/installation/)')

    