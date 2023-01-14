import requests
import json
#from mywork import types_work
#from monotype import monotype_data
#from locations import locations
from Combined import combined
from locations import locations
#---------------------------------------------

def repel_trick():
  data = locations
  land_data = {}
  for key1,value1 in data.items():
    S1 = 0
    a = []
    b = []
    for key2,value2 in value1.items():
      if 'Land' in value2['Area']:
        index = value2['Area'].index('Land')
        if 'M' in value2['Daytime'][index]:
          S1 += 1
          a.append(value2['MinLVL'][index]) 
          b.append(value2['MaxLVL'][index])
        else:
          continue
    r = []
    l = []
    q = []
    for t in a:
      if len(r) == 0 or t in r:
        r.append(t)
      elif len(l) == 0 or t in l:
        l.append(t)
      elif len(q) == 0 or t in q:
        q.append(t)
    if len(r) == 0:
      continue
    if len(l) == 0:
      l.append(0)
    if len(q) == 0:
      q.append(0)
    if S1 >= 7 :
      if len(r) <= 3 and r[0] > l[0] and r[0] > q[0]:
        repel_lower_level = r[0]
      elif len(l) <=3 and l[0] > r[0] and l[0] > q[0]:
        repel_lower_level = l[0]
      elif len(q) <=3 and q[0] > r[0] and q[0] > l[0]:
        repel_lower_level = q[0]
      try:
        if repel_lower_level in b:
          continue
        repel_lower_level_index = a.index(repel_lower_level)
        repel_higher_level = b[repel_lower_level_index]
        check = "True"
      except:
        check = "False"
    else:
      if len(r) <= 2 and r[0] > l[0] and r[0] > q[0]:
        repel_lower_level = r[0]
      elif len(l) <=2 and l[0] > r[0] and l[0] > q[0]:
        repel_lower_level = l[0]
      elif len(q) <=2 and q[0] > r[0] and q[0] > l[0]:
        repel_lower_level = q[0]
      try:
        if repel_lower_level in b:
          continue
        repel_lower_level_index = a.index(repel_lower_level)
        repel_higher_level = b[repel_lower_level_index]
        check = "True"
      except:
        check = "False"
    if check == "True":
      for key2,value2 in value1.items():
        if 'Land' in value2['Area'] and repel_lower_level in value2['MinLVL'] :
          index = value2['Area'].index('Land')
          if key2 not in land_data.keys() : 
            land_data.update({key2:[{"location":key1,"Area":"Land","Daytime":"M","MemberOnly":value2['MemberOnly'][index],"Tier":value2['Tier'][index],"MinLVL":[repel_lower_level],"MaxLVL":[repel_higher_level]}]})
          else:
            land_data[key2].append({"location":key1,"Area":"Land","Daytime":"M","MemberOnly":value2['MemberOnly'][index],"Tier":value2['Tier'][index],"MinLVL":[repel_lower_level],"MaxLVL":[repel_higher_level]})
  for key1,value1 in data.items():
    S1 = 0
    a = []
    b = []
    for key2,value2 in value1.items():
      if 'Land' in value2['Area']:
        index = value2['Area'].index('Land')
        if 'D' in value2['Daytime'][index]:
          S1 += 1
          a.append(value2['MinLVL'][index]) 
          b.append(value2['MaxLVL'][index])
        else:
          continue
    r = []
    l = []
    q = []
    for t in a:
      if len(r) == 0 or t in r:
        r.append(t)
      elif len(l) == 0 or t in l:
        l.append(t)
      elif len(q) == 0 or t in q:
        q.append(t)
    if len(r) == 0:
      continue
    if len(l) == 0:
      l.append(0)
    if len(q) == 0:
      q.append(0)
    if S1 >= 7 :
      if len(r) <= 3 and r[0] > l[0] and r[0] > q[0]:
        repel_lower_level = r[0]
      elif len(l) <=3 and l[0] > r[0] and l[0] > q[0]:
        repel_lower_level = l[0]
      elif len(q) <=3 and q[0] > r[0] and q[0] > l[0]:
        repel_lower_level = q[0]
      try:
        if repel_lower_level in b:
          continue
        repel_lower_level_index = a.index(repel_lower_level)
        repel_higher_level = b[repel_lower_level_index]
        check = "True"
      except:
        check = "False"
    else:
      if len(r) <= 2 and r[0] > l[0] and r[0] > q[0]:
        repel_lower_level = r[0]
      elif len(l) <=2 and l[0] > r[0] and l[0] > q[0]:
        repel_lower_level = l[0]
      elif len(q) <=2 and q[0] > r[0] and q[0] > l[0]:
        repel_lower_level = q[0]
      try:
        if repel_lower_level in b:
          continue
        repel_lower_level_index = a.index(repel_lower_level)
        repel_higher_level = b[repel_lower_level_index]
        check = "True"
      except:
        check = "False"
    if check == "True":
      for key2,value2 in value1.items():
        if 'Land' in value2['Area'] and repel_lower_level in value2['MinLVL'] :
          index = value2['Area'].index('Land')
          if key2 not in land_data.keys() : 
            land_data.update({key2:[{"location":key1,"Area":"Land","Daytime":"D","MemberOnly":value2['MemberOnly'][index],"Tier":value2['Tier'][index],"MinLVL":[repel_lower_level],"MaxLVL":[repel_higher_level]}]})
          else:
            land_data[key2].append({"location":key1,"Area":"Land","Daytime":"D","MemberOnly":value2['MemberOnly'][index],"Tier":value2['Tier'][index],"MinLVL":[repel_lower_level],"MaxLVL":[repel_higher_level]})
  for key1,value1 in data.items():
    S1 = 0
    a = []
    b = []
    for key2,value2 in value1.items():
      if 'Land' in value2['Area']:
        index = value2['Area'].index('Land')
        if 'N' in value2['Daytime'][index]:
          S1 += 1
          a.append(value2['MinLVL'][index]) 
          b.append(value2['MaxLVL'][index])
        else:
          continue
    r = []
    l = []
    q = []
    for t in a:
      if len(r) == 0 or t in r:
        r.append(t)
      elif len(l) == 0 or t in l:
        l.append(t)
      elif len(q) == 0 or t in q:
        q.append(t)
    if len(r) == 0:
      continue
    if len(l) == 0:
      l.append(0)
    if len(q) == 0:
      q.append(0)
    if S1 >= 7 :
      if len(r) <= 3 and r[0] > l[0] and r[0] > q[0]:
        repel_lower_level = r[0]
      elif len(l) <=3 and l[0] > r[0] and l[0] > q[0]:
        repel_lower_level = l[0]
      elif len(q) <=3 and q[0] > r[0] and q[0] > l[0]:
        repel_lower_level = q[0]
      try:
        if repel_lower_level in b:
          continue
        repel_lower_level_index = a.index(repel_lower_level)
        repel_higher_level = b[repel_lower_level_index]
        check = "True"
      except:
        check = "False"
    else:
      if len(r) <= 2 and r[0] > l[0] and r[0] > q[0]:
        repel_lower_level = r[0]
      elif len(l) <=2 and l[0] > r[0] and l[0] > q[0]:
        repel_lower_level = l[0]
      elif len(q) <=2 and q[0] > r[0] and q[0] > l[0]:
        repel_lower_level = q[0]
      try:
        if repel_lower_level in b:
          continue
        repel_lower_level_index = a.index(repel_lower_level)
        repel_higher_level = b[repel_lower_level_index]
        check = "True"
      except:
        check = "False"
    if check == "True":
      for key2,value2 in value1.items():
        if 'Land' in value2['Area'] and repel_lower_level in value2['MinLVL'] :
          index = value2['Area'].index('Land')
          if key2 not in land_data.keys() : 
            land_data.update({key2:[{"location":key1,"Area":"Land","Daytime":"N","MemberOnly":value2['MemberOnly'][index],"Tier":value2['Tier'][index],"MinLVL":[repel_lower_level],"MaxLVL":[repel_higher_level]}]})
          else:
            land_data[key2].append({"location":key1,"Area":"Land","Daytime":"N","MemberOnly":value2['MemberOnly'][index],"Tier":value2['Tier'][index],"MinLVL":[repel_lower_level],"MaxLVL":[repel_higher_level]})            
  return land_data








def check_water(pokename):
  if int(pokename['FishingOnly']) == 1:
    return 'Fish '+'('+pokename['RequiredRod']+')'
  else:
    if int(pokename['Fishing']) == 1:
      return 'Surf/Fish '+'('+pokename['RequiredRod']+')'
    else :
      return 'Surf'
def find_abilities():
  response = requests.get("https://raw.githubusercontent.com/Touched/pokedex-data/master/tables/abilities.json")
  json_data = json.loads(response.text)
  sachin = {}
  for key,value in json_data.items():
    sachin.update({key:{"name":value['name']['english'],"description":value['description']['english']}})
  return sachin

def find_items():
  response = requests.get("https://raw.githubusercontent.com/Touched/pokedex-data/master/tables/items.json")
  json_data = json.loads(response.text)
  sachin = {}
  for key,value in json_data.items():
    sachin.update({key:{"name":value['name']['english'],"description":value['description']['english'],"type":value['type']}})
  return sachin

'''
def find_moves():
  response = requests.get("https://raw.githubusercontent.com/Touched/pokedex-data/master/tables/moves.json")
  json_data = json.loads(response.text)
  sachin = {}
  for key,value in json_data.items():
    sachin.update({key:{"name":value['name']['english'],"description":value['description']['english'],"category":value['category'],"power":value['power'],"pp":value['pp'],"priority":value['priority'],"type":value['type'],"accuracy":value['accuracy'],"secondary":value['secondary']}})
  return sachin
'''


def location():
  response1 = requests.get("https://pokemonrevolution.net/spawns/land_spawns.json")
  response2 = requests.get("https://pokemonrevolution.net/spawns/surf_spawns.json")
  json_data1 = json.loads(response1.text)
  json_data2 = json.loads(response2.text)
  MDN = {'[1, 1, 1]':'M/D/N', '[0, 1, 1]':'D/N', '[1, 1, 0]':'M/D', '[1, 0, 1]':'M/N', '[1, 0, 0]':'M', '[0, 1, 0]':'D', '[0, 0, 1]':'N'}
  location_data_land = {}
  temp_location = []
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
    rods = check_water(location)
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

def spawn():
  response1 = requests.get("https://pokemonrevolution.net/spawns/land_spawns.json")
  response2 = requests.get("https://pokemonrevolution.net/spawns/surf_spawns.json")
  json_data1 = json.loads(response1.text)
  json_data2 = json.loads(response2.text)
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
    rods = check_water(pokemon)
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


#code if we want to update the json files
#@client.event
#async def on_ready():
  '''
  global locations
  locations = location()
  a = open("locations.py","w")
  a.write("locations = " + str(locations))
  global Spawns
  Spawns = spawn()
  b = open("spawns.py","w")
  b.write("Spawns = " + str(Spawns))
  global items
  items = item()
  c = open("items.py","w")
  c.write("Items = " + str(items))
  global combined
  combined = locations
  combined.update(Spawns)
  combined.update(items)
  d = open("Combined.py","w")
  d.write("combined = " + str(combined))
  '''
#  print('We have logged in as {0.user}'.format(client))

def item():
  response1 = requests.get("https://pokemonrevolution.net/spawns/land_spawns.json")
  response2 = requests.get("https://pokemonrevolution.net/spawns/surf_spawns.json")
  json_data1 = json.loads(response1.text)
  json_data2 = json.loads(response2.text)
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
      rods = check_water(item)
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


def next_evolve(sachin,json_data):
  full_data = []
  test_data = []
  next_data = []
  for item in sachin['evolution']['next']:
    data_no = int(item[0])
    if data_no < 810 :  
      next_evo_no = int(item[0])
      next_evo_name = json_data[next_evo_no - 1]['name']['english']
      data_with_name = [next_evo_name,item[1]]
      next_data.append(data_with_name)
  if len(next_data) != 0:
    full_data.append(next_data)
  next_data2 = []
  test_data.append(sachin['evolution']['next'])
  for item in test_data[0]:
    data_no = int(item[0])
    if data_no < 810 :
      next_evo = json_data[data_no - 1]
      if 'next' in next_evo['evolution'].keys():
        for item in next_evo['evolution']['next']:
          next_evo_no = int(item[0])
          if next_evo_no < 810 :
            next_evo_name = json_data[next_evo_no - 1]['name']['english']
            data_with_name = [next_evo_name,item[1]]
            next_data2.append(data_with_name)
  if len(next_data2) != 0:
    full_data.append(next_data2)
  return full_data

def prev_evolve(sachin,json_data):
  full_data = []
  test_data = []
  prev_evo_no = int(sachin['evolution']['prev'][0])
  if prev_evo_no < 810 :
    prev_evo_name = json_data[prev_evo_no - 1]['name']['english']
    data_with_name = [prev_evo_name,sachin['evolution']['prev'][1]]
    full_data.append(data_with_name)
  test_data.append(sachin['evolution']['prev'])
  for item in test_data:

    data_no = int(item[0])


    prev_evo = json_data[data_no - 1]
    if 'prev' in prev_evo['evolution'].keys():
      prev_evo_no = int(prev_evo['evolution']['prev'][0])
      if prev_evo_no < 810 :
        prev_evo_name1 = json_data[prev_evo_no - 1]['name']['english']
        data_with_name = [prev_evo_name1,prev_evo['evolution']['prev'][1]]
        full_data.append(data_with_name)
  return full_data
  

def dex():
  response = requests.get('https://raw.githubusercontent.com/Purukitto/pokemon-data.json/master/pokedex.json')
  json_data = json.loads(response.text)
  pokemon_data = {}
  for sachin in json_data:
    typing = sachin['type']
    
    if 'prev' in sachin['evolution'].keys() and 'next' in sachin['evolution'].keys():
      nexts = next_evolve(sachin,json_data)
      previous = prev_evolve(sachin,json_data)
      pokemon_data.update({sachin['name']['english']:{"Id":sachin['id'],"Type":sachin['type'],"Description":sachin['description'],"Ability":sachin['profile']['ability'],"Base":sachin['base'],"prev":previous,"next":nexts}})
    elif 'prev' not in sachin['evolution'].keys() and 'next' in sachin['evolution'].keys():
      nexts = next_evolve(sachin,json_data)
      pokemon_data.update({sachin['name']['english']:{"Id":sachin['id'],"Type":sachin['type'],"Description":sachin['description'],"Ability":sachin['profile']['ability'],"Base":sachin['base'],"prev":[],"next":nexts}})
    elif 'prev' in sachin['evolution'].keys() and 'next' not in sachin['evolution'].keys():
      previous = prev_evolve(sachin,json_data)
      pokemon_data.update({sachin['name']['english']:{"Id":sachin['id'],"Type":sachin['type'],"Description":sachin['description'],"Ability":sachin['profile']['ability'],"Base":sachin['base'],"prev":previous,"next":[]}})
    else:
      pokemon_data.update({sachin['name']['english']:{"Id":sachin['id'],"Type":sachin['type'],"Description":sachin['description'],"Ability":sachin['profile']['ability'],"Base":sachin['base'],"prev":[],"next":[]}})
  
  return pokemon_data


def type_effect():
  '''
  response = requests.get('https://raw.githubusercontent.com/pcattori/pokemon/master/pokemon/data/type_effectiveness.json')
  return response.text
  json_data = [response.text]
  '''
  json_data = types_work
  blade = {}
  for item in json_data:
    name = str([item['defend'].capitalize()])
    if item['effectiveness'] != 1:
      if item['effectiveness'] == 2:
        if name not in list(blade.keys()):
          blade.update({name:{"2":[item['attack'].capitalize()]}})
        else:
          if '2' not in blade[name].keys():
            blade[name].update({"2":[item['attack'].capitalize()]})
          else:
            blade[name]["2"].append(item['attack'].capitalize())
      elif item['effectiveness'] == 0.5:
        if name not in list(blade.keys()):
          blade.update({name:{"½":[item['attack'].capitalize()]}})
        else:
          if '½' not in blade[name].keys():
            blade[name].update({"½":[item['attack'].capitalize()]})
          else:
            blade[name]["½"].append(item['attack'].capitalize())
      elif item['effectiveness'] == 0:
        if name not in list(blade.keys()):
          blade.update({name:{"0":[item['attack'].capitalize()]}})
        else:
          if '0' not in blade[name].keys():
            blade[name].update({"0":[item['attack'].capitalize()]})
          else:
            blade[name]["0"].append(item['attack'].capitalize())
  

  return blade


'''
def type_effective():
  types = monotype_data
  final_data = {}
  for type1 in types:
    for type2 in types:
      if type1 != type2 :
        name1 = eval(type1)
        name2 = eval(type2)
        name1.append(name2)
        name = str(name1)
        data1 = types[type1]
        data2 = types[type2]
        key_data = {}
        for key1 in data1:
          for key2 in data2:
            if key1 == '½':
              test1 = 0.5
            else:
              test1 = int(key1)
            if key2 == '½':
              test2 = 0.5
            else:
              test2 = int(key2)
            key_dict = {}
            for item1 in types[type1][key1]:
              for item2 in types[type2][key2]:
                if item1 == item2:
                  to_do = test1*test2
                  if to_do == 4:
                    if "4" not in key_dict :
                      key_dict.update({"4":[item1]})
                    else:
                      key_dict['4'].append(item1)
                  elif to_do == 2:
                    if "2" not in key_dict :
                      key_dict.update({"2":[item1]})
                    else:
                      key_dict['2'].append(item1)
                  elif to_do == 0.5:
                    if "½" not in key_dict:
                      key_dict.update({"½":[item1]})
                    else:
                      key_dict['½'].append(item1)
                  elif to_do == 0.25:
                    if "¼" not in key_dict:
                      key_dict.update({"¼":[item1]})
                    else:
                      key_dict['¼'].append(item1)
                  elif to_do == 0:
                    if "0" not in key_dict:
                      key_dict.update({"0":[item1]})
                    else:
                      key_dict['0'].append(item1)
            empty_list = []
            if "4" in key_dict.keys():
              key_data.update({"4":key_dict['4']})
              empty_list.append(key_dict['4'])
            if "2" in key_dict.keys():
              key_data.update({"2":key_dict['2']})
              empty_list.append(key_dict['2'])
            if "½" in key_dict.keys(): 
              key_data.update({"½":key_dict['½']})
              empty_list.append(key_dict['½'])
            if "¼" in key_dict.keys(): 
              key_data.update({"¼":key_dict['¼']})
              empty_list.append(key_dict['¼'])
            if "0" in key_dict.keys(): 
              key_data.update({"0":key_dict['0']})
              empty_list.append(key_dict['0'])
            for item1 in types[type1][key1]:
              if item1 not in empty_list:
                if 

                if "2" in key_data.keys():
                  key_data[key1].append(item1)
                  empty_list.append(item1)
                else:
                  key_data.update({"2":item1})
                  empty_list.append(item1)
                if "½" in key_data.keys():
                  key_data[key1].append(item1)
                  empty_list.append(item1)
                else:
                  key_data.update({"½":item1})
                  empty_list.append(item1)
        final_data.update({name: key_data})
  return final_data
'''

def smogon():
  response = requests.get("https://raw.githubusercontent.com/pokemondev/smogon-stats-discord/master/data/smogon-sets/gen6-sets.json")
  json_data = json.loads(response.text)
  smogon_sets = {}
  for pokemon in json_data.keys():
    pokemon_value = json_data[pokemon]
    for sets in pokemon_value.keys():
      love = str(sets)
      sets_value = pokemon_value[sets]
      if json_data[pokemon][sets]['level'] == 100 and 'Doubles' not in love and 'vgc' not in love and '1v1' not in love:
        if pokemon not in smogon_sets.keys():
          smogon_sets.update({pokemon:{sets:sets_value}})
        else:
          smogon_sets[pokemon].update({sets:sets_value})
  return smogon_sets
      
