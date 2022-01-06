import os
import discord
from discord.ext import commands
from replit import db
import asyncio
from ping import keep_alive

bot = commands.Bot(command_prefix="-")

guide = 'To add task type -add "<task>" Eg. -add "Study for Gre"\n' 

@bot.event
async def on_connect():
  print("I am ready")


try :
  task = db["task"].value
  count = db["count"]
except :
  db["task"] = []
  db["count"] = 0

bot.remove_command("help")

@bot.command()
async def todo(ctx):
    global embed
    global message
    global task
    global count
    start =""
    if ctx.guild != None :
      channel = str(ctx.guild)
    else :
      channel = str(ctx.author)
    try :
      task = db[channel + "task"].value
      count = db[channel + "count"]
    except :
      db[channel + "task"] = []
      db[channel + "count"] = 0

    for x in range(len(task)):
        start += "["+str(x)+"] " + task[x]+ "\n"
    if len(task) == 0 :
        start_desc = ""
    else :
      start_desc = "```css\n"+start+"\n```"
    embed=discord.Embed(title=channel+"'s TODO (" + str(count) +"/" + str(len(task)) + ")", description=guide + start_desc + "\n",color=0x0000)
    embed.set_footer(text = "Click on ❌ to close the list")
    message = await ctx.send(embed=embed)
    await message.add_reaction("❌")

@bot.command()
async def add(ctx,args):
  global task
  if ctx.guild != None :
      channel = str(ctx.guild)
  else :
      channel = str(ctx.author)
  try :
      task = db[channel + "task"].value
      count = db[channel + "count"]
  except :
      db[channel + "task"] = []
      db[channel + "count"] = 0
  
  task.append(args)
  db[channel + "task"] = task
  value = ""
  for x in range(len(task)):
    value += "["+str(x)+"] " + task[x]+ "\n"
  desc = "```css\n"+value +"```"
  new_embed=discord.Embed(title=channel+"'s TODO (" +str(count) +"/"+ str(len(task)) + ")", description=desc + "\n",color=0x0000)
  new_embed.set_footer(text = "Click on ❌ to close the list")
  await message.edit(embed=new_embed)
  if str(ctx.channel.type) != "private":
    await asyncio.sleep(5)
    await ctx.message.delete()

@bot.command()
async def delete(ctx,args):
  global task
  global count
  if ctx.guild != None :
      channel = str(ctx.guild)
  else :
      channel = str(ctx.author)
  try :
    task = db[channel + "task"].value
    count = db[channel + "count"]
  except :
      db[channel + "task"] = []
      db[channel + "count"] = 0
  
  if "-" in args:
    dlt = args.split("-")
    for i in range(int(dlt[0]),int(dlt[1])+1) :
      if "✔" in task[int(dlt[0])] :
        count -= 1
      task.pop(int(dlt[0]))
  else : 
    if "✔" in task[int(args)] :
        count -= 1
    task.pop(int(args))
  db[channel +"task"] = task
  db[channel +"count"] = count
  value = ""
  for x in range(len(task)):
    value += "["+str(x)+"] " + task[x]+ "\n"
  if len(task) == 0 :
    desc = ""
  else :
    desc = "```css\n"+value +"```"
  new_embed=discord.Embed(title=channel+"'s TODO (" + str(count) +"/"+ str(len(task)) + ")", description=desc+ "\n",color=0x0000)
  new_embed.set_footer(text = "Click on ❌ to close the list")
  await message.edit(embed=new_embed)
  if str(ctx.channel.type) != "private":
    await asyncio.sleep(5)
    await ctx.message.delete()

@bot.command()
async def done(ctx,args):
  global count
  global task
  if ctx.guild != None :
      channel = str(ctx.guild)
  else :
      channel = str(ctx.author)
  try :
    task = db[channel + "task"].value
    count = db[channel + "count"]
  except :
      db[channel + "task"] = []
      db[channel + "count"] = 0

  if "-" in args:
    dlt = args.split("-")
    for i in range(int(dlt[0]),int(dlt[1])+1) :
      if "✔" in task[i] :
        await ctx.send("Task "+str(i)+ " already completed")
      else:
        task[i] = task[i] + "   ✔"
        count +=1
  else :
    if "✔" in task[int(args)] :
      await ctx.send("Task "+args+ " already completed") 
    else:
      task[int(args)] = task[int(args)] + "   ✔"
      count +=1
  db[channel+"task"] = task
  value = ""
  for x in range(len(task)):
    value += "["+str(x)+"] " + task[x]+ "\n"
  if len(task) == 0 :
    desc = ""
  else :
    desc = "```css\n"+value +"```"
  db[channel+"count"] = count
  new_embed=discord.Embed(title=channel+"'s TODO (" + str(count) +"/"+ str(len(task)) + ")", description=desc+ "\n",color=0x0000)
  new_embed.set_footer(text = "Click on ❌ to close the list")
  await message.edit(embed=new_embed)
  if str(ctx.channel.type) != "private":
    await asyncio.sleep(5)
    await ctx.message.delete()      

@bot.command()
async def undo(ctx,args):
  global count
  global task
  if ctx.guild != None :
      channel = str(ctx.guild)
  else :
      channel = str(ctx.author)
  try :
    task = db[channel + "task"].value
    count = db[channel + "count"]
  except :
      db[channel + "task"] = []
      db[channel + "count"] = 0

  if "-" in args:
    dlt = args.split("-")
    for i in range(int(dlt[0]),int(dlt[1])+1) :
      if "✔" in task[i] :
        new = task[i].split("✔")
        task[i] = new[0].strip()
        count -=1     
      else:
        await ctx.send("Task "+str(i)+ " yet to be completed")
  else :
    if "✔" in task[int(args)] :
      new = task[int(args)].split("✔")
      task[int(args)] = new[0].strip()
      count -=1    
    else:
      await ctx.send("Task "+args+ " yet to be completed")
  db[channel+"task"] = task
  value = ""
  for x in range(len(task)):
    value += "["+str(x)+"] " + task[x]+ "\n"
  if len(task) == 0 :
    desc = ""
  else :
    desc = "```css\n"+value +"```"
  db[channel+"count"] = count
  new_embed=discord.Embed(title=channel+"'s TODO (" + str(count) +"/"+ str(len(task)) + ")", description=desc+ "\n",color=0x0000)
  new_embed.set_footer(text = "Click on ❌ to close the list")
  await message.edit(embed=new_embed)
  if str(ctx.channel.type) != "private":
    await asyncio.sleep(5)
    await ctx.message.delete()

@bot.command()
async def edit(ctx,*args):
  global task
  global count
  if ctx.guild != None :
      channel = str(ctx.guild)
  else :
      channel = str(ctx.author)
  try :
    task = db[channel + "task"].value
    count = db[channel + "count"]
  except :
      db[channel + "task"] = []
      db[channel + "count"] = 0

  if "✔" in task[int(args[0])] :
    await ctx.send("You cannot edit completed task . Use -add to create new task")
  else:
    task[int(args[0])] = args[1]

  db[channel+"task"] = task
  value = ""
  for x in range(len(task)):
    value += "["+str(x)+"] " + task[x]+ "\n"
  if len(task) == 0 :
    desc = ""
  else :
    desc = "```css\n"+value +"```"
  new_embed=discord.Embed(title=channel+"'s TODO (" + str(count) +"/"+ str(len(task)) + ")", description=desc+ "\n",color=0x0000)
  new_embed.set_footer(text = "Click on ❌ to close the list")
  await message.edit(embed=new_embed)
  if str(ctx.channel.type) != "private":
    await asyncio.sleep(5)
    await ctx.message.delete()




@bot.command()
async def help(ctx):
  hlp = '```ini\n[-todo] - To view task list\n\n[-add <task>] -To add task in the list\n\n[-delete <task index>] -  To remove task from the list\n\n[-delete <task index>-<task index>] - To delete multiple tasks in the list\n\n[-done <task index>] - To mark task completed in the list\n\n[-done <task index>-<task index>] - To mark multiple tasks completed in the list\n\n[-undo <task index>] - To unmark completed task in the list to set as not completed\n\n[-undo <task index>-<task index>] - To unmark multiple completed task in the list to set as not completed\n\n[-edit <task index> <task>] - To edit uncompleted task in the list Eg. -edit 3 "hello world"\n\n[-reset] - To reset the Todo list . Use -todo to create new list\n```'
  help_embed=discord.Embed(title="Help:", description=hlp, color=0xFF5733)
  await ctx.send(embed=help_embed)

@bot.command()
async def reset(ctx):
  
  global task
  global count
  if ctx.guild != None :
      channel = str(ctx.guild)
  else :
      channel = str(ctx.author)
  db[channel+"task"] = []
  db[channel+"count"] = 0
  task = db[channel+"task"].value
  count = db[channel+"count"]

@bot.event
async def on_guild_join(guild):
    join_embed=discord.Embed(title="**======== *Thanks For Adding Me!* ========**", description=f"Thanks for adding me to {guild.name}! You can use the `-help` command to get started!", color=0xd89522)
    await guild.text_channels[0].send(embed=join_embed)

@bot.event
async def on_raw_reaction_add(payload):
  if payload.user_id != message.author.id and payload.emoji.name == "❌" and payload.message_id == message.id :
    await message.delete()

keep_alive()
bot.run(os.environ['KEY'])