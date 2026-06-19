# Django va Aiogram 3 Template

Bu loyiha **Django 5.x** va **Aiogram 3.x** kutubxonalarini birgalikda ishlatish uchun tayyor shablon (template) hisoblanadi. Asosiy maqsad – Telegram botlar yaratishda Django'ning kuchli ORM tizimi va Admin panelidan qulay foydalanishdir.

## Xususiyatlari
- Asosiy framework sifatida **Django 5** ishlatiladi.
- Telegram bot **Aiogram 3.x** yordamida yaratilgan.
- Atrof-muhit o'zgaruvchilarini boshqarish uchun `environs` ishlatiladi (`.env`).
- Asinxron aiogram va sinxron Django ORM o'rtasida muammosiz ishlash uchun `sync_to_async` dekoratoridan foydalanilgan.
- Botni ishga tushirish uchun maxsus Django boshqaruv buyrug'i (`runbot`) yaratilgan.

## O'rnatish

Loyihani o'z kompyuteringizga klonlangandan so'ng, quyidagi qadamlarni bajaring:

### 1. Virtual muhit yaratish va kutubxonalarni o'rnatish
```bash
python -m venv venv
source venv/bin/activate  # Windows uchun: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Sozlamalar faylini tayyorlash
`.env.example` faylini nusxalab, nomini `.env` ga o'zgartiring va ichidagi ma'lumotlarni o'zingizga moslang:
```bash
cp .env.example .env
```
`.env` faylining ichida Telegram bot tokenni yozishni unutmang (`BOT_TOKEN`).

### 3. Ma'lumotlar bazasini yaratish
Django modellarini ma'lumotlar bazasiga o'tkazish uchun migratsiya buyruqlarini bajaring:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Superfoydalanuvchi yaratish (Admin panel uchun)
```bash
python manage.py createsuperuser
```

## Ishga tushirish

Loyiha ikki qismdan iborat bo'lib, ikkalasi bir vaqtda ishlashi uchun ikkita terminal oynasidan foydalanishingiz mumkin:

**1. Django Web server (Admin panel uchun):**
```bash
python manage.py runserver
```
Shundan so'ng http://127.0.0.1:8000/admin sayti orqali foydalanuvchilar va ma'lumotlarni boshqarishingiz mumkin.

**2. Telegram Bot (Polling usulida):**
```bash
python manage.py runbot
```
Bot ishga tushgach, siz unga Telegram orqali `/start` buyrug'ini yuborishingiz mumkin. U avtomatik ravishda ma'lumotlar bazasiga (Django ORM orqali) foydalanuvchini qo'shadi.

## Fayl strukturasi bo'yicha qisqacha ma'lumot
- `tgbot/models.py` – Bot foydalanuvchilari uchun ma'lumotlar bazasi modellari.
- `tgbot/admin.py` – Admin panelda ko'rinadigan qismlar.
- `tgbot/handlers/` – Botning barcha mantiqiy qismi, xabarlarni qabul qilish (masalan, `start.py`). Yangi handler'lar yozganda `tgbot/handlers/__init__.py` orqali router'ga qo'shib qo'ying.
- `tgbot/keyboards/` – Barcha tugmalar (Inline va Reply).
- `tgbot/management/commands/runbot.py` – Aiogram botni ishga tushiruvchi maxsus fayl. Bu yerda `asyncio.run()` va polling mexanizmi joylashgan.
