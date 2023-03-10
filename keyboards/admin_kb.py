from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


# кнопки админа СТАРТ

all_rooms = InlineKeyboardButton(text='💬 Існуючі кімнати 💬',callback_data='all_rooms')
create_room = InlineKeyboardButton(text='🧑‍💻 Створити кімнату 🧑‍💻',callback_data='create_room')
#see_messegas_in_room = InlineKeyboardButton(text='🔔 Переглянути повідомлення конкретної кімнати 🔔',callback_data='see_messegas_in_room')
kick_someone_from_room = InlineKeyboardButton(text='⚠ Вигнати когось із кімнати ⚠️',callback_data='kick_someone_from_room')
delete_room = InlineKeyboardButton(text='❕ Видалити кімнату ❕',callback_data='delete_room')


button_case_admin = InlineKeyboardMarkup(resize_keyboard=True,).add(all_rooms)\
    .add(create_room).add(kick_someone_from_room).add(delete_room)




