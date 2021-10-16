import aiogram
import datetime
import random
import time
import requests
import io
from textwrap import wrap
from gtts import gTTS
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem
from html import escape
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.exceptions import BotBlocked
import asyncio
from aiogram.utils.exceptions import Unauthorized
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from io import StringIO
import sys
from aiogram.utils.exceptions import Throttled
import socket
from aiogram.types import ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
import os
import re
import json
import base64
import asyncio
import requests
from typing import List

import config
import texts

class Rass(StatesGroup):
	msg = State()

# open dev's menu
admin_menu = InlineKeyboardMarkup()
statistics_bt = InlineKeyboardButton(text='📊 Статистика', callback_data='stat')
test_bt = InlineKeyboardButton(text='TID_TEST', callback_data='test_eb')
mail_bt = InlineKeyboardButton(text='✉️ Рассылка', callback_data='rassilka')
cancel_del_menu = InlineKeyboardMarkup()
cancel_del_bt = InlineKeyboardButton(text='❌ Закрыть ❌', callback_data='cancel_del')
admin_menu.add(statistics_bt, mail_bt)
admin_menu.add(cancel_del_bt)

# close button
cancel_menu = InlineKeyboardMarkup()
cancel_bt = InlineKeyboardButton(text = '🚫 Отмена', callback_data = 'cancel')
cancel_menu.add(cancel_bt)

# play keyboard
play_menu = InlineKeyboardMarkup()
play_aue = InlineKeyboardButton(text = '😈 На забив', callback_data = 'play_aue')
help_aue = InlineKeyboardButton(text = '😶‍🌫️ Помощь', callback_data = 'help_aue')
profile_aue = InlineKeyboardButton(text = '💀 Профиль', callback_data = 'profile_aue')
top_aue = InlineKeyboardButton(text = '🤙 Топ АУЕшников', callback_data = 'top_aue')
play_menu.add(play_aue, help_aue)
play_menu.add(profile_aue, top_aue)

# battle keyboard
battle_menu = InlineKeyboardMarkup()
battle_aue = InlineKeyboardButton(text = '👹 Побить школьника', callback_data = 'battle_aue')
battle_close = InlineKeyboardButton(text = '💪🏻 Убежать', callback_data = 'battle_close')
battle_menu.add(battle_aue)
battle_menu.add(battle_close)

