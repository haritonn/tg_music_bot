from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

keyboard_main = ReplyKeyboardMarkup(keyboard = 
    [
        [KeyboardButton(text = "/credits")],
        [KeyboardButton(text = "/name"), KeyboardButton(text = "/link")]
    ],
        resize_keyboard = True,
        input_field_placeholder = "Choose option from below.")

keyboard_contact = InlineKeyboardMarkup(inline_keyboard = 
    [
        [InlineKeyboardButton(text = "GitHub", url = 'https://github.com/haritonn')],
        [InlineKeyboardButton(text = "Telegram", url= 'https://t.me/hariton_p')],
        [InlineKeyboardButton(text = "Go back", callback_data = "kb_back")]
    ])