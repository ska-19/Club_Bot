from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_kb import make_colum_keyboard

router = Router()

yes_no_ans = ["Да", "Нет"]


class Users_rc_ready:
    def __init__(self):
        self.users_rc_ready = {}

    def __getitem__(self, item):
        return self.users_rc_ready[item]

    def __setitem__(self, key, value):
        self.users_rc_ready[key] = value

    def keys(self):
        return self.users_rc_ready.keys()

    def items(self):
        return self.users_rc_ready.items()

    def __len__(self):
        return len(self.users_rc_ready)

    def clear(self):
        self.users_rc_ready.clear()


class User_rc_pair:
    def __init__(self):
        self.user_rc_pair = {}

    def __getitem__(self, item):
        if item not in self.user_rc_pair.keys():
            return None
        return self.user_rc_pair[item]

    def __setitem__(self, key, value):
        self.user_rc_pair[key] = value

    def keys(self):
        return self.user_rc_pair.keys()

    def items(self):
        return self.user_rc_pair.items()

    def __len__(self):
        return len(self.user_rc_pair)

    def clear(self):
        self.user_rc_pair.clear()


users_rc_ready = Users_rc_ready()
user_rc_pair = User_rc_pair()


class Take_part_state:
    def __init__(self):
        self.state = False

    def set_state(self, state: bool):
        self.state = state

    def __bool__(self):
        return self.state


take_part_state = Take_part_state()


async def send_error_message(message: Message, keyboard_options: list[str],
                             error_text: str = "😭 Я не понимаю такого ответа.\n\n"
                                               "Пожалуйста, выберите один из вариантов"
                                               "из списка ниже:"):
    await message.reply(
        text=error_text,
        reply_markup=make_colum_keyboard(keyboard_options, [])
    )


@router.callback_query(F.data == "take_part")
async def cmd_back(callback: F.CallbackQuery):
    if take_part_state:
        await callback.message.answer(
            text="<b>Ожидайте пару</b>",
            reply_markup=ReplyKeyboardRemove()
        )
        users_rc_ready[callback.from_user.id] = True
    else:
        await callback.message.answer(
            text="<b>На этой неделе вы уже не можете принять участие</b>\n"
                 "<i>Попробуйте на следующей неделе</i>",
            reply_markup=ReplyKeyboardRemove()
        )
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == "decline")
async def cmd_back(callback: F.CallbackQuery):
    await callback.message.answer(
        text="<b>Хорошо, эту неделю пропустим</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == "meeting_done")
async def cmd_back(callback: F.CallbackQuery):
    await callback.message.answer(
        text="<b>Отлично! Надеюсь, вам было интересно)</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    users_rc_ready[callback.from_user.id] = False
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == "meeting_later")
async def cmd_back(callback: F.CallbackQuery):
    await callback.message.answer(
        text="<b>Хорошо, договоритесь о встрече позже</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    users_rc_ready[callback.from_user.id] = False
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == "meeting_notdone")
async def cmd_back(callback: F.CallbackQuery):
    await callback.message.answer(
        text="<b>Жаль, надеюсь, в следующий раз получится</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    users_rc_ready[callback.from_user.id] = False
    await callback.message.delete()
    await callback.answer()
