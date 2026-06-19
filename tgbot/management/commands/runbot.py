import asyncio
import logging
import sys

from django.core.management.base import BaseCommand
from django.conf import settings
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from tgbot.handlers import setup_handlers

class Command(BaseCommand):
    help = "Telegram botni ishga tushirish (Polling)"

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        
        # Asinxron loopni ishga tushiramiz
        try:
            asyncio.run(self.run_bot())
        except (KeyboardInterrupt, SystemExit):
            self.stdout.write(self.style.SUCCESS("Bot to'xtatildi!"))

    async def run_bot(self):
        token = settings.BOT_TOKEN
        if not token:
            self.stdout.write(self.style.ERROR("BOT_TOKEN .env faylida topilmadi!"))
            return

        bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp = Dispatcher()

        # Barcha handlerlarni yuklash
        router = setup_handlers()
        dp.include_router(router)

        self.stdout.write(self.style.SUCCESS("Bot ishga tushirildi..."))
        
        # Eski xabarlarni o'tkazib yuborish (optional)
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Botni ishga tushirish
        await dp.start_polling(bot)
