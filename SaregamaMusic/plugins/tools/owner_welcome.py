from pyrogram import filters
from pyrogram.types import Message
from AnonMusic import app  


# ==========================
# 💠 SPECIAL ENTRY SETTINGS
# ==========================

SPECIAL_MEMBERS = {
    8449801101: {
        "type": "developer",
        "photo": "https://files.catbox.moe/68k07i.jpg",
        "caption": (
            "✨ ʀᴏʏᴀʟ ᴇɴᴛʀʏ ᴀʟᴇʀᴛ ✨\n\n"
            "┏━━━━━━━━━━━━━━━━━━━┓\n"
            "✨ ᴡᴇʟᴄᴏᴍᴇ ᴍᴀᴊᴇsᴛɪᴄ ᴅᴇᴠᴇʟᴏᴘᴇʀ\n"
            "┗━━━━━━━━━━━━━━━━━━┛\n\n"

            "ᴛɴᴄ // ɴᴇᴛᴡᴏʀᴋ ➜ @TNCnetwork\n"
            "ᴛɴᴄ || ᴍᴇᴇᴛᴜᴘ ➜ @TNCmeetups\n\n"
            "🌟 ʟɪᴋᴇ ᴀ ᴋɪɴɢ ɪɴ ʜɪs ᴘᴀʟᴀᴄᴇ, ʏᴏᴜʀ ᴄᴏᴅᴇ ʀᴜʟᴇs ᴛʜᴇ ʀᴇᴀʟᴍ 🌟\n"
            "ʟᴏɴɢ ʟɪᴠᴇ ᴛʜᴇ ᴅᴇᴠ"
        ),
    },
    8280692222: {
        "type": "owner",
        "photo": "https://files.catbox.moe/mwwc4o.jpg",
        "caption": (
            "⚠️ 𝐎ᴡɴᴇʀ 𝐀ʟᴇʀᴛ ⚠️\n\n"
            "┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
            "✨ ᴛʜᴇ ʜᴇᴀʀᴛ ᴏғ ᴏᴜʀ ᴄᴏᴍᴍᴜɴɪᴛʏ ✨\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
            "ᴛɴᴄ // ɴᴇᴛᴡᴏʀᴋ ➜ @TNCnetwork\n"
            "ᴛɴᴄ || ᴍᴇᴇᴛᴜᴘ ➜ @TNCmeetups\n\n"
            "ʏᴏᴜʀ ᴘʀᴇsᴇɴᴄᴇ ʙʀɪɴɢs ᴘᴏsɪᴛɪᴠɪᴛʏ,\n"
            "ʏᴏᴜʀ ᴠɪsɪᴏɴ ɢᴜɪᴅᴇs ᴜs ᴛᴏ ɢʀᴇᴀᴛɴᴇss.\n"
            "🤍 ᴡᴇ ᴀʀᴇ ɢʀᴀᴛᴇғᴜʟ ᴛᴏ ʜᴀᴠᴇ ʏᴏᴜ ᴀᴍᴏɴɢ ᴜs."
        ),
    },
}


# ==========================
# ⚡ SPECIAL WELCOME HANDLER
# ==========================

@app.on_message(filters.new_chat_members)
async def handle_special_member(client, message: Message):
    """Send spoiler photo welcome when special users join."""
    for member in message.new_chat_members:
        special = SPECIAL_MEMBERS.get(member.id)
        if not special:
            continue  # Skip normal members

        try:
            # Send spoiler image (hidden preview until tapped)
            await message.reply_photo(
                photo=special["photo"],
                caption=special["caption"],
                has_spoiler=True  # 👈 This adds the spoiler effect
            )
        except Exception as e:
            print(f"[Special Welcome Error] {e}")