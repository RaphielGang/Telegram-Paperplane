from hashlib import sha512
from hmac import new
import json
import pprint
from requests import post, get
from re import sub
from time import time

from telethon.errors.rpcerrorlist import MessageEmptyError

from userbot import CMD_HELP, COINBASE_KEY, COINBASE_SECRET, bot
from userbot.events import register

@register(outgoing=True, pattern=r"^.coin (\S*) ?(\S*) ?(\S*)")
async def coin(cspot):
    """ For .coin command, control the coinspot api for managing your account. """
    if not cspot.text[0].isalpha() and cspot.text[0] not in ("/", "#", "@", "!"):
        await cspot.edit("Processing...")
    coinapi = cspot.pattern_match.group(1)
    arg1 = cspot.pattern_match.group(2)
    arg2 = cspot.pattern_match.group(3)
    arg3 = cspot.pattern_match.group(3)
    key = COINBASE_KEY
    secret = COINBASE_SECRET.encode('utf-8')
    nonce = int(time() * 1000000)

    if coinapi == "bal":
        API = "api/ro/my/balances"
        postdata = {
                'nonce': nonce,
                 }
    if coinapi == "price":
        API = "pubapi/latest"
        postdata = {
                'nonce': nonce,
                 }
    if coinapi == "send":
        API = "api/my/coin/send"
        postdata = {
                'nonce': nonce,
                'cointype': arg1,
                'address': arg2,
                'amount': arg3
                 }

    postdata = json.dumps(postdata, separators=(',', ':'))
    sign = new(secret, postdata.encode('utf-8'), sha512).hexdigest()
    headers = {
               	'Content-Type': 'application/json',
                'key': key,
                'sign': sign
               }

    if coinapi == "bal":
        r = post(f'https://www.coinspot.com.au/{API}', headers=headers, data=postdata).json()
        response = ""
        r = r['balances']
        for i in r:
            formatted = sub("[^a-zA-Z0-9\.:]", "", str(i))
            formatted = sub(":balance:", " balance: ", formatted)
            formatted = sub("audbalance:", " AUD: $", formatted)
            response += sub("rate:.*", "\n", formatted)
    elif coinapi == "price":
        r = get(f'https://www.coinspot.com.au/{API}').json()
        r = r["prices"][f"{arg1.lower()}"]["ask"]
        response = f"The current price of {arg1.upper()} in AUD is:\n`${r}`"
    else:
        response = post(f'https://www.coinspot.com.au/{API}', headers=headers, data=postdata).json()
    try:
        await cspot.edit(f"{response}")
    except MessageEmptyError:
        await cspot.edit("No funds in account.")

CMD_HELP.update({
    'crypto': ".coin <bal/price <token>/send <address>>\
    \nUsage: .coin bal\
    \nUsage: .coin price ETH\
    \nUsage: .coin send ETH <ETH address> <amount>"
})