import time
import asyncio

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from SaregamaMusic import app
from SaregamaMusic.misc import _boot_
from SaregamaMusic.plugins.sudo.sudoers import sudoers_list
from SaregamaMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from SaregamaMusic.utils import bot_sys_stats
from SaregamaMusic.utils.decorators.language import LanguageStart
from SaregamaMusic.utils.formatters import get_readable_time
from SaregamaMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string
from SaregamaMusic.misc import SUDOERS


# ==========================
# Private /start handler
# ==========================
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    # Check if start has arguments
    if len(message.text.split()) > 1:
        arg = message.text.split(None, 1)[1]

        # Help panel
        if arg.startswith("help"):
            keyboard = help_pannel(_)
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_GROUP),
                protect_content=True,
                reply_markup=keyboard,
                has_spoiler=True  # Spoiler effect
            )

        # Sudoers list
        elif arg.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} just started the bot to check <b>sudolist</b>.\n\n"
                         f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
                         f"<b>Username:</b> @{message.from_user.username}"
                )

        # YouTube info
        elif arg.startswith("inf"):
            m = await message.reply_text("🔎")
            query = arg.replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text=_["S_B_8"], url=link),
                     InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_GROUP)],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} just checked <b>track info</b>.\n\n"
                         f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
                         f"<b>Username:</b> @{message.from_user.username}"
                )

    # Default private start
    else:
        out = private_panel(_)
        UP, CPU, RAM, DISK = await bot_sys_stats()
        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["start_2"].format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM),
            reply_markup=InlineKeyboardMarkup(out),
            has_spoiler=True  # Spoiler effect
        )
        if await is_on_off(2):
            await app.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=f"{message.from_user.mention} just started the bot.\n\n"
                     f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
                     f"<b>Username:</b> @{message.from_user.username}"
            )


# ==========================
# Group /start handler
# ==========================
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
        has_spoiler=True  # Spoiler effect
    )
    await add_served_chat(message.chat.id)


# ==========================
# Welcome new chat members
# ==========================
welcome_group = 2
@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome_special(client, message: Message):
    try:
        chat_id = message.chat.id
        for member in message.new_chat_members:
            # Buttons for member
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton(text=member.first_name, user_id=member.id)]])

            # OWNER check
            if isinstance(config.OWNER_ID, int):
                if member.id == config.OWNER_ID:
                    owner_msg = f"#BOT_OWNER\n\n 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐁𝐎𝐒𝐒 💗\n\n{member.mention} Owner of {app.mention} just joined <code>{message.chat.title}</code>."
                    sent = await message.reply_text(owner_msg, reply_markup=buttons)
                    await asyncio.sleep(180)
                    await sent.delete()
                    return

            elif isinstance(config.OWNER_ID, (list, set)):
                if member.id in config.OWNER_ID:
                    owner_msg = f"#BOT_OWNER\n\n 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐁𝐎𝐒𝐒 💗\n\n{member.mention} Owner of {app.mention} just joined <code>{message.chat.title}</code>."
                    sent = await message.reply_text(owner_msg, reply_markup=buttons)
                    await asyncio.sleep(180)
                    await sent.delete()
                    return

            # SUDOERS check
            if isinstance(SUDOERS, int):
                if member.id == SUDOERS:
                    sudo_msg = f"#Sudo_User\n\n Welcome {member.mention} to {app.mention}!"
                    sent = await message.reply_text(sudo_msg, reply_markup=buttons)
                    await asyncio.sleep(180)
                    await sent.delete()
                    return

            elif isinstance(SUDOERS, (list, set)):
                if member.id in SUDOERS:
                    sudo_msg = f"#Sudo_User\n\n Welcome {member.mention} to {app.mention}!"
                    sent = await message.reply_text(sudo_msg, reply_markup=buttons)
                    await asyncio.sleep(180)
                    await sent.delete()
                    return

    except Exception as e:
        print(f"Error in welcome handler: {e}")
        return


# ==========================
# General welcome / blacklisted handling
# ==========================
@app.on_message(filters.new_chat_members, group=-1)
async def welcome_general(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            # Ban blacklisted users
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            # Bot self join
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_GROUP,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                    has_spoiler=True  # Spoiler effect
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as ex:
            print(ex)