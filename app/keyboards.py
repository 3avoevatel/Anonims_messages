from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🔗Ссылка'), KeyboardButton(text='👤Профиль')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт в меню <3')


in_settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получать сообщения', callback_data='get_messages')]
])

admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📊Статистика', callback_data='get_users')],
    [InlineKeyboardButton(text='📢Рассылка', callback_data='say_broadcast')],
    [InlineKeyboardButton(text='📝Текст рассылки', callback_data='set_bc_text')],
    [InlineKeyboardButton(text='🖼Фото рассылки', callback_data='set_bc_photo')]
])