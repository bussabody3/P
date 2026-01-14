import asyncio
from pyrogram import Client, filters
from config import r, Dev_Zaid
from helpers.Ranks import admin_pls

# Tracker for running cleaning tasks: {chat_id: task}
cleaning_tasks = {}

async def cleaner_worker(c, chat_id, interval):
    while r.get(f"{chat_id}:cleaner_active:{Dev_Zaid}"):
        await asyncio.sleep(interval)
        try:
            # Delete media: photos, stickers, voice, video, animations (GIF)
            async for message in c.get_chat_history(chat_id, limit=100):
                if message.media:
                    if message.photo or message.sticker or message.voice or                        message.video or message.animation or message.audio:
                        try:
                            await message.delete()
                        except:
                            continue
        except Exception as e:
            print(f"Cleaner error in {chat_id}: {e}")

@Client.on_message(filters.regex("^تفعيل التنظيف (\d+)$") & filters.group, group=88)
async def enable_cleaner(c, m):
    if not admin_pls(m.from_user.id, m.chat.id):
        return await m.reply("⇜ عذراً، هذا الأمر للمشرفين فقط.")
    
    interval = int(m.matches[0].group(1))
    if interval < 1:
        return await m.reply("⇜ عذراً، يجب أن يكون الوقت أكثر من دقيقة واحدة.")
    
    # Store settings
    r.set(f"{m.chat.id}:cleaner_active:{Dev_Zaid}", "1")
    r.set(f"{m.chat.id}:cleaner_interval:{Dev_Zaid}", interval)
    
    # Cancel existing task if any
    if m.chat.id in cleaning_tasks:
        cleaning_tasks[m.chat.id].cancel()
    
    # Start new worker
    task = asyncio.create_task(cleaner_worker(c, m.chat.id, interval * 60))
    cleaning_tasks[m.chat.id] = task
    
    await m.reply(f"⇜ تم تفعيل التنظيف التلقائي بنجاح ✅\n⇜ سيتم مسح الوسائط كل {interval} دقيقة.")

@Client.on_message(filters.regex("^تعطيل التنظيف$") & filters.group, group=89)
async def disable_cleaner(c, m):
    if not admin_pls(m.from_user.id, m.chat.id):
        return await m.reply("⇜ عذراً، هذا الأمر للمشرفين فقط.")
    
    r.delete(f"{m.chat.id}:cleaner_active:{Dev_Zaid}")
    
    if m.chat.id in cleaning_tasks:
        cleaning_tasks[m.chat.id].cancel()
        del cleaning_tasks[m.chat.id]
    
    await m.reply("⇜ تم تعطيل التنظيف التلقائي بنجاح ✅")
