from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_colum_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один столбец
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    keyboard = []
    for item in items:
        keyboard.append([KeyboardButton(text=item)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
