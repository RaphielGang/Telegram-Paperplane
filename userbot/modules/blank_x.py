#This is the Module By Blank_X Kek!
# The SUPER chat stalk file
SCHATSTALK_LOG='/tmp/schatstalk'

# The bot restart command
RESTART_CMD='sudo systemctl restart botrun_userbot'

from os import listdir
from os.path import isfile, join
import asyncio, os, time, random
from userbot import bot, LOGGER, LOGGER_GROUP
from telethon import events
from telethon.tl.functions.messages import SendMessageRequest, ForwardMessagesRequest
from telethon.tl.functions.channels import DeleteMessagesRequest

cstalk = None
delall = False
dt = False
announcelive = '/tmp'
bcool = False

@bot.on(events.NewMessage(outgoing=True, pattern='^\.csse(t ?)'))
async def chatstalkset_blankx(e):
	global cstalk
	if e.pattern_match.group(1) != 't':
		cstalk=e.text[7:]
		if cstalk != 'c' and cstalk != 's':
			await e.edit('`Set chat stalk ID to ' + cstalk + '`')
		elif cstalk == 'c':
			cstalk=str(e.chat_id)
			await e.edit('`Set chat stalk ID to current chat`')
		else:
			cstalk='s'
			await e.edit('`Set chat stalk ID to `**SUPER**')
	else:
		cstalk=None
		await e.edit('`Set chat stalk ID to None`')

@bot.on(events.NewMessage)
async def chatstalk_blankx(e):
	global cstalk, announcelive
	if str(e.chat_id) == cstalk:
		await bot(ForwardMessagesRequest(from_peer=e.chat_id, id=[e.id], to_peer=LOGGER_GROUP))
	op=announcelive
	opp=[f for f in listdir(op) if isfile(join(op, f))]
	if 'to-announce' in opp:
		oppp=open(op + '/to-announce', 'r')
		opppp=oppp.readlines()
		oppp.close()
		oppp=opppp[0]
		await bot.send_message(int(oppp), '`I\'m back!`')
		os.system('rm ' + op + '/to-announce')

@bot.on(events.NewMessage(pattern='.'))
async def cssuper_blankx(e):
	global cstalk
	if cstalk == 's':
		global SCHATSTALK_LOG
		log=SCHATSTALK_LOG
		p=open(log, 'a')
		p.write(str(e.chat_id) + ': ' + str(e.from_id) + ':\n' + e.text + '\n')
		p.close()

@bot.on(events.NewMessage(outgoing=True, pattern='^\.delall (Tru|Fals)e'))
async def delallc_blankx(e):
	global delall
	if e.pattern_match.group(1) == 'Tru':
		delall = True
	else:
		delall = False
		await e.edit('`Not deleting all new messages.`')

@bot.on(events.NewMessage(outgoing=True, pattern='^\.dt .+'))
async def dt_blankx(e):
	await e.edit(e.text[4:])
	global dt
	dt = True

@bot.on(events.NewMessage(outgoing=True))
async def delall_blankx(e):
	global delall, dt
	if delall == True and dt == False:
		await e.delete()
		await bot.send_message(LOGGER_GROUP, 'You seem to have sent a message while delete all is True, please disable.')
	if dt == True:
		dt = False

@bot.on(events.NewMessage(outgoing=True, pattern='^\.cs$'))
async def cs_blankx(e):
	global cstalk
	ori='`Chat stalk ID: '
	if str(e.chat_id) == cstalk:
		ori+='current chat'
	elif cstalk != 's':
		ori+=str(cstalk)
	else:
		ori+='`**SUPER**'
	if cstalk != 's':
		ori+='`'
	await e.edit(ori)

@bot.on(events.NewMessage(outgoing=True, pattern='^\.(f?t)imer '))
async def timer_blankx(e):
	txt=e.text[7:] + '\nDeleting in '
	j=10
	k=j
	for j in range(j):
		await e.edit(txt + str(k))
		k=k-1
		await asyncio.sleep(1)
	if e.pattern_match.group(1) == 't':
		await e.delete()
	else:
		await e.edit(txt + 'NaN')

@bot.on(events.NewMessage(outgoing=True, pattern='^\.stimer '))
async def stimer_blankx(e):
	await e.edit(e.text[7:])
	await asyncio.sleep(10)
	await e.delete()

@bot.on(events.NewMessage(outgoing=True, pattern='^\.(f?t)ime$'))
async def time_blankx(e):
	if e.reply_to_msg_id != None:
		thed='Deleting replied to message in '
		j=10
		k=j
		for j in range(j):
			await e.edit(thed + str(k))
			k=k-1
			await asyncio.sleep(1)
		if e.pattern_match.group(1) == 't':
			await bot.delete_messages(e.input_chat, [e.reply_to_msg_id, e.id])
		else:
			await e.edit(thed + 'NaN')

@bot.on(events.NewMessage(outgoing=True, pattern='^\.stime$'))
async def stime_blankx(e):
	await e.delete()
	if e.reply_to_msg_id != None:
		await asyncio.sleep(10)
		await bot.delete_messages(e.input_chat, [e.reply_to_msg_id])

@bot.on(events.NewMessage(outgoing=True, pattern='^\.sedit '))
async def sedit_blankx(e):
	await e.edit('s/\X+/' + e.text[7:])
	await e.delete()

@bot.on(events.NewMessage(outgoing=True, pattern='^\.sedita '))
async def sedit_blankx(e):
	await e.delete()
	if e.reply_to_msg_id != None:
		f=await bot.send_message(await bot.get_input_entity(e.chat_id), message='s/((.+|\\n+))+/' + e.text[8:], reply_to=e.reply_to_msg_id)
		await asyncio.sleep(0.25)
		await f.delete()

@bot.on(events.NewMessage(outgoing=True, pattern='^\.send (.*? )'))
async def send_blankx(e):
	usir=e.pattern_match.group(1)[:-1]
	skep=7+len(usir)
	ttxt=e.raw_text[skep:]
	f=':\nUser: `' + usir + '`\nText:\n' + ttxt
	await e.edit('Sending' + f)
	thisisfine=True
	try:
		usir=int(usir)
	except:
		print('this is fine')
	try:
		await bot.send_message(await bot.get_input_entity(usir), message=ttxt)
	except:
		try:
			await bot.send_message(usir, message=ttxt)
		except:
			try:
				await bot(SendMessageRequest(peer=usir, message=ttxt))
			except:
				try:
					await bot(SendMessageRequest(peer=bot.get_input_entity(usir), message=ttxt))
				except:
					thisisfine=False
	if thisisfine == True:
		await e.edit('Sent' + f)
	else:
		await e.edit('Failed to send' + f)

@bot.on(events.NewMessage(outgoing=True, pattern='^\.edit '))
async def edit_blankx(e):
	await e.edit(e.raw_text[6:])

@bot.on(events.NewMessage(outgoing=True, pattern='^\.lchatid$'))
async def lchatid_blankx(e):
	await e.delete()
	await bot.send_message(LOGGER_GROUP, 'Chat ID by .lchatid: ' + str(e.chat_id))

@bot.on(events.NewMessage(outgoing=True, pattern='^\.restart$'))
async def restart_blankx(e):
	await e.edit('`Alrighty then.`')
	global RESTART_CMD, announcelive
	op=open(announcelive + '/to-announce', 'w+')
	op.write(str(e.chat_id))
	op.close()
	os.system(RESTART_CMD)

@bot.on(events.NewMessage(outgoing=True, pattern='^\.enviro(n .*)'))
async def environ_blankx(e):
	if len(e.raw_text) < 9:
		await e.edit('`Syntax: .environ env_var`')
	else:
		wegud=True
		try:
			op=os.environ[e.pattern_match.group(1)[2:]]
		except:
			wegud=False
		if wegud == True:
			await e.edit('**Environment variable: **`' + e.pattern_match.group(1)[2:] + '`\n**Result:**\n' + op)
		else:
			await e.edit('`Failed to get the environment ' + e.pattern_match.group(1)[2:] + '`')

@bot.on(events.NewMessage(outgoing=True, pattern='^\.sendspa(m2?)'))
async def sendspam_blankx(e):
	yeye = True
	if e.pattern_match.group(1) == 'm2':
		yeye = False
	if yeye == True:
		await e.delete()
		p=25
		for p in range(p):
			if len(e.raw_text) == 9:
				o=str(p)
			else:
				o=e.text[9:]
			r=await e.respond(o)
			await r.delete()

@bot.on(events.NewMessage(outgoing=True, pattern='^\.sendspam2'))
async def sendspam2_blankx(e):
	p=25
	o=[e.id]
	for p in range(p):
		if len(e.raw_text) == 10:
			i=str(p)
		else:
			i=e.text[10:]
		r=await e.respond(i)
		o+=[r.id]
	await bot.delete_messages(e.chat_id, o)


@bot.on(events.NewMessage(outgoing=True, pattern='^\.cool (Tru|Fals)e$'))
async def coolc_blankx(e):
	global bcool
	if e.pattern_match.group(1) == 'Tru':
		await e.edit('`Yo\' cool`')
		bcool = True
	else:
		await e.edit('Yo\' not cool')
		bcool = False

@bot.on(events.NewMessage(outgoing=True, pattern='.'))
async def cool_blankx(e):
	global bcool
	if bcool == True:
		if e.raw_text != '.cool True':
			await e.edit('```' + e.raw_text + '```')

