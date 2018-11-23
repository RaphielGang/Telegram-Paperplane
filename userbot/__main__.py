ISAFK=False
ENABLE_KILLME=True
SNIPE_ID=0
MUTING_USERS={}
MUTED_USERS={}
AFKREASON="No Reason "
SPAM_ALLOWANCE=3
SPAM_CHAT_ID=[]
BRAIN_CHECKER=[]
SNIPE_TEXT=""
COUNT_MSG=0
BRAIN_CHECKER=[]
USERS={}
SPAM=False
WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
COUNT_PM={}
import importlib
from userbot.modules import ALL_MODULES
for module_name in ALL_MODULES:
    imported_module = importlib.import_module("userbot.modules." + module_name)
