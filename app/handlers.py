
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
import sqlite3


broadcast_text = ""
broadcast_photo = ""

def db_init():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

db_init()

my_router = Router()

user_states = {}

def add_user_to_db(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def get_user_count():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    conn.close()
    return count

@my_router.message(CommandStart())
async def cmd_start(message: Message):
    referral_id = str(message.from_user.id)
    args = message.text.split()[1:]

    add_user_to_db(message.from_user.id)

    if args:
        referral_id_arg = args[0]
        await message.answer(f'💬 Напишите ваше сообщение (ID: {referral_id_arg}):')
        user_states[message.from_user.id] = referral_id_arg
    else:
        await message.reply(f'💌 Добро пожаловать, вот твоя ссылка:\n🔗 https://t.me/uwu_code_test_bot?start={referral_id}\n'
                            f' \n💬 Каждый, кто перейдет по ней, сможет оставить тебе сообщение!',
                            reply_markup=kb.main)

@my_router.message(lambda msg: msg.text == '🔗Ссылка')
async def anon_mess(message: Message):
    await message.reply('💌 Чтобы получать анонимные сообщения, просто размести эту ссылку у себя в соц. сетях:\n'
                        f'🔗 https://t.me/uwu_code_test_bot?start={message.from_user.id}')

@my_router.message(lambda msg: msg.text == 'адм')
async def admin_panel(message: Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        await message.reply('👮‍♂️ Добро пожаловать в панель администратора', reply_markup=kb.admin_panel)
    else:
        return


@my_router.message(lambda message: message.text == '👤Профиль')
async def profile(message: Message):
    await message.reply(f'ℹ️ Ваш профиль\n'
                        f'\n'
                        f'- Никнейм: {message.from_user.first_name} | @{message.from_user.username} \n')
@my_router.callback_query(lambda cb: cb.data == 'say_broadcast')
async def send_broadcast(callback_query: CallbackQuery):
    user_count = get_user_count()
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()
    conn.close()

    for user in users:
        user_id = user[0]
        try:
            if broadcast_photo and broadcast_text:
                await callback_query.message.bot.send_photo(user_id, broadcast_photo, caption=broadcast_text)
            elif broadcast_text:
                await callback_query.message.bot.send_message(user_id, broadcast_text)
            elif broadcast_photo:
                await callback_query.message.bot.send_photo(user_id, broadcast_photo)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

    await callback_query.answer(f'📢 Рассылка успешно отправлена всем {user_count} пользователям!')

@my_router.callback_query(lambda cb: cb.data == 'set_bc_text')
async def set_broadcast_text(callback_query: CallbackQuery):
    await callback_query.answer("Введите текст рассылки:")

@my_router.callback_query(lambda cb: cb.data == 'set_bc_photo')
async def set_broadcast_photo(callback_query: CallbackQuery):
    await callback_query.answer("Отправьте фото для рассылки:")

@my_router.message(lambda message: message.text)
async def receive_broadcast_text(message: types.Message):
    global broadcast_text
    broadcast_text = message.text
    await message.reply("✅ Текст рассылки установлен!")

@my_router.message(lambda message: message.photo)
async def receive_broadcast_photo(message: types.Message):
    global broadcast_photo
    broadcast_photo = message.photo[-1].file_id
    await message.reply("✅ Фото рассылки установлено!")


@my_router.message(lambda message: message.text)
async def receive_broadcast_text(message: types.Message):
    global broadcast_text
    broadcast_text = message.text
    await message.reply("✅ Текст рассылки установлен!")

@my_router.message(lambda message: message.photo)
async def receive_broadcast_photo(message: types.Message):
    global broadcast_photo
    broadcast_photo = message.photo[-1].file_id
    await message.reply("✅ Фото рассылки установлено!")


@my_router.message()
async def handle_message_to_user(message: Message):
    referral_user_id = user_states.get(message.from_user.id)
    if referral_user_id:
        await message.reply('✅ Ваше сообщение было отправлено')

        await message.bot.send_message(referral_user_id, f'💬 Тебе пришло новое сообщение: \n_\n{message.text}_',
                                       parse_mode='MarkdownV2')
        del user_states[message.from_user.id]
    else:
        await message.reply('❌ Возникла ошибка: Для отправки сообщения, надо сначала перейти по чей-то ссылке')


@my_router.callback_query(lambda cb: cb.data == 'get_users')
async def get_users_count(callback: CallbackQuery):
    user_count = get_user_count()
    await callback.answer(f'📊 Количество участников бота: {user_count}')

