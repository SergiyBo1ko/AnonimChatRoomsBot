from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from telethon.sync import TelegramClient
from telethon.tl import functions
from telethon.tl.types import InputUserSelf, InputUserEmpty, InputUser

from config import TOKEN

from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=storage)




client = TelegramClient('session_phone:str', 'api_id:int', 'api_hash:str')
client.connect()

#session: 'typing.Union[str, Session]',
#api_id: int,
#api_hash: str,
