from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_kb import make_colum_keyboard
from database import requests as rq

router = Router()

yes_no_ans = ["Да", "Нет"]

global users_rc_ready
global user_rc_pair

users_rc_ready = {}
user_rc_pair = {}


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
