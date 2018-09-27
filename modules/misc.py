import hastebin
@bot.on(events.NewMessage(outgoing=True,pattern='.pip (.+)'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.pip (.+)'))
async def pipcheck(e):
	a=await e.reply('`Searching . . .`')
	r='`' + subprocess.run(['pip3', 'search', e.pattern_match.group(1)], stdout=subprocess.PIPE).stdout.decode() + '`'
	await a.edit(r)
@bot.on(events.NewMessage(outgoing=True,pattern='.paste'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.paste'))
async def haste_paste(e):
    message=e.text
    await e.edit('`Sending to bin . . .`')
    text=str(message[7:])
    await e.edit('`Sent to bin! Check it here: `' + hastebin.post(text))
@bot.on(events.NewMessage(outgoing=True, pattern='.log'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.log'))
async def log(e):
    textx=await e.get_reply_message()
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = e.text
        message = str(message[4:])
    if LOGGER:
        await bot.send_message(LOGGER_GROUP,message)
        await e.edit("`Logged Successfully`")
@bot.on(events.NewMessage(outgoing=True, pattern='.speed'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.speed'))
async def speedtest(e):
            l=await e.reply('`Running speed test . . .`')
            k=subprocess.run(['speedtest-cli'], stdout=subprocess.PIPE)
            await l.edit('`' + k.stdout.decode()[:-1] + '`')
            await e.delete()
@bot.on(events.NewMessage(outgoing=True,pattern='.hash (.*)'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.hash (.*)'))
async def hash(e):
	hashtxt_ = e.pattern_match.group(1)
	hashtxt=open('hashdis.txt','w+')
	hashtxt.write(hashtxt_)
	hashtxt.close()
	md5=subprocess.run(['md5sum', 'hashdis.txt'], stdout=subprocess.PIPE)
	md5=md5.stdout.decode()
	sha1=subprocess.run(['sha1sum', 'hashdis.txt'], stdout=subprocess.PIPE)
	sha1=sha1.stdout.decode()
	sha256=subprocess.run(['sha256sum', 'hashdis.txt'], stdout=subprocess.PIPE)
	sha256=sha256.stdout.decode()
	sha512=subprocess.run(['sha512sum', 'hashdis.txt'], stdout=subprocess.PIPE)
	subprocess.run(['rm', 'hashdis.txt'], stdout=subprocess.PIPE)
	sha512=sha512.stdout.decode()
	ans='Text: `' + hashtxt_ + '`\nMD5: `' + md5 + '`SHA1: `' + sha1 + '`SHA256: `' + sha256 + '`SHA512: `' + sha512[:-1] + '`'
	if len(ans) > 4096:
		f=open('hashes.txt', 'w+')
		f.write(ans)
		f.close()
		await bot.send_file(e.chat_id, 'hashes.txt', reply_to=e.id, caption="`It's too big, in a text file and hastebin instead. `" + hastebin.post(ans[1:-1]))
		subprocess.run(['rm', 'hashes.txt'], stdout=subprocess.PIPE)
	else:
		await e.reply(ans)
@bot.on(events.NewMessage(outgoing=True,pattern='.base64 (en|de) (.*)'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.base64 (en|de) (.*)'))
async def endecrypt(e):
	if e.pattern_match.group(1) == 'en':
		lething=str(pybase64.b64encode(bytes(e.pattern_match.group(2), 'utf-8')))[2:]
		await e.reply('Encoded: `' + lething[:-1] + '`')
	else:
		lething=str(pybase64.b64decode(bytes(e.pattern_match.group(2), 'utf-8'), validate=True))[2:]
		await e.reply('Decoded: `' + lething[:-1] + '`')
@bot.on(events.NewMessage(outgoing=True, pattern='.random'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.random'))
async def randomise(e):
    r=(e.text).split()
    index=randint(1,len(r)-1)
    await e.edit("**Query: **\n`"+e.text+'`\n**Output: **\n`'+r[index]+'`')
