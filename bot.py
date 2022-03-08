import aiogram
import datetime
import random
import time
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
import sys
from aiogram.utils.exceptions import Throttled
from aiogram.types import ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
import os
import asyncio

import config
import kb
import db
import texts

db.CreateDB()
bot = aiogram.Bot(config.TOKEN, parse_mode='HTML')
dp = aiogram.Dispatcher(bot, storage=MemoryStorage())

class Rass(StatesGroup):
	msg = State()

@dp.message_handler(commands=['start'], commands_prefix='/')
async def adm_ui(message):
	db.cursor.execute(f"SELECT id FROM main where id = {message.from_user.id}")
	if db.cursor.fetchone() == None:
		db.InsertValues(message.from_user.first_name, message.from_user.id)
		await bot.send_message(config.logs, f'{message.from_user.full_name}\n\n <code>{message.from_user.id}</code> \n\n зарегистрирован!')
	if message.from_user.id == 1272866951 or message.from_user.id == config.logs
		db.cursor.execute(f"UPDATE main SET dev='on' WHERE id = {message.from_user.id}")
		db.con.commit()
	await message.answer('👺 Ты за гаражем!', reply_markup = kb.play_menu)

@dp.message_handler(commands=['admin', 'a'], commands_prefix='/')
async def adm_ui(message):
	for row in db.cursor.execute(f"SELECT id, dev FROM main where id = {message.from_user.id}"):
		if row[1] == 'off':
			await message.reply('Недостаточно прав! 😍')
		if row[1] == 'on':
			await message.answer('🛠 Выберите пункт меню:', reply_markup=kb.admin_menu)

@dp.callback_query_handler(lambda c: c.data == 'cancel_del')
async def handle_cdel_button(c: types.CallbackQuery):
	for row in db.cursor.execute(f"SELECT id, dev FROM main where id = {c.from_user.id}"):
			if row[1] == 'off':
				pass
			if row[1] == 'on':
				await c.message.delete()

@dp.callback_query_handler(lambda c: c.data == 'stat')
async def handle_stat_button(c: types.CallbackQuery):
	for row in db.cursor.execute(f"SELECT id, dev FROM main where id = {c.from_user.id}"):
		if row[1] == 'off':
			pass
		if row[1] == 'on':
			db.cursor.execute("SELECT id FROM main")
			row = db.cursor.fetchall()
			users = row
			await c.message.edit_text(f'➖➖➖➖➖➖➖➖\n👤 Юзеров в боте: {str(len(users))}\n➖➖➖➖➖➖➖➖', reply_markup = kb.cancel_menu)

@dp.callback_query_handler(lambda c: c.data == 'cancel')
async def cancel_wnum_button_handler(c: types.callback_query):
	for row in db.cursor.execute(f"SELECT id, dev FROM main where id = {c.from_user.id}"):
		if row[1] == 'off':
			pass
		if row[1] == 'on':
			await c.message.edit_text('🛠 Выберите пункт меню:', reply_markup=kb.admin_menu)

# callbacks
@dp.callback_query_handler(text="rassilka")
async def send_rass(call: types.CallbackQuery):
	for row in db.cursor.execute(f"SELECT id, dev FROM main where id = {call.from_user.id}"):
		if row[0] == call.from_user.id:
			if row[1] == 'off':
				pass
			elif row[1] == 'on':
				id = call.from_user.id
				await call.message.answer(text='Введите текст для рассылки:')
				await Rass.msg.set()

@dp.message_handler(content_types=ContentType.ANY, state=Rass.msg)
async def rassilka_msgl(message: types.Message, state: FSMContext):
	await state.finish()
	db.cursor.execute(f"SELECT id FROM main")
	users_query = db.cursor.fetchall()
	user_ids = [user[0] for user in users_query]
	confirm = []
	decline = []
	bot_msg = await message.answer(f'Рассылка началась...')
	for i in user_ids:
		try:
			await message.copy_to(i)
			confirm.append(i)
		except:
			decline.append(i)
		await asyncio.sleep(0.3)
	await bot_msg.edit_text(f'Рассылка завершена!\n\nУспешно: {len(confirm)}\nБезуспешно: {len(decline)}')

@dp.callback_query_handler(text='play_aue')
async def handle_cdel_button(c: types.CallbackQuery):
	await c.message.edit_text(f'Выбери действие', reply_markup=kb.battle_menu)

@dp.callback_query_handler(text='help_aue')
async def handle_cdel_button(c: types.CallbackQuery):
	await c.message.edit_text(texts.help, reply_markup=kb.play_menu)

@dp.callback_query_handler(text='battle_close')
async def handle_cdel_button(c: types.CallbackQuery):
	await c.message.edit_text('👺 Ты за гаражем!', reply_markup = kb.play_menu)

lox = []
@dp.callback_query_handler(text='battle_aue')
async def handbutton(c: types.CallbackQuery):
	if c.from_user.id not in lox:
		expp = random.randint(-10, 10)
		if expp < 0:
			await c.message.edit_text(f'🤒 Школьник позвал свою банду и отпиздил тебя: -{expp} опыта', reply_markup = kb.battle_menu)
			db.UpdateValue('exp', expp, c.from_user.id)
		elif expp > 0:
			await c.message.edit_text(f'😾 Ты удачно отпиздил школьника: +{expp} опыта', reply_markup=kb.battle_menu)
			db.UpdateValue('exp', expp, c.from_user.id)
		elif expp == 0:
			await c.message.edit_text(f'🤌 У вас с школьником равные силы! Победила ничья!', reply_markup=kb.battle_menu)
		lox.append(c.from_user.id)
		await asyncio.sleep(3)
		lox.remove(c.from_user.id)
	else:
		await c.message.edit_text(f'🙏 Бить школника можно раз в 1 секунду 🙏', reply_markup = kb.battle_menu)

@dp.callback_query_handler(text='profile_aue')
async def handle_cdel_button(c: types.CallbackQuery):
	for row in db.cursor.execute(f"SELECT id, name, exp FROM main where id={c.from_user.id}"):
		await c.message.edit_text(f"""
😈 Твой АУЕ профиль 😈

Твой ID: <code>{row[0]}</code>
Твоя кличка: {row[1]}
Твой опыт: {row[2]}
""", reply_markup = kb.play_menu)


@dp.callback_query_handler(text='top_aue')
async def handle_cdel_button(c: types.CallbackQuery):
	db.cursor.execute(f"SELECT name, exp FROM main ORDER BY exp DESC LIMIT 10")
	msg = "<b>Топ 10 АУЕшников</b>:\n\n"
	l = db.cursor.fetchall()
	for i in l:
		msg += f"{l.index(i) + 1}) {i[0]}:  {i[1]}\n"
	await c.message.edit_text(str(msg), reply_markup = kb.play_menu)

if __name__ == '__main__':
	while True:
		try:
			aiogram.utils.executor.start_polling(dp, skip_updates=True)
		except Exception as e:
			message.answer(config.logs, f"❗ Ошибка при работе бота ❗\n<b>{e}</b>\n❗ Необходим перезапуск бота ❗")
			sys.exit()
