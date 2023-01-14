import disnake

import re
import pandas as pd
import json

from evspots import ev
from mostused import mostused_data
from repel_data import repelloc, repelpkn
from effectiveness_data import effectivenessData
from excavations import excavation_data
from headbutt import headbutt_data
from moves import movesabc,moves_coding_data
from machine import machines
from move_tutor import move_tutors
from tm_tutor import tm_tutors
from items_data import item_data
from abilities import ability_data
from digspots import digarea
from Combined import combined
from dex_data import dex_Data
from mod_data import emote_id
from smogon import smogon_sets
from learnset import learner


def movesLearn(pokemon,move):
  learn_data = {'E':'Eggmove Tutor','T':'Move Tutor','M':'HM/TM','S':'Event Move Tutor'}
  answer = []
  lower_name = pokemon.lower().replace(" ","").replace("-","")
  if move in learner[lower_name]:
    gens1 = learner[lower_name][move][0]
    abc = gens1[0]
    abcd = gens1[1:]
    leveler1 = gens1[2:]
    try:
      gens2 = learner[lower_name][move][1]
      efg = gens2[0]
      efgh = gens2[1:]
      leveler2 = gens2[2:]
    except:
      efg = ''
    if abc == efg:
      if any(test in abcd for test in['T', 'M','S','E']) and 'L' in efgh:
        answer.append('Pokemon : %s'%(pokemon))
        answer.append('DexID : %d'%(int(dex_Data[pokemon]['Id'])))
        answer.append('Learns the move by %s and by Levelup at level %s'%(abcd[0],leveler2))
        return answer
      elif 'L' in abcd and any(test in efgh for test in['T', 'M','S','E']):
        answer.append('Pokemon : %s\n'%(pokemon))
        answer.append('DexID : %d\n'%(int(dex_Data[pokemon]['Id'])))
        answer.append('Learns the move  Levelup at level %s and by %s'%(leveler1,learn_data[abcd[0]]))
        return answer
      elif ('E' in abcd and any(test in efgh for test in['T', 'M','S'])) or ('T' in abcd and any(test in efgh for test in['E', 'M','S'])) or ('M' in abcd and any(test in efgh for test in['T', 'E','S'])) or ('S' in abcd and any(test in efgh for test in['T', 'M','E'])) :
        answer.append('Pokemon : %s'%(pokemon))
        answer.append('DexID : %d'%(int(dex_Data[pokemon]['Id'])))
        answer.append('Learns the move by %s and by %s'%(learn_data[abcd[0]],learn_data[efgh[0]]))
        return answer
      else:
        answer.append('Pokemon : %s'%(pokemon))
        answer.append('DexID : %d'%(int(dex_Data[pokemon]['Id'])))
        answer.append('Does not learn the move')
        return answer
    else:
      if 'E' in abcd or 'T' in abcd or 'M' in abcd or 'S' in abcd:
        answer.append('Pokemon : %s'%(pokemon))
        answer.append('DexID : %d'%(int(dex_Data[pokemon]['Id'])))
        answer.append('Learns the move by %s'%(learn_data[abcd[0]]))
        return answer
      elif 'L' in abcd:
        answer.append('Pokemon : %s'%(pokemon))
        answer.append('DexID : %d'%(int(dex_Data[pokemon]['Id'])))
        answer.append('Learns the move by Levelup at lvl %s'%(leveler1))
        return answer
      else:
        answer.append('Pokemon : %s'%(pokemon))
        answer.append('DexID : %d'%(int(dex_Data[pokemon]['Id'])))
        answer.append('Does not learn the move')
        return answer
  elif len(dex_Data[pokemon]['prev']) != 0 :
    for item in dex_Data[pokemon]['prev']:
      sachin1 = item[0].replace(" ","").lower()
      sachin1 = item[0].replace("-","").lower()
      try:
        gens1 = learner[sachin1][move][0]
        abcd = gens1[1:]
      except:
        abcd = ''
      if move in learner[sachin1] and 'S' not in abcd and 'E' not in abcd:
        answer.append('Pokemon : %s'%(pokemon))
        answer.append('DexID : %d'%(int(dex_Data[pokemon]['Id'])))
        answer.append('Learns the move by Pre-Evolution Tutor')
        return answer
      elif 'E' in abcd or 'S' in abcd:
        answer.append('Pokemon : %s'%(pokemon))
        answer.append('DexID : %d'%(int(dex_Data[pokemon]['Id'])))
        answer.append('Learns the move by %s'%(learn_data[abcd[0]]))
        return answer
    answer.append('Pokemon : %s'%(pokemon))
    answer.append('DexID : %d'%(int(dex_Data[pokemon]['Id'])))
    answer.append('Does not learn the move')
    return answer    
  else:
    answer.append('Pokemon : %s'%(pokemon))
    answer.append('DexID : %d'%(int(dex_Data[pokemon]['Id'])))
    answer.append('Does not learn the move')
    return answer

def Poke_learnset(pokemon):
  learn_data = {'E':'Eggmove Tutor','T':'Move Tutor','M':'HM/TM','S':'Event Move Tutor'}
  pokemon_learnset = learner[pokemon.lower().replace(" ","").replace("-","")]
  learn_list = []
  learn_list.append('Pokemon : %s'%(pokemon))
  learn_list.append('DexID : %d'%(int(dex_Data[pokemon]['Id'])))
  for key,value in pokemon_learnset.items():
    move1 = value[0]
    check_gen1 = move1[0]
    check_learn1 = move1[1]
    check_level1 = move1[2:]
    try:
      move2 = value[1]
      check_gen2 = move2[0]
      check_learn2 = move2[1]
      check_level2 = move2[2:]
    except:
      check_gen2 = ''

    if check_gen1 == check_gen2:
      if any(test in check_learn1 for test in['T', 'M','S','E']) and 'L' in check_learn2:
        learn_list.append('%s Learns by %s and Level-up at lvl %s'%(key,learn_data[check_learn1],check_level2))
      elif 'L' in check_learn1 and any(test in check_learn2 for test in['T', 'M','S','E']):
        learn_list.append('%s Learns by Level-up at lvl %s and %s'%(key,check_level1,learn_data[check_learn2]))
      elif ('E' in check_learn1 and any(test in check_learn2 for test in ['T', 'M','S'])) or ('T' in check_learn1  and any(test in check_learn2 for test in['E', 'M','S'])) or ('M' in check_learn1  and any(test in check_learn2 for test in['T', 'E','S'])) or ('S' in check_learn1  and any(test in check_learn2 for test in['T', 'M','E'])) :
        learn_list.append('%s Learns by %s and %s'%(key,learn_data[check_learn1],learn_data[check_learn2]))
    else:
      if any(test in check_learn1 for test in['T', 'M','S','E']):
        learn_list.append('%s Learns by %s'%(key,learn_data[check_learn1]))
      elif 'L' in check_learn1:
        learn_list.append('%s Learns by Levelup at lvl %s'%(key,check_level1))
  try:
    if len(dex_Data[pokemon]['prev']) != 0:
      for poke in dex_Data[pokemon]['prev']:
        pre_evo = poke[0].lower()
        for key,value in learner[pre_evo].items():
          move = value[0]
          check_gen = move[0]
          check_learn = move[1]
          if 'E' in check_learn or 'S' in check_learn:
            if any(key in s for s in learn_list):
              continue
            learn_list.append('%s Learns by %s'%(key,learn_data[check_learn]))
          elif 'L' in check_learn :
            if any(key in s for s in learn_list):
              continue
            learn_list.append('%s Learns by pre evo tutor'%(key))
  except: pass
  return learn_list

def get_data(input, category):
  check = 'Area'
  if category == None: return None
  spawns, area_list, map_list, rarity_list = [], [], [], []
  try:
    for key in combined[input]:
      if combined[input][key]['Tier'][0] not in rarity_list:
         rarity_list.append(combined[input][key]['Tier'][0])
      for i in range(len(combined[input][key]['Area'])):
        if combined[input][key]['Area'][i] not in area_list: area_list.append(combined[input][key]['Area'][i])
  except KeyError: return None
  if category == 'Item':
    check = 'Map'
    for key in combined[input]:
      for i in range(len(combined[input][key]['Map'])):
        if combined[input][key]['Map'][i] not in map_list: map_list.append(combined[input][key]['Map'][i])

  for key in combined[input]:
    d = combined[input][key]
    for i in range(len(d[check])):
      item, MS = '-', 'No'

      if category != 'Item':
        if d['Item'][i] != None: item = d['Item'][i]
      if d['MemberOnly'][i]: MS = 'Yes'

      key_ = ' '*(2+len(max(list(combined[input].keys()), key=len))-len(key))
      lvl_ = ' '*(6-(len(str(d['MinLVL'][i]))+len(str(d['MaxLVL'][i]))))
      ms_ = ' '*(5-len(MS))
      area_ = ' '*(2+len(max(area_list, key=len))-len(d['Area'][i]))
      time_ = ' '*(10-len(d['Daytime'][i]))
      rarity_ = ' '*(2+len(max(rarity_list, key=len))-len(d['Tier'][i]))
      header_ = ' '*(2+len(max(list(combined[input].keys()), key=len))-len('#Map'))
      print(rarity_)

      if category in ['#Pokémon', 'Item']:
        header_ = ' '*(2+len(max(list(combined[input].keys()), key=len))-len('#Pokémon'))
        if len(max(list(combined[input].keys()), key=len)) < len('#Pokémon'): 
          key_ = ' '*(2+len('#Pokémon')-len(key))
          header_ = ' '*2

      if category == 'Item':
        map_ = ' '*(2+len(max(map_list, key=len))-len(d['Map'][i]))
        if spawns == []: spawns.append('md\n%s%sMap%sArea%sLevel%sMS%sDaytime%sRarity' % ('#Pokémon', header_, ' '*(2+len(max(map_list, key=len))-len('Map')), ' '*(2+len(max(area_list, key=len))-len('Area')), '  ', '   ', '   '))
        spawns.append('%s%s%s%s%s%s%d-%d%s%s%s%s%s%s' % (key, key_, d['Map'][i], map_, d['Area'][i], area_, d['MinLVL'][i], d['MaxLVL'][i], lvl_, MS, ms_, d['Daytime'][i], time_, d['Tier'][i]))
      else:  
        if spawns == []: spawns.append('md\n%s%sArea%sLevel%sMS%sDaytime%sRarity%sItem' % (category, header_, ' '*(2+len(max(area_list, key=len))-len('Area')), '  ', '   ', '   ', '   '))
        spawns.append('%s%s%s%s%d-%d%s%s%s%s%s%s%s%s' % (key, key_, d['Area'][i], area_, d['MinLVL'][i], d['MaxLVL'][i], lvl_, MS, ms_, d['Daytime'][i], time_, d['Tier'][i], rarity_, item))

  return spawns


def dig_func1(region):
  loc = ['All Locations only']
  for item in digarea[region].keys():
    loc.append(item)
  return loc

def dig_func2(region):
  test_list = []
  for r in digarea[region].keys():
    test_list.append(r)
  embedVar = disnake.Embed(title = region,description="",color=0xe0b8ea)
  n = 0
  for r in digarea[region].keys():
    embedVar.add_field(name=test_list[n],value=digarea[region][r]['Location'],inline=False)
    n += 1
  embedVar.add_field(name='\u200b', value='<:Angreifer:846099096149164032>Angreifer#7055 <:Sachin:846101219415818240>Sachin#4994', inline=False)
  return embedVar

def dig_func3(region,area):
  embedVar = disnake.Embed(title = region,description="",color=0xe0b8ea)
  embedVar.add_field(name="Name",value=area,inline=False)
  embedVar.add_field(name="Location",value=digarea[region][area]['Location'],inline=False)
  embedVar.add_field(name="Pokemon Levels",value=digarea[region][area]['Pokemon Levels'],inline=True)
  embedVar.add_field(name="Patches",value=digarea[region][area]['Patches'],inline=True)
  embedVar.add_field(name="Items",value=", ".join(str(x) for x in digarea[region][area]['Items']),inline=False)
  embedVar.add_field(name="Pokemons",value=", ".join(str(x) for x in digarea[region][area]['Pokemons']),inline=False)
  embedVar.add_field(name='\u200b', value='<:Angreifer:846099096149164032>Angreifer#7055 <:Sachin:846101219415818240>Sachin#4994', inline=False)
  return embedVar

def do_moves(msg):
  answer = "**%s**\n"%(movesabc[msg]['name'])
  if msg in machines.keys():
    answer += "**HM/TM**\n"
    test = machines[msg].split("/")
    for a in test:
      answer += "• %s\n"%(a)
  if msg in move_tutors.keys():
    answer += "**Move Tutor**\n"
    test = move_tutors[msg].split("/")
    for a in test:
      answer += "• %s\n"%(a)
  if msg in tm_tutors.keys():
    answer += "**TM Tutor**\n"
    test = tm_tutors[msg].split("/")
    for a in test:
      answer += "• %s\n"%(a)
  answer += "**Description**\n"
  answer += "• %s\n"%(movesabc[msg]['description'])
  answer += "• {} - {} - {} BP - {}% - {} PP\n".format(movesabc[msg]['type'].capitalize(),movesabc[msg]['category'].capitalize(),movesabc[msg]['power'],movesabc[msg]['accuracy'],movesabc[msg]['pp'])
  if movesabc[msg]['priority'] != 0:
    answer += "•__Priority__ - {}\n".format(movesabc[msg]['priority'])
  if movesabc[msg]['secondary'] != None:
    answer += "__Secondary Effects__\n"
    for key,value in movesabc[msg]['secondary'].items():
      answer += "• {} : {}\n".format(key.capitalize(),value)
  if msg in moves_coding_data['Move']['Incorrectly'].keys():
    answer += "**PRO NOTE**\n•{}".format(moves_coding_data['Move']['Incorrectly'][msg].capitalize())
  elif msg in moves_coding_data['Move']['Notcoded']:
    answer += "**PRO NOTE**\n•This move is not coded"
  return answer

def do_ability(msg):
  answer = "**%s**\n"%(ability_data[msg]['name'])
  answer += "**Description**\n"
  answer += "%s"%(ability_data[msg]['description'])
  if msg in moves_coding_data['Ability']['Incorrectly'].keys():
    answer += "**PRO NOTE**\n•{}".format(moves_coding_data['Ability']['Incorrectly'][msg].capitalize())
  elif msg in moves_coding_data['Ability']['Notcoded']:
    answer += "**PRO NOTE**•This Ability is not coded"
  return answer

def do_item(msg):
  answer = "**%s**\n"%(item_data[msg]['name']) 
  answer += "**Description**\n"
  answer += "Type : %s\n"%(item_data[msg]['type'].capitalize())
  answer += "%s"%(item_data[msg]['description'])
  return answer

def headbutt_check_func(input_data):
  df = pd.DataFrame.from_dict(headbutt_data[input_data], orient='columns')
  try:
    headbutt_data[input_data][0]['Pokemon']
    df.set_index('Pokemon', inplace=True)
  except:
    df.set_index('Area', inplace=True)
  final_data = df.to_string()
  reader = [input_data]
  for line in re.split('\n', final_data):
    reader.append(line)
  return reader

def exca(site_name):
  data = []
  data.append("#Spawns")
  df = pd.DataFrame.from_dict(excavation_data[site_name]['Pokemon'],orient='columns')
  df.set_index('Requirements', inplace=True)
  final_data = df.to_string()
  for line in re.split('\n', final_data):
    data.append(line)
  data.append("\n")
  data.append("#Items")
  data.append("Requirements : %s"%excavation_data[site_name]['Items'][0]['Requirements'])
  data.append("Item : %s"%excavation_data[site_name]['Items'][0]['Items'])
  if len(excavation_data[site_name].keys()) == 3:
    data.append("\n")
    exca_site_info = excavation_data[site_name]
    greg_keys = list(exca_site_info.keys())
    data.append("#%s"%greg_keys[2])
    data.append("Requirements : %s"%exca_site_info[greg_keys[2]][0]['Requirements'])
    data.append("Reward : %s"%exca_site_info[greg_keys[2]][0]['Reward'])
  return data

def get_ev_data(input, category):
  if category == None: return None
  spawns = []

  if category == 'Stat':
    if spawns == []: spawns.append('md\n#Map       Area  Daytime  Pokémon')
    for region in ev:
      d = ev[region][input]
      spawns.append('%s%s%s%s%s%s%s' % (d['Map'], ' '*(11-len(d['Map'])), d['Area'], ' '*2, d['Daytime'], ' '*8, d['Pokemon']))
  
  if category == 'Region':
    if input in ['kanto', 'johto']: map_ = ' '*7
    else: map_ = ' '*8
    if spawns == []: spawns.append('md\n#EV    Map%sArea  Daytime  Pokémon' % map_) 
    for EV in ev[input]:
      stat = ev[input][EV]
      EV_ = ' '*(2+len(max(list(ev[input].keys()), key=len))-len(EV))
      spawns.append('%s%s%s%s%s%s%s%s%s' % (EV, EV_, stat['Map'], ' '*2, stat['Area'], ' '*2, stat['Daytime'], ' '*8, stat['Pokemon']))
  return spawns

def mostused_func(month,year,server):
  if month not in mostused_data[year].keys():
    return False
  my_data = mostused_data[year][month][server]
  reader = ["%s %s %s"%(server,month,year)]
  for line in re.split('&', my_data):
    reader.append(line)

  return reader

def pro_repel(msg,category):
  if category == "pkn":
    df = pd.DataFrame.from_dict(repelpkn[msg], orient='columns')
    df.set_index('Map', inplace=True)
    final_data = df.to_string()
    reader = [msg]
    for line in re.split('\n', final_data):
      reader.append(line)
    #reader.pop(2)
    return reader
  else:
    df = pd.DataFrame.from_dict(repelloc[msg], orient='columns')
    df.set_index('Pokemon', inplace=True)
    final_data = df.to_string()
    reader = [msg]
    for line in re.split('\n', final_data):
      reader.append(line)
    #reader.pop(2)
    return reader

def pad_with_zeros(num):
  if num < 10:
    return "0"+str(num)
  else:
    return str(num)

def get_effectiveness(pokeType):
  effDict = {'Normal':1, 'Fire':1, 'Fighting':1,  'Water':1,  'Flying':1,  'Grass':1,  'Poison':1,  'Electric':1,  'Ground':1,  'Psychic':1,  'Rock':1,  'Ice':1,  'Bug':1,  'Dragon':1,  'Ghost':1,  'Dark':1,  'Steel':1,  'Fairy':1}
  for pType in pokeType:
    for Eff in effectivenessData[pType]:
      for Type in effectivenessData[pType][Eff]:
        effDict[Type] *= Eff
  effChart = {}
  for Type in effDict.keys():
    try:
      if effDict[Type] == 4: effChart['4'].append(Type)
      if effDict[Type] == 2: effChart['2'].append(Type)
      if effDict[Type] == 0.5: effChart['½'].append(Type)
      if effDict[Type] == 0.25: effChart['¼'].append(Type)
      if effDict[Type] == 0: effChart['0'].append(Type)
    except KeyError:
      if effDict[Type] == 4: effChart['4'] = [Type]
      if effDict[Type] == 2: effChart['2'] = [Type]
      if effDict[Type] == 0.5: effChart['½'] = [Type]
      if effDict[Type] == 0.25: effChart['¼'] = [Type]
      if effDict[Type] == 0: effChart['0'] = [Type]
  return effChart

def type_check(types):
	effChart = get_effectiveness(types)
	pokeResists2, pokeResists4, pokeWkns2, pokeWkns4, pokeImmunity = '', '', '', '', ''
	for X in effChart:
		for pType in effChart[X]:
			typeEffectiveness = '%s, '%pType
			if X == '2': pokeWkns2 += typeEffectiveness
			if X == '4': pokeWkns4 += typeEffectiveness
			if X == '½': pokeResists2 += typeEffectiveness
			if X == '¼': pokeResists4 += typeEffectiveness
			if X == '0': pokeImmunity += typeEffectiveness
	pokeWkns2 = pokeWkns2[:-2]
	pokeWkns4 = pokeWkns4[:-2]
	pokeResists2 = pokeResists2[:-2]
	pokeResists4 = pokeResists4[:-2]
	pokeImmunity = pokeImmunity[:-2]
	return [pokeResists2, pokeResists4, pokeWkns2, pokeWkns4, pokeImmunity]

def get_form(pokeName):
  if pokeName == 'Rotom Wash': return '-w'
  if pokeName == 'Rotom Heat': return '-h'
  if pokeName == 'Rotom Frost': return '-f'
  if pokeName == 'Rotom Fan': return '-s'
  if pokeName == 'Rotom Mow': return '-c'
  if pokeName == 'Rotom': return ''
  if pokeName == 'Lycanroc Dusk': return '-d'
  if pokeName == 'Lycanroc Midnight': return '-m'
  if pokeName == 'Lycanroc': return ''
  if 'Alola' in pokeName: return '-a'
  if 'Therian' in pokeName: return '-s'
  return ''

def dex_embed(pokeName):
  if pokeName in ['Kommo-O', 'Jangmo-O', 'Hakamo-O']: pokeName = pokeName.capitalize()
  if pokeName not in dex_Data.keys(): return None
  pokeData = dex_Data[pokeName]
  #Effectiveness
  pokeType = pokeData['Type']
  effChart = get_effectiveness(pokeType)
  pokeResists, pokeWkns = '', ''
  for X in effChart:
    typeEffectiveness = '\n'.join(['**'+X+'x** '+emote_id[pType] for pType in effChart[X]]) + '\n'
    if X in ['2', '4']: pokeWkns += typeEffectiveness
    if X in ['½', '¼', '0']: pokeResists += typeEffectiveness
  #--------------------------------------
  #Evolution
  pokeEvolution, prevEvo = "", ""
  if len(pokeData['prev']) == 1:  prevEvo = pokeData['prev'][0][0]+'('+pokeData['prev'][0][1]+')'+' → '
  if len(pokeData['prev']) == 2:  pokeEvolution += pokeData['prev'][1][0]+'('+pokeData['prev'][1][1]+')'+' → '+pokeData['prev'][0][0]+'('+pokeData['prev'][0][1]+')'+' → '+'***'+pokeName+'***'
  if len(pokeData['next']) == 0 and len(pokeData['prev']) == 1: pokeEvolution += prevEvo+'***'+pokeName+'***\n'
  if len(pokeData['next']) == 1: pokeEvolution += '\n'.join([prevEvo+'***'+pokeName+'***('+nextEvo[1]+')'+' → '+nextEvo[0] for nextEvo in pokeData['next'][0]]) + '\n'
  if len(pokeData['next']) == 2:
    try: pokeEvolution += '\n'.join(['***'+pokeName+'***'+'('+pokeData['next'][0][i][1]+')'+' → '+pokeData['next'][0][i][0]+'('+nextEvo[1]+')'+' → '+nextEvo[0] for i, nextEvo in enumerate(pokeData['next'][1])])
    except IndexError: pokeEvolution += '\n'.join(['***'+pokeName+'***'+'('+pokeData['next'][0][0][1]+')'+' → '+pokeData['next'][0][0][0]+'('+nextEvo[1]+')'+' → '+nextEvo[0] for nextEvo in pokeData['next'][1]])
  if pokeEvolution == "": pokeEvolution = '-'
  #--------------------------------------
  #Rest of data
  pokeID, pokeTitleID = str(pokeData['Id']), str(pokeData['Id'])
  if len(pokeID) == 1: pokeTitleID = "00" + pokeID
  if len(pokeID) == 2: pokeTitleID = "0" + pokeID
  pokeType = '\n'.join([emote_id[Type]+' '+Type for Type in pokeData['Type']])
  pokeAbility = '\n'.join([Ability[0] if Ability[1] == 'false' else '***'+Ability[0]+'***' for Ability in pokeData['Ability']])
  pokeStats = '\n'.join(['**'+Stat+':** '+str(pokeData['Base'][Stat]) for Stat in pokeData['Base']])
  embedThumbnail = "https://www.serebii.net/art/th/%s.png" % (pokeID + get_form(pokeName))
  embedTitleUrl = "https://www.smogon.com/dex/sm/pokemon/%s/" % (pokeName.replace(' ', '-') if ' ' in pokeName else pokeName)
  #---------------------------------------
  #Constructing Embed
  embedVar = disnake.Embed(title="%s #%s" % (pokeName, pokeTitleID), url=embedTitleUrl, description=pokeData['Description'], color=0xe0b8ea)
  embedVar.add_field(name='Type', value=pokeType, inline=True)
  embedVar.add_field(name='Abilities', value=pokeAbility, inline=True)
  embedVar.add_field(name='Evolution Line', value=pokeEvolution+'\n\u200b', inline=False)
  embedVar.add_field(name='Base Stats', value=pokeStats, inline=True)
  embedVar.add_field(name='Weak to', value=pokeWkns, inline=True)
  embedVar.add_field(name='Resists', value=pokeResists, inline=True)
  embedVar.add_field(name='\u200b', value='<:Angreifer:846099096149164032>Angreifer#7055 <:Sachin:846101219415818240>Sachin#4994', inline=False)
  embedVar.set_thumbnail(url=embedThumbnail)
  return embedVar

def smogon_embed(pokeName):
  if pokeName in ['Kommo-O', 'Jangmo-O', 'Hakamo-O']: pokeName = pokeName.capitalize()
  if pokeName not in smogon_sets.keys(): return None
  pokeData = smogon_sets[pokeName]
  try:  pokeID = str(dex_Data[pokeName]['Id'])
  except KeyError:  
    try: pokeID = str(dex_Data[pokeName.split('-')[0]]['Id'])
    except KeyError: pokeID = str(dex_Data[pokeName.split()[0]]['Id'])
  try:
    embedThumbnail = "https://www.serebii.net/art/th/%s.png" % (pokeID + get_form(pokeName))
    embedTitleUrl = "https://www.smogon.com/dex/sm/pokemon/%s/" % (pokeName.replace(' ', '-') if ' ' in pokeName else pokeName)
  except KeyError: return None
  embedVar = disnake.Embed(title=pokeName, url=embedTitleUrl, description='***X/Y***\n\u200b', color=0xe0b8ea)
  for set in list(pokeData.keys()):
    #if 'Monotype' in set: pokeData.pop(set)
    if 'BH' in set: pokeData.pop(set)
  for index, set in enumerate(pokeData, start=1):
    pokeSet = pokeData[set]
    fieldValue = '\n'.join(['**%s:** %s' % (data.capitalize(), pokeSet[data]) for data in pokeSet if data not in ['level', 'evs', 'moves', 'ivs']]) + '\n**EVs:** '
    fieldValue += '/'.join(['%d %s' % (pokeSet['evs'][EV], EV) for EV in pokeSet['evs']]) + '\n'
    try:  fieldValue += '**IVs:** ' + ', '.join(['%d %s' % (pokeSet['ivs'][IV], IV) for IV in pokeSet['ivs']]) + '\n```'
    except KeyError: fieldValue += '```'
    fieldValue += '\n'.join(['Move %d:    %s' % (index, move) for index, move in enumerate(pokeSet['moves'], start=1)]) + '```'
    if index == len(list(pokeData)): fieldValue += '\n<:Angreifer:846099096149164032>Angreifer#7055 <:Sachin:846101219415818240>Sachin#0353'
    else: fieldValue += '\n__***#---------------------------------------#***__'
    embedVar.add_field(name='```%s```' % set, value=fieldValue, inline=False)
  embedVar.set_thumbnail(url=embedThumbnail)
  
  return embedVar

def check_water_func(pokename):
  if int(pokename['FishingOnly']) == 1:
    return 'Fish '+'('+pokename['RequiredRod']+')'
  else:
    if int(pokename['Fishing']) == 1:
      return 'Surf/Fish '+'('+pokename['RequiredRod']+')'
    else :
      return 'Surf'


async def location_func():
  a = open('land_spawns_dump.txt', 'r')
  b = open('surf_spawns_dump.txt', 'r')
  json_data1 = json.loads(a.read())
  json_data2 = json.loads(b.read())
  a.close()
  b.close()
  MDN = {'[1, 1, 1]':'M/D/N', '[0, 1, 1]':'D/N', '[1, 1, 0]':'M/D', '[1, 0, 1]':'M/N', '[1, 0, 0]':'M', '[0, 1, 0]':'D', '[0, 0, 1]':'N'}
  location_data_land = {}
  temp_location = []
  dump_data = ""
  for location in json_data1:
    if location['Map'] not in temp_location:
      if len(temp_location) != 0:
        location_data_land.update({name:dump_data})
      temp_location.append(location['Map'])
      dump_data = {}
      dump_data.update({location['Pokemon']: {"Area": ['Land'], "Daytime": [MDN[str(location['Daytime'])]],"MinLVL": [location['MinLVL']], "MaxLVL": [location['MaxLVL']], "MemberOnly": [location['MemberOnly']], "Tier": [location['Tier']], "Item": [location['Item']]}})
      name = location['Map'].lower()
    else:
      dump_data.update({location['Pokemon'] : {"Area": ['Land'], "Daytime": [MDN[str(location['Daytime'])]],"MinLVL": [location['MinLVL']], "MaxLVL": [location['MaxLVL']], "MemberOnly": [location['MemberOnly']], "Tier": [location['Tier']], "Item": [location['Item']]}})

  location_data_water = []
  for location in json_data2:
    name = location['Map'].lower()
    rods = check_water_func(location)
    if name in location_data_land:
      if location['Pokemon'] in location_data_land[name]:
        
        location_data_land[name][location['Pokemon']]['Area'].append(rods)
        location_data_land[name][location['Pokemon']]['Daytime'].append(MDN[str(location['Daytime'])])
        location_data_land[name][location['Pokemon']]['MinLVL'].append(location['MinLVL'])
        location_data_land[name][location['Pokemon']]['MaxLVL'].append(location['MaxLVL'])
        location_data_land[name][location['Pokemon']]['MemberOnly'].append(location['MemberOnly'])
        location_data_land[name][location['Pokemon']]['Tier'].append(location['Tier'])
        location_data_land[name][location['Pokemon']]['Item'].append(location['Item'])
        
      else:
        location_data_land[name].update({location['Pokemon']: {"Area": [rods], "Daytime": [MDN[str(location['Daytime'])]],"MinLVL": [location['MinLVL']], "MaxLVL": [location['MaxLVL']], "MemberOnly": [location['MemberOnly']], "Tier": [location['Tier']], "Item": [location['Item']]}})
    else:
      if name not in location_data_water :
        location_data_water.append(name)
        location_data_land.update({name : {location['Pokemon']: {"Area": [rods], "Daytime": [MDN[str(location['Daytime'])]],"MinLVL": [location['MinLVL']], "MaxLVL": [location['MaxLVL']], "MemberOnly": [location['MemberOnly']], "Tier": [location['Tier']], "Item": [location['Item']]}}})
      else:
        location_data_land[name].update({location['Map']: {"Area": [rods], "Daytime": [MDN[str(location['Daytime'])]],"MinLVL": [location['MinLVL']], "MaxLVL": [location['MaxLVL']], "MemberOnly": [location['MemberOnly']], "Tier": [location['Tier']], "Item": [location['Item']]}})

  return location_data_land

async def spawn_func():
  #response1 = requests.get("https://pokemonrevolution.net/spawns/land_spawns.json")
  #response2 = requests.get("https://pokemonrevolution.net/spawns/surf_spawns.json")
  a = open('land_spawns_dump.txt', 'r')
  b = open('surf_spawns_dump.txt', 'r')
  json_data1 = json.loads(a.read())
  json_data2 = json.loads(b.read())
  a.close()
  b.close()
  MDN = {'[1, 1, 1]':'M/D/N', '[0, 1, 1]':'D/N', '[1, 1, 0]':'M/D', '[1, 0, 1]':'M/N', '[1, 0, 0]':'M', '[0, 1, 0]':'D', '[0, 0, 1]':'N'}
  pokemon_data_land = {}
  for pokemon in json_data1:
    name = pokemon['Pokemon'].lower()
    if name not in pokemon_data_land :
      pokemon_data_land.update({name : {pokemon['Map']: {"Area": ['Land'], "Daytime": [MDN[str(pokemon['Daytime'])]],"MinLVL": [pokemon['MinLVL']], "MaxLVL": [pokemon['MaxLVL']], "MemberOnly": [pokemon['MemberOnly']], "Tier": [pokemon['Tier']], "Item": [pokemon['Item']]}}})
    else:
      pokemon_data_land[name].update({pokemon['Map']: {"Area": ['Land'], "Daytime": [MDN[str(pokemon['Daytime'])]],"MinLVL": [pokemon['MinLVL']], "MaxLVL": [pokemon['MaxLVL']], "MemberOnly": [pokemon['MemberOnly']], "Tier": [pokemon['Tier']], "Item": [pokemon['Item']]}})
  
  pokemon_data_water = []
  for pokemon in json_data2:
    name = pokemon['Pokemon'].lower()
    rods = check_water_func(pokemon)
    if name in pokemon_data_land:
      if pokemon['Map'] in pokemon_data_land[name]:
        
        pokemon_data_land[name][pokemon['Map']]['Area'].append(rods)
        pokemon_data_land[name][pokemon['Map']]['Daytime'].append(MDN[str(pokemon['Daytime'])])
        pokemon_data_land[name][pokemon['Map']]['MinLVL'].append(pokemon['MinLVL'])
        pokemon_data_land[name][pokemon['Map']]['MaxLVL'].append(pokemon['MaxLVL'])
        pokemon_data_land[name][pokemon['Map']]['MemberOnly'].append(pokemon['MemberOnly'])
        pokemon_data_land[name][pokemon['Map']]['Tier'].append(pokemon['Tier'])
        pokemon_data_land[name][pokemon['Map']]['Item'].append(pokemon['Item'])
        
      else:
        pokemon_data_land[name].update({pokemon['Map']: {"Area": [rods], "Daytime": [MDN[str(pokemon['Daytime'])]],"MinLVL": [pokemon['MinLVL']], "MaxLVL": [pokemon['MaxLVL']], "MemberOnly": [pokemon['MemberOnly']], "Tier": [pokemon['Tier']], "Item": [pokemon['Item']]}})
    else:
      if name not in pokemon_data_water :
        pokemon_data_water.append(name)
        pokemon_data_land.update({name : {pokemon['Map']: {"Area": [rods], "Daytime": [MDN[str(pokemon['Daytime'])]],"MinLVL": [pokemon['MinLVL']], "MaxLVL": [pokemon['MaxLVL']], "MemberOnly": [pokemon['MemberOnly']], "Tier": [pokemon['Tier']], "Item": [pokemon['Item']]}}})
      else:
        pokemon_data_land[name].update({pokemon['Map']: {"Area": [rods], "Daytime": [MDN[str(pokemon['Daytime'])]],"MinLVL": [pokemon['MinLVL']], "MaxLVL": [pokemon['MaxLVL']], "MemberOnly": [pokemon['MemberOnly']], "Tier": [pokemon['Tier']], "Item": [pokemon['Item']]}})

  return pokemon_data_land


async def item_func():
  a = open('land_spawns_dump.txt', 'r')
  b = open('surf_spawns_dump.txt', 'r')
  json_data1 = json.loads(a.read())
  json_data2 = json.loads(b.read())
  a.close()
  b.close()
  MDN = {'[1, 1, 1]':'M/D/N', '[0, 1, 1]':'D/N', '[1, 1, 0]':'M/D', '[1, 0, 1]':'M/N', '[1, 0, 0]':'M', '[0, 1, 0]':'D', '[0, 0, 1]':'N'}
  item_data_land = {}
  temp_item = []
  for item in json_data1:
    if item['Item'] != None:
      low_item = item['Item'].lower()
      if item['Item'] not in temp_item:
        temp_item.append(item['Item'])
        item_data_land.update({low_item : {item['Pokemon']: {"Map": [item['Map']],"Area": ['Land'], "Daytime": [MDN[str(item['Daytime'])]],"MinLVL": [item['MinLVL']], "MaxLVL": [item['MaxLVL']], "MemberOnly": [item['MemberOnly']], "Tier": [item['Tier']]}}})
      else:
        if low_item in item_data_land.keys():
          if item['Pokemon'] in item_data_land[low_item].keys():
            item_data_land[low_item][item['Pokemon']]['Map'].append(item['Map'])
            item_data_land[low_item][item['Pokemon']]['Area'].append('Land')
            item_data_land[low_item][item['Pokemon']]['Daytime'].append(MDN[str(item['Daytime'])])
            item_data_land[low_item][item['Pokemon']]['MinLVL'].append(item['MinLVL'])
            item_data_land[low_item][item['Pokemon']]['MaxLVL'].append(item['MaxLVL'])
            item_data_land[low_item][item['Pokemon']]['MemberOnly'].append(item['MemberOnly'])
            item_data_land[low_item][item['Pokemon']]['Tier'].append(item['Tier'])
          else:
            item_data_land[low_item].update({item['Pokemon']: {"Map": [item['Map']],"Area": ['Land'], "Daytime": [MDN[str(item['Daytime'])]],"MinLVL": [item['MinLVL']], "MaxLVL": [item['MaxLVL']], "MemberOnly": [item['MemberOnly']], "Tier": [item['Tier']]}})
  
  item_data_water = []
  for item in json_data2:
    if item['Item'] != None:
      low_item = item['Item'].lower()
      rods = check_water_func(item)
      if low_item in item_data_land.keys():
        if item['Pokemon'] in item_data_land[low_item].keys():
            item_data_land[low_item][item['Pokemon']]['Map'].append(item['Map'])
            item_data_land[low_item][item['Pokemon']]['Area'].append(rods)
            item_data_land[low_item][item['Pokemon']]['Daytime'].append(MDN[str(item['Daytime'])])
            item_data_land[low_item][item['Pokemon']]['MinLVL'].append(item['MinLVL'])
            item_data_land[low_item][item['Pokemon']]['MaxLVL'].append(item['MaxLVL'])
            item_data_land[low_item][item['Pokemon']]['MemberOnly'].append(item['MemberOnly'])
            item_data_land[low_item][item['Pokemon']]['Tier'].append(item['Tier'])  
        else:
          item_data_land[low_item].update({item['Pokemon']: {"Map": [item['Map']],"Area": [rods], "Daytime": [MDN[str(item['Daytime'])]],"MinLVL": [item['MinLVL']], "MaxLVL": [item['MaxLVL']], "MemberOnly": [item['MemberOnly']], "Tier": [item['Tier']]}})
      else:
        item_data_land.update({low_item : {item['Pokemon']: {"Map": [item['Map']],"Area": [rods], "Daytime": [MDN[str(item['Daytime'])]],"MinLVL": [item['MinLVL']], "MaxLVL": [item['MaxLVL']], "MemberOnly": [item['MemberOnly']], "Tier": [item['Tier']]}}})
  return item_data_land