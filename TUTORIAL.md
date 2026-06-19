# Django + Aiogram 3: O'quvchilar uchun qo'llanma

Assalomu alaykum! Ushbu qo'llanma **Django** va **Aiogram 3** ni birgalikda qanday ishlatishni va bu shablon qanday tuzilganligini tushunishga yordam beradi.

---

## 1. Nega Django va Aiogram ni birga ishlatamiz?
- **Aiogram 3**: Telegram bot yaratish uchun eng tezkor va zamonaviy (asinxron) kutubxonalardan biri.
- **Django**: Ma'lumotlar bazasi (ORM) bilan ishlash juda qulay va u tayyor kuchli **Admin Panel** ga ega.
- **Natija**: Botni Aiogram'da yozamiz (tezkor ishlashi uchun), foydalanuvchilar va ma'lumotlarni esa Django Admin panelidan boshqaramiz (qulay bo'lishi uchun).

---

## 2. Loyiha arxitekturasi qanday ishlaydi?
Odatda Django web-saytlar uchun ishlatiladi va `runserver` komandasi orqali server ko'tariladi. Ammo bot uzluksiz ishlashi uchun biz maxsus **Django Management Command** yaratdik.

Ya'ni, bot alohida skript sifatida ishga tushadi, lekin Django'ning ichida yashagani uchun uning ma'lumotlar bazasidan to'g'ridan-to'g'ri foydalana oladi. 

---

## 3. Asosiy fayllar va ularning vazifasi

### 🔹 `tgbot/models.py`
Bu yerda biz ma'lumotlar bazasi jadvallarini yaratamiz. Hozirgi shablonda `TelegramUser` nomli jadval bor. 
Siz yangi ma'lumot qo'shmoqchi bo'lsangiz (masalan, Mahsulotlar jadvali), uni shu yerda yozib, so'ngra migratsiya qilasiz (`makemigrations` va `migrate`).

### 🔹 `tgbot/admin.py`
Yaratgan modellaringiz Admin panelda ko'rinishi uchun ularni shu faylda ro'yxatdan o'tkazasiz.

### 🔹 `tgbot/management/commands/runbot.py`
Bu bizning botimizning "motor"i. 
Botni ishga tushirish uchun siz terminalda `python manage.py runbot` deb yozasiz. Bu fayl barcha handler'larni yig'ib, Aiogram botni "Polling" usulida ishga tushiradi.

### 🔹 `tgbot/handlers/`
Bu papkada botning mantiqiy qismi yoziladi. Masalan, foydalanuvchi `/start` ni bossa, bot nima deb javob berishi kerakligi `start.py` faylida yozilgan.

---

## 4. Eng muhim qoida: `sync_to_async` nima o'zi?

Aiogram **asinxron** (`async` va `await` bilan) ishlaydi. 
Django ORM (ma'lumotlar bazasiga murojaat) esa hozircha to'liq asinxron emas, u **sinxron** ishlaydi. 

Siz asinxron funksiya ichida ma'lumotlar bazasidan nimadir qidirsangiz (masalan `TelegramUser.objects.get()`), xatolik yuz beradi. Buni oldini olish uchun Django bizga **`sync_to_async`** degan vositani bergan.

**Misol uchun:**
```python
from asgiref.sync import sync_to_async

# Baza bilan ishlaydigan oddiy sinxron kodni alohida yozib, @sync_to_async qo'shamiz
@sync_to_async
def get_user_from_db(user_id):
    return TelegramUser.objects.get(telegram_id=user_id)

# Aiogram handler'da esa uni await qilib chaqiramiz
@router.message(CommandStart())
async def start_bot(message: types.Message):
    user = await get_user_from_db(message.from_user.id)
    await message.answer(f"Salom, {user.full_name}!")
```

---

## 5. Amaliyot: Yangi buyruq qo'shib ko'ramiz

Keling, botga `/help` degan buyruq va handler qo'shamiz:

1. `tgbot/handlers/` papkasida yangi `help.py` fayl yarating.
2. Quyidagi kodni yozing:
```python
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command('help'))
async def help_handler(message: types.Message):
    await message.answer("Sizga qanday yordam bera olaman?")
```
3. Endi bu handlerni bot tanishi uchun `tgbot/handlers/__init__.py` faylini ochib uni router'ga qo'shamiz:
```python
from .start import router as start_router
from .help import router as help_router # Yangi qo'shilgan qator

def setup_handlers() -> Router:
    router = Router()
    router.include_router(start_router)
    router.include_router(help_router) # Yangi qo'shilgan qator
    return router
```
4. `python manage.py runbot` orqali botni o'chirib qayta yoqing. Endi bot `/help` ni tushunadi!

---

## 6. Loyihani qanday qilib serverga (Production) qo'yamiz?
Bu shablon Polling orqali ishlashga mo'ljallangan bo'lib, o'rganish va loyihani ishlab chiqish uchun eng zo'r usul hisoblanadi. Real loyihalarda va serverlarda botni **Webhook** usuliga o'tkazish tavsiya qilinadi (yoki Pollingni `systemd` orqali fonda ishlashga qo'yib qo'yish ham mumkin).
