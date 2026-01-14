from pyrogram import Client, filters
from pyrogram.types import ChatPrivileges
from config import r, Dev_Zaid
from helpers.Ranks import admin_pls
import time

# Dictionary to track kicks: {chat_id: {user_id: [timestamps]}}
kick_tracker = {}

@Client.on_chat_member_updated()
async def antiselfkill_handler(c, m):
    if not m.new_chat_member or m.new_chat_member.status != "left":
        return
    
    if not r.get(f'{m.chat.id}:antiselfkill:{Dev_Zaid}'):
        return

    # Check who performed the action
    async for entry in c.get_chat_event_log(m.chat.id, limit=1):
        if entry.action == "member_kicked":
            admin = entry.user
            target = entry.old_chat_member.user
            
            # If the kicked person is a bot or the admin is the bot owner/bot itself, skip
            if target.is_bot or admin.is_self:
                return

            # Check if admin is a bot-promoted admin (this logic depends on how the bot stores its admins)
            # For simplicity, we check if they have specific bot ranks
            is_bot_admin = r.get(f'{m.chat.id}:rankADMIN:{admin.id}{Dev_Zaid}') or \
                          r.get(f'{m.chat.id}:rankMOD:{admin.id}{Dev_Zaid}') or \
                          r.get(f'{m.chat.id}:rankOWNER:{admin.id}{Dev_Zaid}')

            # Message in group
            await c.send_message(
                m.chat.id,
                f"⇜ تم طرد المستخدم: {target.mention}\n⇜ الايدي: `{target.id}`\n⇜ بواسطة: {admin.mention}\n\n☆"
            )

            # Message to bot owner
            owner_id = r.get(f'{Dev_Zaid}botowner')
            if owner_id:
                try:
                    await c.send_message(
                        int(owner_id),
                        f"مرحبا يا مالكي لقد قام هذا المشرف بطرد شخص ما\n- المشرف {admin.mention}"
                    )
                except:
                    pass

            # Anti-Selfkill Logic: 5 kicks in 20 seconds
            now = time.time()
            if m.chat.id not in kick_tracker:
                kick_tracker[m.chat.id] = {}
            if admin.id not in kick_tracker[m.chat.id]:
                kick_tracker[m.chat.id][admin.id] = []
            
            # Clean old timestamps
            kick_tracker[m.chat.id][admin.id] = [t for t in kick_tracker[m.chat.id][admin.id] if now - t <= 20]
            kick_tracker[m.chat.id][admin.id].append(now)

            if len(kick_tracker[m.chat.id][admin.id]) >= 5:
                # Demote the admin
                try:
                    await c.promote_chat_member(
                        chat_id=m.chat.id,
                        user_id=admin.id,
                        privileges=ChatPrivileges(
                            can_manage_chat=False,
                            can_delete_messages=False,
                            can_manage_video_chats=False,
                            can_restrict_members=False,
                            can_promote_members=False,
                            can_change_info=False,
                            can_invite_users=False,
                            can_pin_messages=False
                        )
                    )
                    await c.send_message(
                        m.chat.id,
                        f"⇜ المشرف {admin.mention} قام بتصفية المجموعة (طرد 5 أشخاص في 20 ثانية)\n⇜ تم تنزيله من الإشراف بنجاح ✅"
                    )
                except Exception as e:
                    await c.send_message(
                        m.chat.id,
                        f"⇜ فشل في تنزيل المشرف {admin.mention}\n⇜ الخطأ: {e}"
                    )
                # Clear tracker for this admin
                kick_tracker[m.chat.id][admin.id] = []
