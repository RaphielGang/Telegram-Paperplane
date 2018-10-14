import inspect
import hastebin
@bot.on(events.NewMessage(outgoing=True, pattern='.eval'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.eval'))
async def evaluate(e):
    evaluation = eval(e.text[6:])
    if inspect.isawaitable(evaluation):
       evaluation = await evaluation
    if evaluation:
      if len(evaluation) > 4096:
          f=open('sender.txt', 'w+')
          f.write(evaluation)
          f.close()
          await bot.send_file(e.chat_id, 'sender.txt', reply_to=e.id, caption="`It's too big to send as text, sent to hastebin: `" + hastebin.post(evaluation[1:-1]))
          subprocess.run(['rm', 'sender.txt'], stdout=subprocess.PIPE)
      await e.edit("**Query: **\n`"+e.text[6:]+'`\n**Result: **\n`'+str(evaluation)+'`')
    else:
      await e.edit("**Query: **\n`"+e.text[6:]+'`\n**Result: **\n`No Result Returned/False`')
    if LOGGER:
      await bot.send_message(LOGGER_GROUP,"Eval query "+e.text[6:]+" was executed successfully")
@bot.on(events.NewMessage(outgoing=True, pattern=r'.exec (.*)'))
async def run(e):
 code = e.raw_text[5:]
 exec(
  f'async def __ex(e): ' +
  ''.join(f'\n {l}' for l in code.split('\n'))
 )
 result = await locals()['__ex'](e)
 if result:
      if len(result) > 4096:
          f=open('sender.txt', 'w+')
          f.write(result)
          f.close()
          await bot.send_file(e.chat_id, 'sender.txt', reply_to=e.id, caption="`It's too big to send as text, sent to hastebin: `" + hastebin.post(result[1:-1]))
          subprocess.run(['rm', 'sender.txt'], stdout=subprocess.PIPE)
      await e.edit("**Query: **\n`"+e.text[5:]+'`\n**Result: **\n`'+str(result)+'`')
 else:
  await e.edit("**Query: **\n`"+e.text[5:]+'`\n**Result: **\n`'+'No Result Returned/False'+'`')
 if LOGGER:
     await bot.send_message(LOGGER_GROUP,"Exec query "+e.text[5:]+" was executed successfully")
@bot.on(events.NewMessage(outgoing=True, pattern='.term'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.term'))
async def terminal_runner(e):
    message=e.text
    command = str(message)
    list_x=command.split(' ')
    result=subprocess.run(list_x[1:], stdout=subprocess.PIPE)
    result=str(result.stdout.decode())
    if len(result) > 4096:
        f=open('sender.txt', 'w+')
        f.write(result)
        f.close()
        await bot.send_file(e.chat_id, 'sender.txt', reply_to=e.id, caption="`It's too big to send as text, sent to hastebin: `" + hastebin.post(result[1:-1]))
        subprocess.run(['rm', 'sender.txt'], stdout=subprocess.PIPE)
    await e.edit("**Query: **\n`"+str(command[6:])+'`\n**Output: **\n`'+result+'`')
    if LOGGER:
        await bot.send_message(LOGGER_GROUP,"Terminal Command "+ str(list_x[1:])+" was executed sucessfully")
