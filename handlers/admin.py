from aiogram.dispatcher.filters.state import State,StatesGroup
from telethon.tl import functions
from config import BOT_ACCESS_HASH, BOT_USER_ID
from create_bot import client, dp
from handlers.client import *
from keyboards.admin_kb import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from database.sqlite_db import sql_create_room, sql_show_all_rooms, sql_delete_room, check_which_room,kick_student_from_room,kick_teacher_from_room,check_teacher_or_student_kick,sql_show_enter_teacher_code_rooms,get_teacher_user_id,\
get_enter_teacher_code_using_room_number,get_enter_student_code_using_room_number,get_student_user_id,get_room_status,update_enter_teacher_code,update_enter_student_code,get_chat_id,check_room_exist
from aiogram.dispatcher.filters import Text





from telethon.sync import TelegramClient

from telethon.tl import types as tele_types

import random

data = []
#await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)        # видалення для колбека



class FSMAdmin(StatesGroup):
    teacher = State()
    student = State()
    delete_room = State()
    kick_from_room = State()





#Кнопка всі кімнати
@dp.callback_query_handler(text = ['all_rooms'])
async def show_allyryr_rooms(call: types.CallbackQuery):

    rooms = await sql_show_all_rooms()
    codes = await sql_show_enter_teacher_code_rooms()
    await bot.send_message(call.from_user.id, text='👾---------------- Існуючі кімнати ----------------👾')
    for room in rooms:
        #await bot.send_message(call.from_user.id, text='---------------- Існуючі кімнати ----------------')  # БД для кімнат
        #await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

        tmp1 = await get_enter_teacher_code_using_room_number(room[0])
        tmp2 = await get_enter_student_code_using_room_number(room[0])
        tmp3 = await get_teacher_user_id(room[0])
        tmp4 = await get_student_user_id(room[0])
        tmp5 = await get_room_status(room[0])
        tmp6 = await get_chat_id(room[0])



        await bot.send_message(call.from_user.id ,text = f'Кімната: <code>{ room[0]}</code> \n'
                                                         f'ID Вчителя: <code>{ tmp3 }</code>\n'
                                                         f'ID Учня: <code>{ tmp4 }</code>\n'
                                                         f'Код допуску вчителя: <code>{ tmp1}</code>\n'
                                                         f'Код допуску учня:  <code>{ tmp2}</code>\n'
                                                         f'Статус кімнати: {tmp5}\n'
                                                         f'Чат-id із повідомленнями: <code>{tmp6}</code>')  #БД для кімнат
    await bot.send_message(call.from_user.id, text='👾-------------------------------------------------------------👾')









# Створення кімнати
@dp.callback_query_handler(text = ['create_room'])
async def createe_rooms(call: types.CallbackQuery):
    #await FSMAdmin.teacher.set()
    room_number = random.randint(100, 10000)
    enter_code_for_teacher = random.randint(100000, 100000000)
    enter_code_for_student = random.randint(100000, 100000000)
    await bot.send_message(call.from_user.id,text = f'✔️ Кімната створена успішно.\n#️⃣ Номер кімнати: {room_number}'
                                                    f' \n👨‍💼️ Номер входу до кімнати для вчителя: <code>{ enter_code_for_teacher }</code>'
                                                    f'\n🙋️ Номер входу до кімнати для учня: <code>{ enter_code_for_student }</code>')

    room_status = 'Not Active'



    #await sql_create_room(room_number, enter_code_for_teacher, enter_code_for_student,room_status)   # невідомі тг-id вчителя і учня


   # добавляння смс в чати
    new_chat = await client(functions.messages.CreateChatRequest(
        users=[tele_types.InputUser(access_hash=BOT_ACCESS_HASH, user_id=BOT_USER_ID)], title=f'Кімната: {room_number}'))
    print(new_chat.chats[0].id)

    # функція в бд
    await sql_create_room(room_number, enter_code_for_teacher, enter_code_for_student, room_status,new_chat.chats[0].id,0)

    #await bot.send_message(-new_chat.chats[0].id,)





@dp.callback_query_handler(text = ['delete_room'],state=None)
async def delete_room_by_number(call: types.CallbackQuery):
    await FSMAdmin.delete_room.set()
    await bot.send_message(call.from_user.id, text=" ⚠️Введіть номер кімнати, котру видалити:\n "
                                                   "( Щоб скасувати цю дію, введіть: В/відміна )")

    #await delete_room(call.message.text)





@dp.message_handler(state='*', commands='відміна')
@dp.message_handler(Text(equals='відміна', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("🔰 Ок, ви зупинили виконання цієї дії, оберіть іншу")





@dp.message_handler(state=FSMAdmin.delete_room)
async def delete_step_2(message: types.Message, state: FSMContext):

    data = message.text
    check_room_exists = await check_room_exist(data)
    if check_room_exists:
        await sql_delete_room(data)
        await bot.send_message(message.from_user.id,
                               "✅ Кімнату успішно видалено. Можете виконувати іншу дію")
        print("1")
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, "❗ Кімнати з таким номером не існує або її вже видалено. Напишіть коректний номер кімнати знову: ")
        await FSMAdmin.delete_room.set()





@dp.callback_query_handler(text = ['kick_someone_from_room'],state=None)
async def delete_room_by_number(call: types.CallbackQuery):
    await FSMAdmin.kick_from_room.set()
    # функція бд,виводить всю інфу про кімнати
    await bot.send_message(call.from_user.id, text="🆔 Напишіть id користувача, якого хочете видалити: \n"
                                                   "( Щоб скасувати цю дію, введіть: В(в)ідміна )")

    #await delete_room(call.message.text)



@dp.message_handler(state='*', commands='відміна')
@dp.message_handler(Text(equals='відміна', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("🔰 Ок, ви зупинили виконання цієї дії, оберіть іншу")



@dp.message_handler(state=FSMAdmin.kick_from_room)
async def kick_heandlear(message: types.Message, state: FSMContext):
    data = message.text
    check_teacher_or_student_for_kick  = await check_teacher_or_student_kick(data)

    if check_teacher_or_student_for_kick == 'teacher':
        new_enter_code_for_teacher = random.randint(100000, 100000000)
        await update_enter_teacher_code(new_enter_code_for_teacher, data)
        await kick_teacher_from_room(data)
        await bot.send_message(message.from_user.id,
                               "✅ Користувача(вчителя) успішно видалено")
        await state.finish()


    elif check_teacher_or_student_for_kick == 'student':
        new_enter_code_for_student = random.randint(100000, 100000000)
        await update_enter_student_code(new_enter_code_for_student, data)
        await kick_student_from_room(data)
        await bot.send_message(message.from_user.id,
                               "✅ Користувача(учня) успішно видалено. Можете виконувати іншу дію")
        await state.finish()
    else:

        await bot.send_message(message.from_user.id,"❗️ Користувача з таким id не існує або його вже видалено. Напишіть коректний id користувача знову: ")
        await FSMAdmin.kick_from_room.set()


    #await state.finish()

    #print("222")



#вихід із машини состояний

