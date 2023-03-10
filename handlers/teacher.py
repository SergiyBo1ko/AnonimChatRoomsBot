#Кнопка всі кімнати
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, callback_query

from create_bot import bot, dp
from database.sqlite_db import sql_show_all_rooms, sql_show_enter_teacher_code_rooms, \
    get_enter_teacher_code_using_room_number, get_enter_student_code_using_room_number, get_teacher_user_id, \
    get_student_user_id, get_room_status, get_chat_id, set_note_to_room, check_which_room, get_teacher_note,get_all_rooms_for_teacher
from keyboards.teacher_kb import add_note_for_room, button_case_teacher



class FSMTeacher(StatesGroup):
    fisrt_move = State()
    second_move = State()




@dp.callback_query_handler(text = ['all_teachers_rooms'])
async def show_all_teachers_rooms(call: types.CallbackQuery):

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
        tmp7 = await get_teacher_note(room[0])


        await bot.send_message(call.from_user.id ,text = f'Кімната: <code>{ room[0]}</code> \n'
                                                         f'ID Вчителя: <code>{ tmp3 }</code>\n'
                                                         f'ID Учня: <code>{ tmp4 }</code>\n'
                                                         f'# Замітка: {tmp7}\n',reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'Зайти в кімнату { room[0]}',callback_data=f'enter_{room[0]}'),InlineKeyboardButton(text=f'Добавити нотатку в км { room[0]}',callback_data=f'note_{room[0]}')))
                               #reply_markup=button_case_teacher)
                                                        # f'Код допуску вчителя: <code>{ tmp1}</code>\n'
                                                        # f'Код допуску учня:  <code>{ tmp2}</code>\n'
                                                        # f'Статус кімнати: {tmp5}\n'
                                                        # f'Чат-id із повідомленнями: <code>{tmp6}</code>')  #БД для кімнат
    await bot.send_message(call.from_user.id, text='👾-------------------------------------------------------------👾')




# Створення нотаток
#@dp.callback_query_handler(text = ['add_note_to_room_info'])
#async def add_note_to_room_infoo(call: types.CallbackQuery):

    #set_note_to_room()



@dp.callback_query_handler(lambda x: x.data and x.data.startswith('note_'),state=None)
async def callback_note(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,text="Введіть вашу замітку ")
    await FSMTeacher.fisrt_move.set()



@dp.message_handler(state='*', commands='відміна')
@dp.message_handler(Text(equals='відміна', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("🔰 Ок, ви зупинили виконання цієї дії, оберіть іншу")





@dp.message_handler(state=FSMTeacher.fisrt_move)
async def get_note_info(message: types.Message, state: FSMContext):
    data = message.text
    user_id = message.from_user.id
    room_number = await check_which_room(user_id)
    print(data)
    #await set_note_to_room(data.split('_')[1])
    await set_note_to_room(data,room_number)
    await bot.send_message(message.from_user.id,"Ви успішно створли нотатку!")
    await state.finish()



# -------------------------------------------------




@dp.callback_query_handler(lambda x: x.data and x.data.startswith('enter_'),state=None)
async def callback_note(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,text="Введіть вашу замітку ")
    await FSMTeacher.fisrt_move.set()



@dp.message_handler(state='*', commands='відміна')
@dp.message_handler(Text(equals='відміна', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("🔰 Ок, ви зупинили виконання цієї дії, оберіть іншу")





@dp.message_handler(state=FSMTeacher.fisrt_move)
async def get_note_info(message: types.Message, state: FSMContext):

    data = message.text
    print("room",data)
    user_id = message.from_user.id
    room_number = await check_which_room(user_id)
    #print(data)
    #await set_note_to_room(data.split('_')[1])
    await set_note_to_room(data,room_number)
    await bot.send_message(message.from_user.id,"Ви успішно створли нотатку!")
    await state.finish()