# ==========================
# SAFE EVENT LOOP INITIALIZATION (Fix for Heroku)
# ==========================
import asyncio

try:
    import uvloop
    uvloop.install()
except ImportError:
    pass

# Ensure there's always an active asyncio loop in the main thread
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


# ==========================
# EXISTING PROJECT IMPORTS
# ==========================
from SaregamaMusic.core.bot import AMBOTOP
from SaregamaMusic.core.dir import dirr
from SaregamaMusic.core.git import git
from SaregamaMusic.core.userbot import Userbot
from SaregamaMusic.misc import dbb, heroku

from .logging import LOGGER

# ==========================
# CORE INITIALIZATION
# ==========================
dirr()
git()
dbb()
heroku()

app = AMBOTOP()
userbot = Userbot()

# ==========================
# PLATFORM API IMPORTS
# ==========================
from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()