from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_colum_keyboard(items: list[str], chosen_items: list[str] = None, continue_button: bool = False) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один столбец
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """

    keyboard = []

    if chosen_items is None:
        chosen_items = []

    for item in items:
        if item.lower() not in chosen_items:
            # keyboard.append([KeyboardButton(text=f"✅ {item}")])
            keyboard.append([KeyboardButton(text=item)])
    if continue_button:
        keyboard.append([KeyboardButton(text="Продолжить")])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
