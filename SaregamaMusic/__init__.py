import asyncio
import uvloop

# Ensure there's a running event loop before importing Pyrogram
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.set_event_loop(asyncio.new_event_loop())

# Now safe to import Pyrogram and your bot
from SaregamaMusic.core.bot import AMBOTOP
from SaregamaMusic.core.dir import dirr
from SaregamaMusic.core.git import git
from SaregamaMusic.core.userbot import Userbot
from SaregamaMusic.misc import dbb, heroku
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = AMBOTOP()
userbot = Userbot()

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()