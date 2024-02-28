from main import bot
from aiogram import Router
from aiogram import F
from aiogram.types import Message
from keyboards import keyboard
from aiogram import types
from aiogram.filters import Command

router = Router()
@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer('Тестируем WebApp!', reply_markup=keyboard)



PRICE = {
    '1': [types.LabeledPrice(label='Item1', amount=100000)],
    '2': [types.LabeledPrice(label='Item2', amount=200000)],
    '3': [types.LabeledPrice(label='Item3', amount=300000)],
    '4': [types.LabeledPrice(label='Item4', amount=400000)],
    '5': [types.LabeledPrice(label='Item5', amount=500000)],
    '6': [types.LabeledPrice(label='Item6', amount=600000)]
}


@router.message(F.web_app_data)
async def buy_process(web_app_message):
    await bot.send_invoice(web_app_message.chat.id,
                           title='Laptop',
                           description='Description',
                           provider_token='pay_token',
                           currency='rub',
                           need_email=True,
                           prices=PRICE[f'{web_app_message.web_app_data.data}'],
                           start_parameter='example',
                           payload='some_invoice')


@router.pre_checkout_query()
async def pre_checkout_process(pre_checkout: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: types.Message):
    await message.answer('Платеж прошел успешно!')
