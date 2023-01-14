import disnake
from disnake import Option, OptionChoice, SelectOption
from disnake.ext import commands
from disnake.ext.commands import CommandNotFound, CommandOnCooldown

import os
import copy
import asyncio
from difflib import SequenceMatcher
from datetime import datetime, timedelta, timezone

from keys import repel_loc_keys, repel_pkn_keys, headbutt_keys, items_keys, ability_keys, moves_keys, dex_keys, combined_keys, spawn_item_keys, spawn_keys, location_keys
from reminders import  reminder_data
from smogon import smogon_sets
from prefixes import prefix1
from move_pokemons import moveset_data
from learnset import learner
from keep_alive import keep_alive


from data_functions import get_ev_data, mostused_func, pro_repel, pad_with_zeros, type_check, exca, headbutt_check_func, do_item, do_moves, do_ability, dig_func1, get_data, dex_embed, smogon_embed, Poke_learnset, movesLearn, spawn_func, location_func, item_func
from dropdown_class import DropdownView

intents = disnake.Intents.none()
client = commands.Bot(command_prefix=disnake.ext.commands.when_mentioned, intents=intents)#command_prefix='^')#,test_guilds=[])

test = ['^invite', '^spawn', '^item', '^evspots', '^s', '^dex', '^learnset', '^smogon', '^repel', '^digspots', '^info', '^poketime', '^headbutt', 'excavation', '^mostused', 'types', '^exca', '^remindme']

# @client.event
# async def on_message(message):
#   if message.author == client.user:
#     return
#   if message.author.bot:
#     return
#   if any(ext in message.content.lower() for ext in test):
#     await message.channel.send("```\nPlease add the bot again from its profile and use the bot via slash commands\nDiscord wants all verifed bots to go slash commands and will be revoking all message reading capabilities from them unless the bot has a use for message data.\nIt can take upto 2 hours for the commands to sync to your server\nIf the bot has already been readded.\n```\nslash commands prefix is '/'")
#   await client.process_commands(message)

@client.slash_command(
	description = "This command shows learnset of pokemon",
	options = [
		Option("pokemon", "enter pokemon"),
		Option("move", "enter move")
	]
)
@commands.cooldown(1, 5, commands.BucketType.user)
async def learnset(ctx, pokemon = None, move = None):
	user = ctx.user
	if pokemon is None and move is None:
		await ctx.response.send_message("Please enter atleast one pokemon or move")
	elif pokemon is None and move is not None:
		move = move.lower().replace("-", "").replace(" ", "")
		if move in moveset_data.keys():
			moves = moveset_data[move]
			move_check_flag = 0
			msg = '\n'
			for data in moves:
				if len(msg) + len(data) >= 2000-6:
					msg = ''.join(['```', msg, '```'])
					move_check_flag = move_check_flag + 1
					await user.send(msg)
					msg = '\n'
				msg += data + '\n'
			if move_check_flag == 0 :
				msg = ''.join(['```', msg, '```'])
				await ctx.response.send_message(msg)
			else:
				msg = ''.join(['```', msg, '```'])
				await user.send(msg)
				if ctx.guild != None:
					await ctx.response.send_message("Sent the requested data in DM.")
		else:
			await ctx.response.send_message("Please enter a valid move")
	elif pokemon is not None and move is None:
		pokemon = pokemon.lower().replace("-", "").replace(" ", "")
		if pokemon in dex_keys.keys():
			pokemon = dex_keys[pokemon]
			pokemon_data = Poke_learnset(pokemon)
			move_check_flag = 0
			msg = '\n'
			for data in pokemon_data:
				if len(msg) + len(data) >= 2000-6:
					msg = ''.join(['```', msg, '```'])
					move_check_flag = move_check_flag + 1
					await user.send(msg)
					msg = '\n'
				msg += data + '\n'
			if move_check_flag == 0 :
				msg = ''.join(['```', msg, '```'])
				await ctx.response.send_message(msg)
			else:
				msg = ''.join(['```', msg, '```'])
				await user.send(msg)
				if ctx.guild != None:
					await ctx.response.send_message("Sent the requested data in DM.")
		else:
			await ctx.response.send_message("Please enter a valid pokemon")
	else:
		pokemon = pokemon.lower().replace("-", "").replace(" ", "")
		move = move.lower().replace("-", "").replace(" ", "")
		if pokemon in dex_keys.keys() and move in moveset_data.keys():
			pokemon = dex_keys[pokemon]
		else:
			await ctx.response.send_message("please enter a valid pokemon or move")
			return
		poke_move_learn = movesLearn(pokemon, move)
		msg = '\n'
		for data in poke_move_learn:
			if len(msg) + len(data) >= 2000-6:
				msg = ''.join(['```', msg, '```'])
				await ctx.channel.send_message(msg)
				msg = '\n'
			msg += data + '\n'
		msg = ''.join(['```', msg, '```'])
		await ctx.response.send_message(msg)


async def remind_ping(userid,time,reason):
  user = client.get_user(int(userid))
  if user is None:
    user = await client.fetch_user(int(userid))
  now = datetime.now()
  timer = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
  seconds_until_ping = (timer - now).total_seconds()
  await asyncio.sleep(seconds_until_ping)
  await user.send("Hi, you asked me to remind you about %s"%reason)
  reminder_data[userid].pop(time)
  res = not bool(reminder_data[userid])
  if res:
    reminder_data.pop(userid)
  a = open("reminders.py","w")
  a.write("reminder_data = " + str(reminder_data))
  a.close()

reminder_check = "True"

async def background_task():
  await client.wait_until_ready()
  global reminder_check
  reminder_check_data = copy.deepcopy(reminder_data)
  for key1,value1 in reminder_check_data.items():
    for key2,value2 in reminder_check_data[key1].items():
      client.loop.create_task(remind_ping(key1,key2,value2))

@client.slash_command(
  description = "reminds you of anything u want",
  options = [
    Option("time","d/h/m/s",required=True),
    Option("reminder","reminder",required=True)
  ]
)
async def remindme(ctx, time, reminder):
  user = ctx.user
  user_id = ctx.user.id
  seconds = 0
  if time.lower().endswith("d"):
    seconds += int(time[:-1]) * 60 * 60 * 24
    counter = f"{seconds // 60 // 60 // 24} days"
  elif time.lower().endswith("h"):
    seconds += int(time[:-1]) * 60 * 60
    counter = f"{seconds // 60 // 60} hours"
  elif time.lower().endswith("m"):
    seconds += int(time[:-1]) * 60
    counter = f"{seconds // 60} minutes"
  elif time.lower().endswith("s"):
    seconds += int(time[:-1])
    counter = f"{seconds} seconds"
  if seconds == 0:
    await ctx.response.send_message('Please specify a proper duration')
  else:
    await ctx.response.send_message(f"Alright, I will remind you about {reminder} in {counter}.")
    then = datetime.now() + timedelta(seconds=seconds)
    if str(user_id) in reminder_data:
      reminder_data[str(user_id)].update({"%s"%then:"%s"%reminder})
    else:
      reminder_data.update({str(user_id):{"%s"%then:"%s"%reminder}})
    a = open("reminders.py","w")
    a.write("reminder_data = " + str(reminder_data))
    a.close()
    await asyncio.sleep(seconds)
    await user.send(f"Hi, you asked me to remind you about {reminder}.")
    reminder_data[str(user_id)].pop("%s"%then)
    res = not bool(reminder_data[str(user_id)])
    if res:
      reminder_data.pop(str(user_id))
      a = open("reminders.py","w")
      a.write("reminder_data = " + str(reminder_data))
      a.close()
    return

@client.slash_command(
	description = "This command shows smogon sets of pokemon",
	options = [
		Option("pokemon", "Enter a pokemon", required = True)
	]
)
@commands.cooldown(1, 5, commands.BucketType.user)
async def smogon(ctx, pokemon):
  user = ctx.user.id
  input = pokemon.capitalize()
  if ' ' in input: input = ' '.join([input.split()[0].capitalize(), input.split()[1].capitalize()])
  elif '-' in input: input = '-'.join([input.split('-')[0].capitalize(), input.split('-')[1].capitalize()])
  test_keys = []
  if input not in smogon_sets.keys():
    for key in smogon_sets.keys():
      if SequenceMatcher(a = input, b = key).ratio() >= 0.8:
        test_keys.append(key)
    if len(test_keys) == 1:
      input = test_keys[0]
    elif len(test_keys) > 1:
      options = []
      for item in test_keys:
        options.append(SelectOption(label = item, description = 'Select this'))
      view = DropdownView(options, "smogon", "smogon", "Select one", user)
      await ctx.response.send_message('Pick Pokemon', view=view)
      return
    else:
      await ctx.response.send_message('Pokémon could not be found.')
      return

  smogonEmbed = smogon_embed(input)
  await ctx.response.send_message(embed = smogonEmbed)

@client.slash_command(
	description = "This command shows dex entries of pokemon",
	options = [
		Option("pokemon", "Enter pokemon name", required = True)
	]
)
@commands.cooldown(1, 5, commands.BucketType.user)
async def dex(ctx, pokemon):
  user = ctx.user.id
  input = pokemon.lower()
  test_keys = []
  test_values = []
  if input in dex_keys.keys():
    input = dex_keys[input]
  else:
    for key, value in dex_keys.items():
      if SequenceMatcher(a = input, b = key).ratio() >= 0.8:
        test_keys.append(key)
        test_values.append(value)
    if len(test_keys) == 1:
      input = dex_keys[test_keys[0]]
    elif len(test_keys) > 1:
      options = []
      for item in test_values:
        options.append(SelectOption(label = item, description = 'Select this'))
      view = DropdownView(options, "dex", "dex", "Select one", user)
      await ctx.response.send_message('Pick Pokemon', view=view)
      return
    else:
      await ctx.response.send_message('Pokémon could not be found.')
      return
  dexEmbed = dex_embed(input)
  if dexEmbed == None: await ctx.response.send_message('Pokémon could not be found.')
  else: await ctx.response.send_message(embed = dexEmbed)

@client.slash_command(
	description = 'This command shows items held by pokemon',
	options = [
		Option("argument", "item", required = True)
	]
)
@commands.cooldown(1,5,commands.BucketType.user)
async def item(ctx,argument):
  user = ctx.user.id
  channel = ctx.channel
  input = argument.lower()
  test_keys = []
  if input not in spawn_item_keys:
    for key in spawn_item_keys:
      if SequenceMatcher(a=input,b=key.lower()).ratio() >= 0.8:
        test_keys.append(key)
    if len(test_keys) == 1:
      input = test_keys[0]
    elif len(test_keys) > 1:
      options = []
      for item in test_keys:
        options.append(SelectOption(label=item,description='Select this'))
      view = DropdownView(options,"Item","spawns","Select one",user)
      await ctx.response.send_message('Pick item', view=view)
      return
    else:
      await ctx.response.send_message('Item could not be found.')
      return

  spawns = get_data(input, 'Item')
  if spawns == None: await ctx.response.send_message('Item could not be found.')
  else:
    msg = ''
    for data in spawns:
      if len(msg) + len(data) >= 2000-6:
        msg = ''.join(['```', msg, '```'])
        await ctx.channel.send_message(msg)
        msg = '\n'
      msg += data + '\n'
    msg = ''.join(['```', msg, '```'])
    await ctx.response.send_message(msg)

@client.slash_command(
  description = "This command shows spawns of specific pokemon/area",
  options = [
    Option("argument", "Enter a pokemon/area", required = True)
  ]
)
@commands.cooldown(1,5,commands.BucketType.user)
async def spawn(ctx,argument):
  input = argument.lower()
  user = ctx.user.id
  if input in location_keys: category = '#Pokémon'
  elif input in spawn_keys: category = '#Map'
  else:
    test_keys = []
    category = {}
    for key in spawn_keys:
      if SequenceMatcher(a=input,b=key).ratio() >= 0.8:
        test_keys.append(key)
        category.update({key:"#Pokémon"})
    for key in location_keys:
      if SequenceMatcher(a=input,b=key).ratio() >= 0.8:
        test_keys.append(key)
        category.update({key:"#Map"})
    if len(test_keys) == 1:
      input = test_keys[0]
      category = category[test_keys[0]]
    elif len(test_keys) > 1:
      options = []
      for item in test_keys:
        options.append(SelectOption(label=item,description='Select this'))
      view = DropdownView(options,category,"spawns","Select one",user)
      await ctx.response.send_message('Pick Your Pokemon/Area', view=view)
      return
  spawns = get_data(input, category)

  if spawns == None: await ctx.response.send_message('Pokémon/Map could not be found.')
  else:
    msg = ''
    for data in spawns:
      if len(msg) + len(data) >= 2000-6:
        msg = ''.join(['```', msg, '```'])
        await ctx.channel.send(msg)
        msg = '\n'
      msg += data + '\n'
    msg = ''.join(['```', msg, '```'])
    await ctx.response.send_message(msg)

@client.slash_command(
  description = "This command shows digspots",
  options = [
    Option("region", "Choose the region", required= True, choices=[
      OptionChoice("Kanto", "KANTO"),
      OptionChoice("Johto", "JOHTO"),
      OptionChoice("Sevii Islands", "SEVII ISLANDS"),
      OptionChoice("Sinnoh", "SINNOH")
      ]
    )
  ]
)
@commands.cooldown(1,5,commands.BucketType.user)
async def digspots(ctx, region):
  user = ctx.user.id
  loc = dig_func1(region)
  options = []
  for item in loc:
    options.append(SelectOption(label=item,description='Select this'))
  view = DropdownView(options, region, "digspots", "Select one", user)
  await ctx.response.send_message('Choose one', view=view)
  return

@client.slash_command(
  description = "This command shows information about moves, items and abilities",
  options = [
    Option("argument", "Move, Item, Ability", required = True)
  ]
)
@commands.cooldown(1,5,commands.BucketType.user)
async def info(ctx,argument):
  user = ctx.user.id
  msg = argument.replace("-","").lower()
  if msg in moves_keys:
    data = do_moves(msg)
  elif msg in ability_keys:
    data = do_ability(msg)
  elif msg in items_keys:
    data = do_item(msg)
  else:
    test_keys = []
    category = {}
    for key in moves_keys:
      if SequenceMatcher(a=msg,b=key).ratio() >= 0.8:
        test_keys.append(key)
        category.update({key:"move"})
    for key in ability_keys:
      if SequenceMatcher(a=msg,b=key).ratio() >= 0.8:
        test_keys.append(key)
        category.update({key:"ability"})
    for key in items_keys:
      if SequenceMatcher(a=msg,b=key).ratio() >= 0.8:
        test_keys.append(key)
        category.update({key:"item"})
    if len(test_keys) == 1:
      check = category[test_keys[0]]
      if check == "move":
        data = do_moves(test_keys[0])
      elif check == "ability":
        data = do_ability(test_keys[0])
      elif check == "item":
        data = do_item(test_keys[0])
    elif len(test_keys) > 1:
      options = []
      for item in test_keys:
        options.append(SelectOption(label=item,description='Select this'))
      view = DropdownView(options,category,"info","Select one",user)
      await ctx.response.send_message('Pick Your Move, Item or Ability', view=view)
      return
    else:
      await ctx.response.send_message("Move, Item or Ability does not exist")
      return
  await ctx.response.send_message(data)

@client.slash_command(
  description = "Gives information on excavation sites",
  options=[
    Option("site","Choose the excavation site",required=True,choices=[
      OptionChoice("Haunted Site", "Haunted Site"),
      OptionChoice("Mineral Site", "Mineral Site"),
      OptionChoice("Feral Site", "Feral Site"),
      OptionChoice("Glacial Site", "Glacial Site"),
      OptionChoice("Natural Site", "Natural Site"),
      OptionChoice("Historical Site", "Historical Site"),
      OptionChoice("Wondrous Site", "Wondrous Site"),
      OptionChoice("Briny Site", "Briny Site"),
      OptionChoice("Draconic Site", "Draconic Site")
      ]
    )
  ]
)
@commands.cooldown(1,5,commands.BucketType.user)
async def excavation(ctx,site):
  exca_data = exca(site)
  msg = '\n'
  for data in exca_data:
    if len(msg) + len(data) >= 2000-6:
      msg = ''.join(['```CSS', msg, '```'])
      await ctx.channel.send_message(msg)
      msg = '\n'
    msg += data + '\n'
  msg = ''.join(['```CSS', msg, '```'])
  await ctx.response.send_message(msg)

@client.slash_command(
  description="This command gives areas for ev training",
  options=[
    Option("region","Choose the region",choices=[
      OptionChoice("Kanto", "kanto"),
      OptionChoice("Johto", "johto"),
      OptionChoice("Hoenn", "hoenn"),
      OptionChoice("Sinnoh", "sinnoh")
    ]
    ),
    Option("evstat","Choose the ev stat",choices=[
      OptionChoice("Attack", "ATK"),
      OptionChoice("Defence", "DEF"),
      OptionChoice("Speed", "SPD"),
      OptionChoice("Special attack", "SPATK"),
      OptionChoice("Special defence", "SPDEF"),
      OptionChoice("Hp", "HP")
    ]
    )
  ]
)
@commands.cooldown(1,5,commands.BucketType.user)
async def evspots(ctx,region=None,evstat=None):
  if region is None and evstat is None:
    await ctx.response.send_message('Please provide a Region/Stat')
    return
  elif region is None and evstat is not None:
    input = evstat
    category = 'Stat'
  elif region is not None and evstat is None:
    input = region
    category = 'Region'
  else:
    await ctx.response.send_message('Please select only one option')
    return

  spawns = get_ev_data(input, category)

  msg = ''
  for data in spawns:
    if len(msg) + len(data) >= 2000-6:
      msg = ''.join(['```', msg, '```'])
      await ctx.channel.send_message(msg)
      msg = '\n'
    msg += data + '\n'
  msg = ''.join(['```', msg, '```'])
  await ctx.response.send_message(msg)
    





@client.slash_command(
  description="This command gives mostused pokemon data for different months",
  options=[
    Option("month","Choose the month",required=True,choices=[
      OptionChoice("January", "January"),
      OptionChoice("February", "February"),
      OptionChoice("March", "March"),
      OptionChoice("April", "April"),
      OptionChoice("May", "May"),
      OptionChoice("June", "June"),
      OptionChoice("July", "July"),
      OptionChoice("August", "August"),
      OptionChoice("September", "September"),
      OptionChoice("October", "October"),
      OptionChoice("November", "Novemeber"),
      OptionChoice("December", "December")
    ]
    ),
    Option("year","Choose the year",required=True,choices=[
      OptionChoice("2021", "2021"),
      OptionChoice("2022", "2022")
    ]
    ),
    Option("server","Choose the server",required=True,choices=[
      OptionChoice("Silver", "Silver"),
      OptionChoice("Gold", "Gold")
    ]
    )
  ]
)
@commands.cooldown(1,5,commands.BucketType.user)
async def mostused(ctx,month,year,server):
  most_data = mostused_func(month,year,server)
  if most_data == False:
    await ctx.response.send_message("Data for this month doesnt exist")
    return

  msg = '\n'
  for data in most_data:
    if len(msg) + len(data) >= 2000-6:
      msg = ''.join(['```CSS', msg, '```'])
      await ctx.channel.send(msg)
      msg = '\n'
    msg += data + '\n'
  msg = ''.join(['```CSS', msg, '```'])
  await ctx.response.send_message(msg)


@client.slash_command(
  description = "This command shows headbutt spawns",
  options = [
    Option("argument","Pokemon/Area",required=True)
  ]
)
@commands.cooldown(1,5,commands.BucketType.user)
async def headbutt(ctx, argument):
  input = argument.lower()
  user = ctx.user.id
  test_keys = []
  if input not in headbutt_keys:
    for key in headbutt_keys:
      if SequenceMatcher(a=input,b=key).ratio() >= 0.8:
        test_keys.append(key)
    if len(test_keys) == 1:
      input = test_keys[0]
    elif len(test_keys) > 1:
      options = []
      for item in test_keys:
        options.append(SelectOption(label=item,description='Select this'))
      view = DropdownView(options,"None","headbutt","Select one",user)
      await ctx.response.send_message('Pick Your Pokemon/Area', view=view)
      return
    else:
      await ctx.response.send_message("Please add a valid Pokemon/Area")
      return
  head = headbutt_check_func(input)
  msg = '\n'
  for data in head:
    if len(msg) + len(data) >= 2000-6:
      msg = ''.join(['```', msg, '```'])
      await ctx.channel.send_message(msg)
      msg = '\n'
    msg += data + '\n'
  msg = ''.join(['```', msg, '```'])
  await ctx.response.send_message(msg)

@client.slash_command(
  description = "This command shows repel tricks of pokemons",
  options = [
    Option("argument","Pokemon/Area",required=True)
  ]
)
@commands.cooldown(1,5,commands.BucketType.user)
async def repel(ctx,argument):
  user = ctx.user.id
  input = argument.lower().replace(" ","")
  if input in repel_pkn_keys.keys():
    input = repel_pkn_keys[input]
    category = "pkn"
  elif input in repel_loc_keys.keys():
    input = repel_loc_keys[input]
    category = "loc"
  else:
    pkn_input = []
    for item in repel_pkn_keys.keys():
      if SequenceMatcher(a=input,b=item).ratio() >= 0.7:
        pkn_input.append(repel_pkn_keys[item])
    if len(pkn_input) == 1:
      input = pkn_input[0]
      category = "pkn"
    elif len(pkn_input) > 1:
      category = "pkn"
      options = []
      for pkn in pkn_input:
        options.append(SelectOption(label=pkn,description='Select this'))
      view = DropdownView(options,category,"repel","Select one",user)
      await ctx.response.send_message('Pick your Pokemon/Area:', view=view)
      return
    else:
      loc_input = []
      for item in repel_loc_keys.keys():
        if SequenceMatcher(a=input,b=item).ratio() >= 0.7:
          loc_input.append(repel_loc_keys[item])
      if len(loc_input) == 1:
        input = loc_input[0]
        category = "loc"
      elif len(loc_input) > 1:
        category = "loc"
        options = []
        for loc in loc_input:
          options.append(SelectOption(label=loc,description='Select this'))
        view = DropdownView(options, category, "repel", "Select one", user)
        await ctx.response.send_message('Pick Your Pokemon/Area', view=view)
        return
      else:
        await ctx.response.send_message("Please add a valid Pokemon/Area")
        return
  pro = pro_repel(input,category)
  msg = '\n'
  for data in pro:
    if len(msg) + len(data) >= 2000-6:
      msg = ''.join(['```', msg, '```'])
      await ctx.channel.send_message(msg)
      msg = '\n'
    msg += data + '\n'
  msg = ''.join(['```', msg, '```'])
  await ctx.response.send_message(msg)

@client.slash_command(
  description = "Shows the type chart for one or two types",
  options=[
    Option("type1","Choose the type",required=True,choices=[
      OptionChoice("Fire", "Fire"),
      OptionChoice("Water", "Water"),
      OptionChoice("Grass", "Grass"),
      OptionChoice("Normal", "Normal"),
      OptionChoice("Electric", "Electric"),
      OptionChoice("Ice", "Ice"),
      OptionChoice("Fighting", "Fighting"),
      OptionChoice("Poison", "Poison"),
      OptionChoice("Ground", "Ground"),
      OptionChoice("Flying", "Flying"),
      OptionChoice("Psychic", "Psychic"),
      OptionChoice("Bug", "Bug"),
      OptionChoice("Rock", "Rock"),
      OptionChoice("Ghost", "Ghost"),
      OptionChoice("Dark", "Dark"),
      OptionChoice("Dragon", "Dragon"),
      OptionChoice("Steel", "Steel"),
      OptionChoice("Fairy", "Fairy")
    ]
    ),
    Option("type2","Choose 2nd type",choices=[
      OptionChoice("Fire", "Fire"),
      OptionChoice("Water", "Water"),
      OptionChoice("Grass", "Grass"),
      OptionChoice("Normal", "Normal"),
      OptionChoice("Electric", "Electric"),
      OptionChoice("Ice", "Ice"),
      OptionChoice("Fighting", "Fighting"),
      OptionChoice("Poison", "Poison"),
      OptionChoice("Ground", "Ground"),
      OptionChoice("Flying", "Flying"),
      OptionChoice("Psychic", "Psychic"),
      OptionChoice("Bug", "Bug"),
      OptionChoice("Rock", "Rock"),
      OptionChoice("Ghost", "Ghost"),
      OptionChoice("Dark", "Dark"),
      OptionChoice("Dragon", "Dragon"),
      OptionChoice("Steel", "Steel"),
      OptionChoice("Fairy", "Fairy")
    ]
    )
  ]
)
@commands.cooldown(1,5,commands.BucketType.user)
async def poketypes(ctx,type1,type2=None):
	if type2 != None:
		types = [type1,type2]
	else:
		types = [type1]

	data = type_check(types)

	msg = ''
	if len(data[3]) != 0:
		msg += '**4x Effective**\n%s\n'%data[3]
	if len(data[2]) != 0:
		msg += '**2x Effective**\n%s\n'%data[2]
	if len(data[4]) != 0:
		msg += '**Immunity**\n%s\n'%data[4]
	if len(data[0]) != 0:
		msg += '**½x Resistance**\n%s\n'%data[0]
	if len(data[1]) != 0:
		msg += '**¼x Resistance**\n%s'%data[1]
	await ctx.response.send_message(msg)

@client.slash_command(
  description = "Gives the current time of PRO"
)
@commands.cooldown(1,5,commands.BucketType.user)
async def poketime(ctx):
  offset = 172909
  now = datetime.now(timezone.utc)
  hh = now.hour * 3600
  mm = now.minute * 60
  ss = now.second
  total_seconds = hh + mm + ss
  poke_seconds = total_seconds * 4

  total_game_seconds = offset+poke_seconds
  game_time = now + timedelta(seconds=total_game_seconds)

  game_hour = game_time.hour
  game_min = game_time.minute
  timer = pad_with_zeros(game_hour) + ":" + pad_with_zeros(game_min)
  if 4 <= game_hour < 10 :
    timer = ":sunrise: Morning - " + timer
  elif 10 <= game_hour < 20 :
    timer = ":sunny: Day - " + timer
  else:
    timer = ":crescent_moon: Night - " + timer
  await ctx.response.send_message(timer)


@client.slash_command(
  description = 'owner only command'
)
async def update_spawns_data(ctx):
  if ctx.author.id != 308993841124474891:
    return
  global Spawns, locations, Items, combined
  final_data = {}
  spawner = await spawn_func()
  a = open("spawns.py","w")
  a.write("Spawns = " + str(spawner))
  a.close()
  from spawns import Spawns
  final_data.update(spawner)
  locationer = await location_func()
  b = open("locations.py","w")
  b.write("locations = " + str(locationer))
  b.close()
  from locations import locations
  final_data.update(locationer)
  itemer = await item_func()
  c = open("items.py","w")
  c.write("Items = " + str(itemer))
  c.close()
  from items import Items
  final_data.update(itemer)
  d = open("Combined.py","w")
  d.write("combined = " + str(final_data))
  d.close()
  from Combined import combined
  global location_list, spawn_list, total_list, item_list
  location_list = list(locations.keys())
  spawn_list = list(Spawns.keys())
  total_list = []
  total_list.extend(location_list)
  total_list.extend(spawn_list)
  item_list = list(Items.keys())
  await ctx.response.send_message("Data has been updated")

@client.slash_command(description="Shows invite links of NQR, PRO discord and my silver server's guild")
async def invite(ctx):
  msg = "Invite link of NQR\nhttps://discord.com/api/oauth2/authorize?client_id=810237383832240162&permissions=139855264832&scope=bot applications.commands\n"
  msg += "Invite link to PRO discord.\nhttps://discord.gg/98pMNxq\n"
  msg += "Looking for a guild in Silver Server? Checkout SilverNabs\nhttps://pokemonrevolution.net/forum/topic/123966-silvernabs/"
  await ctx.response.send_message(msg)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_slash_command_error(ctx, error):
  if isinstance(error, CommandOnCooldown):
    msg = "**still on cooldown**, try again after {:.2f}s".format(error.retry_after)
    await ctx.response.send_message(msg)
  else:
    raise error

@client.event
async def on_command_error(ctx,error):
  if isinstance(error, CommandNotFound):
    pass
  else:
    raise error

# @client.event
# async def on_guild_join(guild):
#   prefix1[str(guild.id)] = '^'
#   sachin = prefix1
#   with open("prefixes.py","w") as f:
#     f.write("prefix1 = "+ str(sachin))
#     f.close()

# @client.event
# async def on_guild_remove(guild):
#   if guild.id in prefix1:
#     prefix1.pop(str(guild.id))
#     sachin = prefix1
#     with open("prefixes.py", "w") as f :
#       f.write("prefix1 = "+ str(sachin))
#       f.close()

keep_alive()
client.loop.create_task(background_task())

client.run("Token goes here")