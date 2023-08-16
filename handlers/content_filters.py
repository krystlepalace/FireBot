from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.toggles import anim_inline
import bot


router = Router()

@router.message(Command("animations"))
async def toggle_animated_stickers(message: Message):
    await message.answer(
            "Разрешить анимированные стикеры?",
            reply_markup=anim_inline()
            )


@router.message()
async def check_sticker(message: Message):
    if not bot.animations_allowed:
        if message.sticker and (message.sticker.is_video or message.sticker.is_animated):
            await message.delete()
