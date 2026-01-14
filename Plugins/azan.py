import asyncio
import pytz
import aiohttp
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import *
from helpers.Ranks import *

# ━━━ إعدادات المنطقة الزمنية ━━━
cairo_timezone = pytz.timezone("Africa/Cairo")

# ━━━ قائمة المجموعات المفعل بها الأذان ━━━
azan_enabled_chats: list[int] = []

# ━━━ سدّ مكرر الإشعارات: خريطة chat_id -> last_sent_minute ━━━
_last_sent_minute: dict[int, str] = {}

# ━━━━━━━━━━ أوامر التشغيل والإيقاف ━━━━━━━━━━
@Client.on_message(filters.command(["تفعيل الاذان", "تشغيل الاذان"], ""), group=828)
async def enable_azan(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        if not admin_pls(message.from_user.id, chat_id):
            return await message.reply_text("هذا الأمر يخص ❪ الأدمن وفوق ❫ بس")

        if chat_id in azan_enabled_chats:
            await message.reply_text("🔊 الأذان مفعل بالفعل في هذه المجموعة")
        else:
            azan_enabled_chats.append(chat_id)
            await message.reply_text("✅ تم تفعيل الأذان بنجاح في هذه المجموعة")
    except Exception as e:
        print("enable_azan ERROR:", e)


@Client.on_message(filters.command(["تعطيل الاذان", "ايقاف الاذان"], ""), group=929229)
async def disable_azan(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        if not admin_pls(message.from_user.id, chat_id):
            return await message.reply_text("هذا الأمر يخص ❪ الأدمن وفوق ❫ بس")

        if chat_id in azan_enabled_chats:
            azan_enabled_chats.remove(chat_id)
            # تنظيف الكاش إن وُجد
            _last_sent_minute.pop(chat_id, None)
            await message.reply_text("✅ تم تعطيل الأذان بنجاح في هذه المجموعة")
        else:
            await message.reply_text("🔇 الأذان معطل بالفعل في هذه المجموعة")
    except Exception as e:
        print("disable_azan ERROR:", e)


# ━━━━━━━━━━ وظيفة الحصول على مواقيت الصلاة (async, آمنة) ━━━━━━━━━━
async def get_prayer_time() -> tuple | None:
    """
    ترجع (prayer_name_ar, prayer_time_str) لو في أذان الآن،
    أو None لو لا أو لو فشل الاتصال.
    """
    url = "http://api.aladhan.com/v1/timingsByAddress?address=Cairo&method=4&school=0"
    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    print(f"خطأ HTTP في المواقيت: status={resp.status}")
                    return None
                data = await resp.json()
    except Exception as e:
        print(f"خطأ في الحصول على المواقيت: {e}")
        return None

    try:
        timings = data["data"]["timings"]
        # current time in Cairo as HH:MM
        current_time = datetime.now(cairo_timezone).strftime("%H:%M")

        # كلمات الصلاة بالإنجليزية من API واسمها العربي
        mapping = {
            "Fajr": "الفجر",
            "Dhuhr": "الظهر",
            "Asr": "العصر",
            "Maghrib": "المغرب",
            "Isha": "العشاء"
        }

        # ابحث إذا وقت الصلاة يطابق الوقت الحالي
        for prayer_en, prayer_ar in mapping.items():
            prayer_time_raw = timings.get(prayer_en)
            if not prayer_time_raw:
                continue

            # واعتماداً على شكل الـ API، نأخذ أول 5 أحرف "HH:MM"
            prayer_time = prayer_time_raw.strip()[:5]

            if prayer_time == current_time:
                return prayer_ar, prayer_time
    except Exception as e:
        print("خطأ في تحليل مواقيت الصلاة:", e)

    return None


# ━━━━━━━━━━ وظيفة إرسال الإشعارات ━━━━━━━━━━
async def send_prayer_alert(client: Client, chat_id: int, prayer: str):
    message = f"<b>- حان الآن وقت أذان {prayer} 🕌</b>"
    try:
        await client.send_message(chat_id, message, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        print(f"خطأ في إرسال الإشعار للمجموعة {chat_id}: {e}")


# ━━━━━━━━━━ المهمة الرئيسية للتشغيل التلقائي ━━━━━━━━━━
async def azan_scheduler(client: Client):
    print("🔁 بدء مهمة المراقبة للأذان...")
    while True:
        try:
            res = await get_prayer_time()  # async الآن
            if res:
                prayer_ar, prayer_time = res
                print(f"⏰ تم الكشف عن موعد أذان {prayer_ar} في {prayer_time}")

                # لكل مجموعة مفعلها الأذان - أرسل لكن تجنب التكرار في نفس الدقيقة
                for chat_id in list(azan_enabled_chats):
                    try:
                        last = _last_sent_minute.get(chat_id)
                        # إذا لم نرسل لهذه المجموعة في نفس الدقيقة بعد
                        if last != prayer_time:
                            await send_prayer_alert(client, chat_id, prayer_ar)
                            _last_sent_minute[chat_id] = prayer_time
                        else:
                            print(f"تخطي إرسال مكرر لمجموعة {chat_id} للوقت {prayer_time}")
                    except Exception as e:
                        print(f"خطأ عند معالجة مجموعة {chat_id}: {e}")

                # بعد الإرسال انتظر 65 ثانية عشان ما يعيدش مرّة ثانية في نفس الدقيقة
                await asyncio.sleep(65)
            else:
                # لا شيء الآن، ننتظر 25 ثانية قبل التحقق مرّة أخرى
                await asyncio.sleep(25)
        except Exception as e:
            print(f"خطأ في المخطط العام: {e}")
            await asyncio.sleep(30)


# تفعيل الجدولة عند تشغيل المودول — دالة آمنة لتُستدعى من main
def start_azan_task(client: Client):
    """
    استدعِ هذه الدالة بعد تشغيل الـ Client (بعد app.start())
    مثال في main.py:
        start_azan_task(app)
    """
    try:
        loop = asyncio.get_event_loop()
        # أنشئ task فقط إن لم تكن موجودة مسبقاً
        loop.create_task(azan_scheduler(client))
        print("✅ جدولة الأذان تم تفعيلها.")
    except Exception as e:
        print("start_azan_task ERROR:", e)