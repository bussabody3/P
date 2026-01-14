"""


██████╗░██████╗░██████╗░
██╔══██╗╚════██╗██╔══██╗
██████╔╝░█████╔╝██║░░██║
██╔══██╗░╚═══██╗██║░░██║
██║░░██║██████╔╝██████╔╝
╚═╝░░╚═╝╚═════╝░╚═════╝░


[ = This plugin is a part from R3D Source code = ]
{"Developer":"https://t.me/Tepthon"}

"""

import random, re, time, pytz
from datetime import datetime
from threading import Thread
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from helpers.Ranks import *
from helpers.Ranks import isLockCommand

default_welcome = """**لا تُسِئ اللفظ وإن ضَاق عليك الرَّد

ɴᴀᴍᴇ ⌯ {الاسم}
ᴜѕᴇʀɴᴀᴍᴇ ⌯ {اليوزر}
𝖣𝖺𝗍𝖾 ⌯ {التاريخ}**"""


@Client.on_message(filters.group & filters.text, group=29)
def setWelcomeHandler(c, m):
    k = r.get(f"{Dev_Zaid}:botkey")
    Thread(target=welcomeFunc, args=(c, m, k)).start()


def welcomeFunc(c, m, k):
    if not r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        return
    if r.get(f"{m.chat.id}:mute:{Dev_Zaid}") and not admin_pls(
        m.from_user.id, m.chat.id
    ):
        return
    if r.get(f"{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}"):
        return
    if r.get(f"{m.from_user.id}:mute:{Dev_Zaid}"):
        return
    if r.get(f"{m.chat.id}:addCustom:{m.from_user.id}{Dev_Zaid}"):
        return
    if r.get(f"{m.chat.id}addCustomG:{m.from_user.id}{Dev_Zaid}"):
        return
    if r.get(f"{m.chat.id}:delCustom:{m.from_user.id}{Dev_Zaid}") or r.get(
        f"{m.chat.id}:delCustomG:{m.from_user.id}{Dev_Zaid}"
    ):
        return
    text = m.text
    name = r.get(f"{Dev_Zaid}:BotName") if r.get(f"{Dev_Zaid}:BotName") else "رعد"
    if text.startswith(f"{name} "):
        text = text.replace(f"{name} ", "")
    if r.get(f"{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}"):
        text = r.get(f"{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}")
    if r.get(f"Custom:{Dev_Zaid}&text={text}"):
        text = r.get(f"Custom:{Dev_Zaid}&text={text}")
    if isLockCommand(m.from_user.id, m.chat.id, text):
        return
    if text == "الغاء" and r.get(f"{m.chat.id}:setWelcome:{m.from_user.id}{Dev_Zaid}"):
        r.delete(f"{m.chat.id}:setWelcome:{m.from_user.id}{Dev_Zaid}")
        return m.reply(f"{k} ابشر لغيت وضع الترحيب")

    if text == "الغاء" and r.get(f"{m.chat.id}:setRules:{m.from_user.id}{Dev_Zaid}"):
        r.delete(f"{m.chat.id}:setRules:{m.from_user.id}{Dev_Zaid}")
        return m.reply(f"{k} ابشر لغيت وضع القوانين")

    if r.get(f"{m.chat.id}:setRules:{m.from_user.id}{Dev_Zaid}") and mod_pls(
        m.from_user.id, m.chat.id
    ):
        r.set(f"{m.chat.id}:CustomRules:{Dev_Zaid}", m.text.html)
        r.delete(f"{m.chat.id}:setRules:{m.from_user.id}{Dev_Zaid}")
        return m.reply(f"{k} تم حطيتها")

    if r.get(f"{m.chat.id}:setWelcome:{m.from_user.id}{Dev_Zaid}") and mod_pls(
        m.from_user.id, m.chat.id
    ):
        r.set(f"{m.chat.id}:CustomWelcome:{Dev_Zaid}", m.text.html)
        r.delete(f"{m.chat.id}:setWelcome:{m.from_user.id}{Dev_Zaid}")
        return m.reply(f"{k} تم وسوينا الترحيب ياعيني")

    if text == "مسح القوانين":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            r.delete(f"{m.chat.id}:CustomRules:{Dev_Zaid}")
            return m.reply(f"{k} من عيوني مسحت القوانين")

    if text == "وضع قوانين":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            r.set(f"{m.chat.id}:setRules:{m.from_user.id}{Dev_Zaid}", 1)
            return m.reply(f"{k} ارسل القوانين الحين")

    if text == "الترحيب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:CustomWelcome:{Dev_Zaid}"):
                return m.reply(f"`{default_welcome}`")
            else:
                welcome = r.get(f"{m.chat.id}:CustomWelcome:{Dev_Zaid}")
                return m.reply(f"`{welcome}`")

    if text == "مسح الترحيب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            r.delete(f"{m.chat.id}:CustomWelcome:{Dev_Zaid}")
            return m.reply(f"{k} مسحت الترحيب")

    if text == "وضع الترحيب" or text == "ضع الترحيب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            r.set(f"{m.chat.id}:setWelcome:{m.from_user.id}{Dev_Zaid}", 1)
            return m.reply("""⇜ تمام عيني  
⇜ ارسل رسالة الترحيب الحين

⇜ ملاحظة تقدر تضيف دوال للترحيب مثلا :
⇜ اظهار قوانين المجموعه  ⇠ {القوانين}  
⇜ اظهار اسم العضو ⇠ {الاسم}
⇜ اظهار اليوزر العضو ⇠ {اليوزر}
⇜ اظهار اسم المجموعه ⇠ {المجموعه} 
⇜ اظهار تاريخ دخول العضو ⇠ {التاريخ} 
⇜ اظهار وقت دخول العضو ⇠ {الوقت} 
☆
""")


@Client.on_message(filters.regex("^مميزات البوت 🎖$"), group=260)
async def features_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        text = """**⇜اهلا بك في عالم المبرمجين 🧑🏻‍💻

 𝟏- افضل بوتات حماية وميوزك 
 𝟐- الافضل بالتليجـرام بدون نزاع 🧚
 𝟑- التكامل في القوة و السرعة والأداء 
 𝟒- لتعلم البرمجه @Tepthon 



𝟓- هذا البوت يحتوي علي افضل مميزات يمكنك استخدمه في حمايه مجموعتك فقط اضف البوت لمجموعتك بصلاحيات وارسل الاوامر 🏺


• يمكنك تحميل الاغاني 📻
• حمايه المجموعات من الاباحيه والتفليش
• افضل العاب بالبوت 🎎**"""
        await m.reply(text)


# إنشاء الكيبورد الجديد (أزرار كيبورد)
keyboard_tep = ReplyKeyboardMarkup([
    ["قران", "النقشبندي"],
    ["قسم الصور", "استوري"],
    ["اقتباسات", "متحركه"],
    ["𝗬𝗼𝘂𝗧𝘂𝗯𝗲 🎞 اليوتيوب"],
    ["غنيلي"],
    ["الغاء الكيبورد 🧚‍♂️"],
    ["مميزات البوت 🎖"]
], resize_keyboard=True)

# كيبورد قسم الصور
keyboard_images = ReplyKeyboardMarkup([
    ["صور انمي", "صور شباب"],
    ["صور بنات", "متنوع"],
    ["رجوع ↩️"]
], resize_keyboard=True)

@Client.on_message(filters.command("TEP", ["/", ""]) & filters.private | filters.regex("^رجوع ↩️$"), group=88)
async def tep_keyboard_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        await m.reply("🎖 **اختار ما تريده من الازرار**", reply_markup=keyboard_tep)

@Client.on_message(filters.regex("^قسم الصور$"), group=89)
async def images_menu_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        await m.reply("🖼 **أهلاً بك في قسم الصور، اختر النوع:**", reply_markup=keyboard_images)

@Client.on_message(filters.regex("^صور انمي$"), group=90)
async def anime_images_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        rl = random.randint(2, 90)
        url = f"https://t.me/LoreBots7/{rl}"
        await m.reply_photo(url, caption="**صور انمي ⛩**")

@Client.on_message(filters.regex("^صور شباب$"), group=91)
async def shabab_images_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        rl = random.randint(1, 90)
        url = f"https://t.me/vgbmm/{rl}"
        await m.reply_photo(url, caption="**صور شباب 🙎🏻‍♂️**")

@Client.on_message(filters.regex("^صور بنات$"), group=92)
async def banat_images_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        rl = random.randint(2, 54)
        url = f"https://t.me/vvyuol/{rl}"
        await m.reply_photo(url, caption="**صور بنات 👸🏻**")

@Client.on_message(filters.regex("^متنوع$") | filters.command(["هيدرا", "هيدرات"], ""), group=93)
async def hydra_images_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        rl = random.randint(2, 60)
        url = f"https://t.me/flflfldld/{rl}"
        await m.reply_photo(url, caption="**متنوع / هيدرات 🌀**")

@Client.on_message(filters.regex("^قران$") | filters.command(["قران", "القرآن"], ""), group=86)
async def quran_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        rl = random.randint(1, 90)
        url = f"https://t.me/opuml/{rl}"
        await m.reply_voice(url, caption="**القرآن الكريم 🕋**")

@Client.on_message(filters.regex("^النقشبندي$") | filters.command(["الشيخ", "النقشبندي"], ""), group=40986)
async def naqshbandi_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        rl = random.randint(1, 90)
        url = f"https://t.me/ggcnjj/{rl}"
        await m.reply_voice(url, caption="**الشيخ سيد النقشبندي ✨**")

@Client.on_message(filters.regex("^استوري$") | filters.command(["استوري"], ""), group=1209)
async def story_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        rl = random.randint(1, 50)
        url = f"https://t.me/yoipopl/{rl}"
        await m.reply_video(url, caption="**استوري 🎬**")

@Client.on_message(filters.regex("^اقتباسات$") | filters.command(["اقتباس", "اقتباسات"], ""), group=30605)
async def quotes_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        rl = random.randint(2, 90)
        url = f"https://t.me/LoreBots9/{rl}"
        await m.reply_photo(url, caption="**اقتباس راقي ✨**")

@Client.on_message(filters.regex("^متحركه$") | filters.command(["متحركه"], ""), group=5090)
async def gif_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        rl = random.randint(2, 90)
        url = f"https://t.me/GifWaTaN/{rl}"
        await m.reply_animation(url, caption="**متحركه 🎬**")

@Client.on_message(filters.regex("^غنيلي$") | filters.command(["غني", "غنيلي"], ""), group=765432)
async def sing_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        rl = random.randint(3, 267)
        url = f"https://t.me/bsmaatt/{rl}"
        await m.reply_audio(url, caption="**تم اختيار أغنية لك ✨**")

@Client.on_message(filters.regex("^𝗬𝗼𝘂𝗧𝘂𝗯𝗲 🎞 اليوتيوب$"), group=87654)
async def youtube_info_handler(c: Client, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE or r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        text = """『  اليوتيوب 🎞 𝗬𝗼𝘂𝗧𝘂𝗯𝗲  』
ٴ⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
يتميـز البـوت بـ تحميـل عالـي السـرعـة وبلا حـدود من اليـوتيـوب 🛸

- لـ تحميـل المقـاطع الصوتيـه 🎧 ارسـل
(بحث) + اسـم الاغنيـه

- لـ البحث عن روابـط 🖇 ارسـل
(ابحث) + كلمـه او نـص

ٴ⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆"""
        await m.reply(text)

@Client.on_message(filters.regex("^الغاء الكيبورد 🧚‍♂️$") & filters.private, group=5765870)
async def remove_keyboard_handler(c: Client, m: Message):
    await m.reply("**تم إلغاء الكيبورد بنجاح ✅**", reply_markup=ReplyKeyboardRemove())

@Client.on_message(group=4)
async def welcomeRespons(c: Client, m: Message):
    if not r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        return
    k = r.get(f"{Dev_Zaid}:botkey")
    channel = (
        r.get(f"{Dev_Zaid}:BotChannel") if r.get(f"{Dev_Zaid}:BotChannel") else "Tepthon"
    )
    
    # Check if this is a video chat invitation (often comes as service message)
    if hasattr(m, "video_chat_invited_members") and m.video_chat_invited_members:
        inviter = m.from_user
        inviter_name = f"[{inviter.first_name}](tg://user?id={inviter.id})" if inviter else "مستخدم"
        for user in m.video_chat_invited_members:
            invited_name = f"[{user.first_name}](tg://user?id={user.id})"
            text = (
                f"<b>{inviter.first_name if inviter else 'المكالمة'}</b>\n"
                f"قام {inviter_name} بدعوة {invited_name} للمحادثة المرئية\n\n"
                f"- قام {inviter_name}\n"
                f"- بدعوة : {invited_name}"
            )
            try:
                await m.reply(text, disable_web_page_preview=True)
            except:
                pass
        return

    if not r.get(f"{m.chat.id}:disableWelcome:{Dev_Zaid}") and m.new_chat_members:
        if not r.get(f"{m.chat.id}:CustomWelcome:{Dev_Zaid}"):
            welcome = default_welcome
        else:
            welcome = r.get(f"{m.chat.id}:CustomWelcome:{Dev_Zaid}")
        
        # استخدام الكيبورد الموحد
        keyboard = keyboard_tep

        for me in m.new_chat_members:
            if not me.id == int(Dev_Zaid):
                if r.get(f"{m.chat.id}:enableVerify:{Dev_Zaid}") and not pre_pls(
                    me.id, m.chat.id
                ):
                    return
                photo = None
                if not r.get(f"{m.chat.id}:disableWelcomep:{Dev_Zaid}") and me.photo:
                    try:
                        async for p in c.get_chat_photos(me.id, limit=1):
                            photo = p.file_id
                    except:
                        photo = None
                title = m.chat.title
                name = me.first_name
                if me.username:
                    username = f"@{me.username}"
                else:
                    username = f"@{channel}"
                TIME_ZONE = "Asia/Riyadh"
                ZONE = pytz.timezone(TIME_ZONE)
                TIME = datetime.now(ZONE)
                clock = TIME.strftime("%I:%M %p")
                date = TIME.strftime("%d/%m/%Y")
                if r.get(f"{m.chat.id}:CustomRules:{Dev_Zaid}"):
                    rules = r.get(f"{m.chat.id}:CustomRules:{Dev_Zaid}")
                else:
                    rules = """{k} ممنوع نشر الروابط 
{k} ممنوع التكلم او نشر صور اباحيه 
{k} ممنوع اعاده توجيه 
{k} ممنوع العنصرية بكل انواعها 
{k} الرجاء احترام المدراء والادمنيه"""
                w = (
                    welcome.replace("{القوانين}", rules)
                    .replace("{الاسم}", name)
                    .replace("{المجموعه}", title)
                    .replace("{الوقت}", clock)
                    .replace("{التاريخ}", date)
                    .replace("{اليوزر}", username)
                )
                
                if not photo:
                    video = r.get(f"{Dev_Zaid}:WelcomeVideo")
                    if video:
                        try:
                            await m.reply_video(video, caption=w, reply_markup=keyboard)
                            continue
                        except:
                            pass
                    await m.reply(w, disable_web_page_preview=True, reply_markup=keyboard)
                else:
                    await m.reply_photo(photo, caption=w, reply_markup=keyboard)
