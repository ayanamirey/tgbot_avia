import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from users.models import User, Category
from cities import city

Token = '5070606813:AAG-U6oFgut6MDHasNPA-kPvpIv62wDnvgI'

bot = telebot.TeleBot(token=Token)


def ask_language(chat_id, name):
    msg = f"<strong>{name}</strong>,\n\nTilni tanlang\nвыберите язык"
    user = user_info(chat_id)
    if user.lang != 'ru' and user.lang != 'uz':
        if name:
            user.fullname = name
            user.save()
        rkm = ReplyKeyboardMarkup(True, row_width=2)
        rkm.add('Uzbek 🇺🇿', 'Русский 🇷🇺')
        bot.send_message(chat_id, msg, reply_markup=rkm, parse_mode='HTML')


def user_info(chat_id):
    return User.objects.filter(chat_id=chat_id).first()


def category_info(id):
    return Category.objects.filter(id).first()


@bot.message_handler(commands=['del'])
def command_help(message):
    chat_id = message.from_user.id
    user = User.objects.get(chat_id=chat_id).delete()
    bot.send_message(chat_id, 'Deleted', reply_markup=ReplyKeyboardRemove())


def ask_contact(chat_id, lang):
    msg = 'Telefon raqamingizni kiriting' if lang == 'uz' else 'Введите свой номер телефона'
    bsg = 'Raqam yuborish' if lang == 'uz' else 'Отправить номер'
    rkm = ReplyKeyboardMarkup(True).add(KeyboardButton(bsg, request_contact=True))
    bot.send_message(chat_id, msg, reply_markup=rkm, parse_mode='HTML')


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    chat_id = message.from_user.id
    user = user_info(chat_id)
    lang = message.from_user.language_code
    phone_num = message.contact.phone_number

    if not user.contact_number:
        user.contact_number = phone_num[1:]
        user.save()

    rkm = ReplyKeyboardRemove()
    markup_inline = InlineKeyboardMarkup(row_width=1)

    if lang == 'ru':
        bot.send_message(chat_id, "Напишите город вылета", reply_markup=rkm, parse_mode='HTML')

    if lang == 'uz':
        bot.send_message(chat_id, "Ketish shahrini yozing", reply_markup=rkm, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def command_help(message):
    chat_id = message.from_user.id
    user_lang = user_info(chat_id=chat_id)
    name = message.from_user.first_name
    # Bazadan chat_id ni qidirish
    user = User.objects.filter(chat_id=chat_id)
    # Agar topilmasa
    if not user:
        # yangi user yaratish
        id = User.objects.create(chat_id=chat_id)
    else:
        if user_lang.lang == 'ru' or user_lang.lang == 'uz':
            if user_lang.lang == 'ru':
                bot.send_message(chat_id, f'С возвращением!\nЯзык выбран: Русский 🇷🇺')
            elif user_lang.lang == 'uz':
                bot.send_message(chat_id, f'Qaytish bilan!\nTil tanlangan: Uzbek 🇺🇿')
        else:
            bot.send_message(chat_id, 'С возвращением!')

    ask_language(chat_id, name)


@bot.message_handler(commands=['change_language'])
def change_language(message):
    chat_id = message.from_user.id
    name = message.from_user.first_name
    msg = f"<strong>{name}</strong>,\n\nTilni tanlang\nвыберите язык"
    user = user_info(chat_id)
    if name:
        user.fullname = name
        user.save()
    rkm = ReplyKeyboardMarkup(True, row_width=2)
    rkm.add('Uzbek 🇺🇿', 'Русский 🇷🇺')
    bot.send_message(chat_id, msg, reply_markup=rkm, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def text_message_handler(message):
    text = message.text
    chat_id = message.from_user.id
    user = user_info(chat_id)
    if text == 'Uzbek 🇺🇿' or 'Русский 🇷🇺':
        if text == 'Uzbek 🇺🇿':
            lang = 'uz'
        elif text == 'Русский 🇷🇺':
            lang = 'ru'
        user.lang = lang
        user.save()
        ask_contact(chat_id, lang)


bot.infinity_polling()
