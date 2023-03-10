import random


from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

from create_bot import dp, bot
from database.sqlite_db import check_id_for_teacher, sql_add_user_id, check_user_id, \
    check_teacher_or_student_code_for_enter, update_id_for_teacher_in_room, update_id_for_student_in_room, \
    check_which_room, check_room_status, get_student_user_id, get_user_id, get_teacher_user_id, sql_delete_room, \
    get_teacher_user_id, get_chat_id, \
    check_active_status_room, update_enter_student_code, update_enter_teacher_code


class FSMUser(StatesGroup):
    get_room_enter_code = State()
    get_handler_for_teacher = State()
    get_handler_for_student = State()


@dp.callback_query_handler(text=['choose_rooms_for_student'], state=None)
async def check_userdsads_id(call: types.CallbackQuery):
    user_id = call.from_user.id
    temp = await check_user_id(user_id)

    if temp == 1:
        #await FSMUser.get_room_enter_code.set()
        await bot.send_message(call.from_user.id,text='✅ До речі, ви вже зареєстрований у боті \n 🔒 Введіть ваш код допуску для входу до кімнати:')
        await FSMUser.get_room_enter_code.set()
    else:
        await sql_add_user_id(user_id)
        #await FSMUser.get_room_enter_code.set()
        await bot.send_message(call.from_user.id, text='✅ Ви зареєструвалися у бот \n 🔒 Введіть ваш код допуску для входу до кімнати:')
        await FSMUser.get_room_enter_code.set()






@dp.message_handler(state='*', commands='відміна')
@dp.message_handler(Text(equals='відміна', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("🔰 Ок, ви зупинили виконання цієї дії, оберіть іншу")




@dp.message_handler(content_types=['text'], state=FSMUser.get_room_enter_code)
async def comunicating_from_teacher_side(message: types.Message, state: FSMContext):
    data = message.text
    id = message.from_user.id
    user_id = message.from_user.id
    check_tacher_or_student_code = await check_teacher_or_student_code_for_enter(data)


#-------------------------------------- вчитель


    if check_tacher_or_student_code == 'teacher':


        await update_id_for_teacher_in_room(user_id, data)
        await bot.send_message(message.from_user.id,
                               text=f" 👨‍🏫 Ви зайшли до кімнати, як вчитель.\n #️⃣ Код кімнати: <code>{await check_which_room(user_id)}</code>.\n"
                                    f" ❗  Чат активовано і розпочато...")
        room_number = await check_which_room(user_id)
        check_status = await check_room_status(room_number)


        if check_status:
            #check_st = await check_active_status_room(room_number)
            #if check_st == 1:
                #updated_enter_code_for_teacher = random.randint(100000, 100000000)
                #await update_enter_teacher_code(updated_enter_code_for_teacher,id)
            await FSMUser.get_handler_for_teacher.set()














    if check_tacher_or_student_code == 'student':

        await update_id_for_student_in_room(user_id, data)
        await bot.send_message(message.from_user.id,
                               text=f" 🙋 Ви зайшли до кімнати, як учень.\n #️⃣ Код кімнати: <code>{await check_which_room(user_id)}</code>.\n"
                                    f" ❗  Чат активовано і розпочато...")
        room_number = await check_which_room(user_id)
        check_status = await check_room_status(room_number)
        #student_user_id = await get_student_user_id(room_number)  # писати студенту (не виходить,лише в хендлері на смс)

        if check_status:
            #await bot.send_message(message.from_user.id, "👨‍💼 Вчитель приєднався...")
            #check_st = await check_active_status_room(room_number)
            #if check_st == 1:
                #updated_enter_code_for_student = random.randint(100000, 100000000)
                #await update_enter_student_code(updated_enter_code_for_student, id)

            await FSMUser.get_handler_for_student.set()

            #await bot.send_message(message.from_user.id, "👨‍💼 Вчитель приєднався...")

    if check_tacher_or_student_code == 'no in rooms':
        await bot.send_message(message.from_user.id, text='❗ Вас немає в кімнаті або ви ввели неправильний код допуску до кімнати. Напишіть ваш коректний код допуску до кімнати знову: ')


        await FSMUser.get_room_enter_code.set()
        #await bot.send_message(message.from_user.id, text='Введіть ваш код допуску для входу в кімнату ❗')
        # await bot.send_message(message.from_user.id, text='Ок,чекайте зєднання')    #f'{data}'
    # await FSMUser.next()






@dp.message_handler(state=FSMUser.get_handler_for_teacher, content_types=['text', 'photo', 'file', 'audio','voice','video','document','sticker'])
async def next_step_handler_for_teacher(message: types.Message, state: FSMContext):

    data = message.text
    user_id = message.from_user.id
    # запит в бд на активну кімнату цього юзера інашке ти не в акт кімнаті ,км де в кімнеті юзер
    # бд запит на інфу про км за номером
    room_number = await check_which_room(user_id)
    chat_id = await get_chat_id(room_number)
    print("chat id: ",chat_id)
    # TODO отримання кімнати по айді
    #print(room_number)
    student_user_id = await get_student_user_id(room_number)
    #await bot.send_message(student_user_id, "🔔 Вчитель приєднався до кімнати...")
    #print(student_user_id)
    #await bot.send_message(student_user_id, text=f"{data}")

    #await bot.forward_message()

    if message.photo:
        #print(message.photo[0].file_id)
        await bot.send_photo(student_user_id,message.photo[0].file_id)

    if message.audio:
        #print(message.audio[0])
        await bot.send_audio(student_user_id,message.audio.file_id)

    if message.voice:
        print(message.voice)
        await bot.send_voice(student_user_id,message.voice.file_id)

    if message.sticker:
        await bot.send_sticker(student_user_id,message.sticker.file_id)


    if message.video:
        print(message.video.file_id)
        await bot.send_video(student_user_id,message.video.file_id)

    #else:
    if message.text:
        #print(message.text)
        await bot.send_message(student_user_id, text=f"{message.text}")

    if message.document:
        print(message.document.file_id)
        await bot.send_document(student_user_id, message.document.file_id)


    await bot.forward_message('-'+chat_id, message.chat.id, message.message_id)

@dp.message_handler(state=FSMUser.get_handler_for_student, content_types=['text', 'photo', 'file', 'audio','voice','video','document','sticker'])
async def next_step_handler_for_student(message: types.Message, state: FSMContext):
    data = message.text
    user_id = message.from_user.id
    room_number = await check_which_room(user_id)
    chat_id = await get_chat_id(room_number)
    teacher_user_id = await get_teacher_user_id(room_number)
    #await bot.send_message(teacher_user_id, "🔔 Учень приєднався до кімнати...")
    #await bot.send_message(teacher_user_id, text=f"{data}")
    #await bot.forward_message(teacher_user_id, user_id, message.message_id, True)

    if message.photo:
        # print(message.photo[0].file_id)
        await bot.send_photo(teacher_user_id, message.photo[0].file_id)

    if message.audio:
        # print(message.audio[0])
        await bot.send_audio(teacher_user_id, message.audio.file_id)

    if message.voice:
        print(message.voice)
        await bot.send_voice(teacher_user_id, message.voice.file_id)

    if message.sticker:
        await bot.send_sticker(teacher_user_id,message.sticker.file_id)



    if message.video:
        print(message.video.file_id)
        await bot.send_video(teacher_user_id, message.video.file_id)

    # else:
    if message.text:
        # print(message.text)
        await bot.send_message(teacher_user_id, text=f"{message.text}")

    if message.document:
        print(message.document.file_id)
        await bot.send_document(teacher_user_id, message.document.file_id)

    await bot.forward_message('-'+chat_id, message.chat.id, message.message_id)

