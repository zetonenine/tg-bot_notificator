import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from inliner import Inliner
from utils import TestStates
from tasker import Jsoner
from dedoder import Decoder
import redis
import asyncio

logging.basicConfig(level=logging.INFO)

bot = Bot(token='1160891964:AAE0ba37vkpS14RQlH0VVlI2VPTovdS_D7U')

dp = Dispatcher(bot, storage=RedisStorage('localhost', 6379, db=5))
dp.middleware.setup(LoggingMiddleware())

r = redis.Redis(db=5)

button_task = KeyboardButton('Назначить задачу')

markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(button_task)


# TABLE = { 'users': {}}
# json_file = json.dumps(TABLE, indent=4)
# r.hset('TABLE', 'table', json_file)


@dp.message_handler(state=None, commands='start')
async def starting(message: types.Message):
    await message.answer('Привет!', reply_markup=markup)
    Jsoner.put_user_into_redis(None, message.from_user.id, r)

    # r.hset('user', message.from_user.id)


@dp.message_handler(state=None, text='Назначить задачу')
async def set_task(message: types.Message, state: FSMContext):
    await TestStates.setting_task.set()
    await message.answer('Продолжи: напомни мне, чтобы я...(помыл машину)')


@dp.message_handler(state=TestStates.setting_task, content_types=['text'])
async def set_time(message: types, state: FSMContext):
    if message.text == 'Назначить задачу':
        await message.answer('Ошибка, напиши ещё раз')
    else:
        await state.reset_state()
        Jsoner.rec_tasks(None, message.from_user.id, message.text, r)
        await message.answer('Хорошо, я сделаю так, чтобы ты обязательно ' + str.lower(message.text) + '!')


@dp.message_handler(state=None, commands='send')
async def sender(message: types.Message):
    user_id = message.from_user.id
    tasks = Jsoner.get_tasks(None, user_id, r)


    if tasks:
        keyboard = Inliner.inline_maker(None, tasks)
        await bot.send_message(user_id, f'Что из задуманного ты сделал?\n', reply_markup=keyboard)
    else:
        await bot.send_message(user_id, f'Молодец, ты всё выполнил! Жду новых указаний')


async def sender2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    tasks = Jsoner.get_tasks(None, user_id, r)
    keyboard = Inliner.inline_maker(None, tasks)

    if tasks:
        await bot.send_message(user_id, f'Хороооош! Что ещё сделал?\n', reply_markup=keyboard)
    else:
        await bot.send_message(user_id, f'Молодец, ты всё выполнил! Жду новых указаний')


@dp.callback_query_handler()
async def process_callback_today(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = Decoder.dcdr(None, callback_query)
    Jsoner.delete_tasks(None, callback_query.from_user.id, text, r)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await sender2(callback_query)


@dp.message_handler(commands='check')
async def check(message: types.Message):
    await message.answer('не знаю')


@dp.message_handler(commands=['flushall'])
async def hey(message: types.Message):
    r.flushall()
    await message.answer("All deleted")


@dp.message_handler(content_types=['text'])
async def hey(message: types.Message):
    await message.answer(message.text)


async def scheduler():
    """КАКИМ-ТО ОБРАЗОМ В get_tasks НУЖНО ПЕРЕДАТЬ user_id"""


    pass

    # if Jsoner.get_tasks(None, None, r):
    #     aioschedule.every().day.at("14:33").do(sender)
    #     aioschedule.every().day.at("18:10").do(sender)
    #     while True:
    #         await aioschedule.run_pending()
    #         await asyncio.sleep(1)


async def on_startup(x):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
