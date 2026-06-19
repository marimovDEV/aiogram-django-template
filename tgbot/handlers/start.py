from aiogram import Router, types
from aiogram.filters import CommandStart
from asgiref.sync import sync_to_async
from tgbot.models import TelegramUser

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    # Django ORM yordamida foydalanuvchini bazaga qo'shish yoki topish
    # ORM sinxron bo'lgani uchun, asinxron funksiyada 'sync_to_async' ishlatilishi shart.
    
    @sync_to_async
    def get_or_create_user(user: types.User):
        return TelegramUser.objects.get_or_create(
            telegram_id=user.id,
            defaults={
                'full_name': user.full_name,
                'username': user.username
            }
        )
    
    user_obj, created = await get_or_create_user(message.from_user)
    
    if created:
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.")
    else:
        await message.answer(f"Assalomu alaykum yana bir bor, {message.from_user.full_name}! Sizni ko'rib turganimdan xursandman.")
