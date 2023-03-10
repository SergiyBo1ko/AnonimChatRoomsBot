from aiogram import types, Dispatcher
from handlers.teacher import *
from keyboards.teacher_kb import *
import config
from create_bot import bot
from database.sqlite_db import check_student_id_exist
# from data_base import sqlite_db
from keyboards.admin_kb import button_case_admin
from keyboards.student_kb import button_case_student
from keyboards.teacher_kb import button_main_menu_teacher


# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    print(message.chat.id)
    await message.delete()
    # print(message.chat.id)
    user_id = message.from_user.id

    if message.from_user.id == config.ADMIN:
        await bot.send_message(message.from_user.id, "Привіт, адміністратор, що бажаєте зробити? 🧐\n",
                               reply_markup=button_case_admin)

    check1 = await check_student_id_exist(user_id)
    if check1 == 1:
        await bot.send_message(message.from_user.id, "Привіт, студенте 🙋", reply_markup=button_case_student)
    if check1 == 2:
        await bot.send_message(message.from_user.id, "Привіт, вчителю, це головне меню! 👨‍🏫", reply_markup=button_main_menu_teacher)
        #await bot.send_message(message.from_user.id, "Привіт, вчителю 👨‍🏫", reply_markup=button_case_student)

    if check1 != 1 and check1 != 2 and message.from_user.id != config.ADMIN:
        await bot.send_message(message.from_user.id, f"Привіт, {message.from_user.first_name} 👋\n"
                                                     f"Бачу тебе тут вперше, після того, як натиснеш на кнопку, ти станеш зареєстрованим 😉",
                               reply_markup=button_case_student)

        # await message.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    # dp.register_message_handler(cancel_handler, state='*',commands='відміна')
    # dp.register_message_handler(cancel_handler,Text(equals='відміна',ignore_case=True),state="*")
