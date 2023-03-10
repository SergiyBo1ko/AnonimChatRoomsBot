import telethon
from aiogram import executor
from create_bot import dp
from database import sqlite_db
from telethon.sync import TelegramClient
from handlers import client, admin,student

async def on_startup(_):
    print('Бот вышел в онлайн')
    await sqlite_db.sql_start()





#,admin,other

client.register_handlers_client(dp)




executor.start_polling(dp,skip_updates=True,on_startup=on_startup)