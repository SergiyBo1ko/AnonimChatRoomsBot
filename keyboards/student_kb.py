from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

# кнопки учня

choose_rooms_st = InlineKeyboardButton(text='📌 Ввійти до кімнати 📌',callback_data='choose_rooms_for_student')

button_case_student = InlineKeyboardMarkup(resize_keyboard=True).add(choose_rooms_st)
