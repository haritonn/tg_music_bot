from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import app.keyboard as kb
import app.yt_script as yt

import os 


router = Router(name = "main_router")


#/start
@router.message(CommandStart())
async def cmd_start(message: Message) -> None:

    await message.answer(
    f"""Hello, <em>{message.from_user.full_name}</em>!
Choose option from keyboard below.""", reply_markup=kb.keyboard_main)


#/name
@router.message(Command('name'))
async def cmd_name(message: Message, command: CommandObject) -> None:

    await message.answer(f"Searching for '{command.args}'...")

    try:
        filenames = await yt.install_from_name(command.args)
        builder_results = InlineKeyboardBuilder()
        for i in filenames:
            builder_results.add(InlineKeyboardButton(text = f'{i[3]} | {i[2]} - {i[1]}', callback_data= f'install_{i[0][32:]}'))

        kb_results = builder_results.adjust(1).as_markup()

        await message.answer(f"What i found by query {message.text}:", reply_markup = kb_results)

    except Exception as e:
        await message.answer(f"Something went wrong (name/): {e}")


#/link
@router.message(Command('link'))
async def cmd_link(message: Message, command: CommandObject) -> None:

    await message.answer(f"Searching for your link...")

    try:
        file_name = await yt.install_from_link(command.args)
        await message.answer_audio(FSInputFile(file_name))

        os.remove(file_name)

    except Exception as e:
        await message.answer('Something went wrong. (link/)')


#/credits
@router.message(Command('credits'))
async def cmd_link(message: Message) -> None:

    await message.answer("Credits: ", reply_markup=kb.keyboard_contact)




#callback for /credits
@router.callback_query(F.data == 'kb_back')
async def away_from_credits(callback: CallbackQuery) -> None:
    await callback.message.delete()

    await callback.message.answer('Choose option from keyboard below.', reply_markup=kb.keyboard_main)

#callback for selected /name
@router.callback_query('install_' == F.data[:8])
async def install_selected(callback: CallbackQuery) -> None:

    id = callback.data[8:]
    install_url = f'https://www.youtube.com/watch?v={id}'

    try:
        file_name = await yt.install_from_link(install_url)
        await callback.message.answer_audio(FSInputFile(file_name))

        os.remove(file_name)
    except Exception as e:
        await callback.message.answer('Something went wrong (name/installation/)')

    