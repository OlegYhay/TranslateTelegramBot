from aiogram import Bot, Dispatcher, types
from googletrans import Translator
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import config

bot = Bot(token=config.TOKEN_TELEGRAM)
dp = Dispatcher(bot=bot)

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(KeyboardButton('Английский 🇱🇷'))
kb_menu.insert(KeyboardButton('Французкий 🇫🇷'))
kb_menu.add(KeyboardButton('Китайский 🇨🇳'))
kb_menu.insert(KeyboardButton('Русский 🇷🇺'))

kb_settings = ReplyKeyboardMarkup(resize_keyboard=True)
kb_settings.add(KeyboardButton('Сменить язык'))

info_user = {}

LANGUAGE_PREFFIX = {
    'Английский 🇱🇷': 'en',
    'Французкий 🇫🇷': 'fr',
    'Китайский 🇨🇳': 'zh-tw',
    'Русский 🇷🇺': 'ru',
}


# обработчик который обрабатывает команду start
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.answer(
        "Выбери язык на который мы будем переводить!🇷🇺\n Язык с которого переводим определяется автоматически!",
        reply_markup=kb_menu)


# Сохраняем информацию на какой язык хочет перевести пользователь
@dp.message_handler(Text(equals=["Английский 🇱🇷", "Французкий 🇫🇷", "Китайский 🇨🇳", "Русский 🇷🇺"]))
async def start_bot(message: types.Message):
    info_user[message.from_user.id] = LANGUAGE_PREFFIX[message.text]
    await message.answer('Успешно!\nТеперь вы можете отправлять текст для перевода.', reply_markup=kb_settings)


# Обрабатываем команду сменить язык и выводим список доступных языков
@dp.message_handler(Text(equals='Сменить язык'))
async def change_language(message: types.Message):
    await message.answer(
        "Выберите язык на который будем переводить",
        reply_markup=kb_menu)


# Переводим отправленный пользователем текст
@dp.message_handler(content_types=[types.ContentType.ANY])
async def change_language(message: types.Message):
    translator = Translator()
    try:
        result = translator.translate(message.text, dest=info_user[message.from_user.id])
        text = result.text
    except:
        text = 'Что то пошло не так:('
    await message.answer(
        text,
        reply_markup=kb_settings)
