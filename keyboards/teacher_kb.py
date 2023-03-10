from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


# кнопки вчителя

main_menu_for_teacher = InlineKeyboardButton(text='📌 Мої кімнати 📌', callback_data = 'all_teachers_rooms')
button_main_menu_teacher = InlineKeyboardMarkup(resize_keyboard=True).add(main_menu_for_teacher)



choose_rooms_tch = InlineKeyboardButton(text='🔑 Ввійти до кімнати ', callback_data = 'enter_in_room')
add_note_for_room = InlineKeyboardButton(text='🛎 Добавити замітки ', callback_data = 'add_note_to_room_info')
button_case_teacher = InlineKeyboardMarkup(resize_keyboard=True).row(choose_rooms_tch,add_note_for_room)


#choose_rooms_tch = InlineKeyboardButton(text='📌 Ввійти до кімнати 📌', callback_data = 'choose_rooms_for_teacher')
#button_case_teacher = InlineKeyboardMarkup(resize_keyboard=True).add(choose_rooms_tch)



#change_room_name = InlineKeyboardButton(text='📌 Змінити назву кімнати 📌', callback_data = 'choose_rooms_for_teacher')
#button_case2_teacher = InlineKeyboardMarkup(resize_keyboard=True).add(choose_rooms_tch)
