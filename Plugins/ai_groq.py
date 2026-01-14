from pyrogram import Client, filters, enums
from pyrogram.types import Message
from groq import Groq
from config import r, Dev_Zaid
import asyncio

# إعداد عميل Groq
client_groq = Groq(api_key="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")

@Client.on_message(filters.regex("^بوت (.*)") | filters.command("بوت", ""), group=9988)
async def ai_handler(c: Client, m: Message):
    # التحقق من التفعيل في الخاص أو المجموعات
    if m.chat.type != enums.ChatType.PRIVATE and not r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        return

    # استخراج السؤال
    question = None
    if m.matches:
        question = m.matches[0].group(1)
    elif m.command and len(m.command) > 1:
        question = m.text.split(None, 1)[1]
    
    if not question:
        return

    # إرسال حالة "يكتب"
    await c.send_chat_action(m.chat.id, enums.ChatAction.TYPING)
    
    try:
        # طلب الإجابة من Groq (استخدام LLaMA)
        chat_completion = client_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": question,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        
        response = chat_completion.choices[0].message.content
        await m.reply(f"- الذكاء الاصطناعي LLaMA 🧙:\n\n{response}")
        
    except Exception as e:
        await m.reply(f"❌ **عذراً، حدث خطأ أثناء الاتصال بالذكاء الاصطناعي:**\n`{str(e)}`")
