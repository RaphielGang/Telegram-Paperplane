# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

import pybase64
from subprocess import PIPE
from subprocess import run as runapp
from userbot import LOGGER, LOGGER_GROUP, HELPER
from userbot.events import register

@register(outgoing=True, pattern="^.hash (.*)")
async def hash(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        hashtxt_ = e.pattern_match.group(1)
        hashtxt = open("hashdis.txt", "w+")
        hashtxt.write(hashtxt_)
        hashtxt.close()
        md5 = runapp(["md5sum", "hashdis.txt"], stdout=PIPE)
        md5 = md5.stdout.decode()
        sha1 = runapp(["sha1sum", "hashdis.txt"], stdout=PIPE)
        sha1 = sha1.stdout.decode()
        sha256 = runapp(["sha256sum", "hashdis.txt"], stdout=PIPE)
        sha256 = sha256.stdout.decode()
        sha512 = runapp(["sha512sum", "hashdis.txt"], stdout=PIPE)
        runapp(["rm", "hashdis.txt"], stdout=PIPE)
        sha512 = sha512.stdout.decode()
        ans = (
            "Text: `"
            + hashtxt_
            + "`\nMD5: `"
            + md5
            + "`SHA1: `"
            + sha1
            + "`SHA256: `"
            + sha256
            + "`SHA512: `"
            + sha512[:-1]
            + "`"
        )
        if len(ans) > 4096:
            f = open("hashes.txt", "w+")
            f.write(ans)
            f.close()
            await e.client.send_file(
                e.chat_id,
                "hashes.txt",
                reply_to=e.id,
                caption="`It's too big, in a text file and hastebin instead. `"
                + hastebin.post(ans[1:-1]),
            )
            runapp(["rm", "hashes.txt"], stdout=PIPE)
        else:
            await e.reply(ans)


@register(outgoing=True, pattern="^.base64 (en|de) (.*)")
async def endecrypt(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if e.pattern_match.group(1) == "en":
            lething = str(pybase64.b64encode(bytes(e.pattern_match.group(2), "utf-8")))[
                2:
            ]
            await e.reply("Encoded: `" + lething[:-1] + "`")
        else:
            lething = str(
                pybase64.b64decode(
                    bytes(e.pattern_match.group(2), "utf-8"), validate=True
                )
            )[2:]
            await e.reply("Decoded: `" + lething[:-1] + "`")