effectivenessData = {
  'Rock': {0.5: ['Normal', 'Fire', 'Poison', 'Flying'], 2: ['Water', 'Grass', 'Fighting', 'Ground', 'Steel']}, 
  'Ghost': {0: ['Normal', 'Fighting'], 0.5: ['Poison', 'Bug'], 2: ['Ghost', 'Dark']}, 
  'Fire': {0.5: ['Fire', 'Grass', 'Bug', 'Ice', 'Fairy', 'Steel'], 2: ['Water', 'Ground', 'Rock']}, 
  'Water': {0.5: ['Fire', 'Water', 'Ice', 'Steel'], 2: ['Electric', 'Grass']}, 
  'Grass': {2: ['Fire', 'Ice', 'Poison', 'Flying', 'Bug'], 0.5: ['Water', 'Electric', 'Grass', 'Ground']}, 
  'Ice': {2: ['Fire', 'Fighting', 'Rock', 'Steel'], 0.5: ['Ice']}, 
  'Bug': {2: ['Fire', 'Flying', 'Rock'], 0.5: ['Grass', 'Fighting', 'Ground']}, 
  'Dragon': {0.5: ['Fire', 'Water', 'Electric', 'Grass'], 2: ['Ice', 'Dragon', 'Fairy']}, 
  'Ground': {2: ['Water', 'Grass', 'Ice'], 0: ['Electric'], 0.5: ['Poison', 'Rock']}, 
  'Electric': {0.5: ['Electric', 'Flying', 'Steel'], 2: ['Ground']}, 
  'Flying': {2: ['Electric', 'Ice', 'Rock'], 0.5: ['Grass', 'Fighting', 'Bug'], 0: ['Ground']}, 
  'Poison': {0.5: ['Grass', 'Fighting', 'Poison', 'Bug', 'Fairy'], 2: ['Ground', 'Psychic']}, 
  'Normal': {2: ['Fighting'], 0: ['Ghost']}, 
  'Psychic': {0.5: ['Fighting', 'Psychic'], 2: ['Bug', 'Dark', 'Ghost']},
  'Fighting': {2: ['Flying', 'Psychic', 'Fairy'], 0.5: ['Bug', 'Rock', 'Dark']},
  'Steel': {2: ['Fire', 'Fighting', 'Ground'], 0.5: ['Normal', 'Grass', 'Ice', 'Flying', 'Psychic', 'Bug', 'Rock', 'Dragon', 'Fairy', 'Steel'], 0: ['Poison']},
  'Dark': {2: ['Fighting', 'Fairy', 'Bug'], 0: ['Psychic'], 0.5: ['Dark', 'Ghost']},
  'Fairy': {2: ['Poison', 'Steel'], 0:['Dragon'], 0.5:['Dark', 'Fighting', 'Bug']}
  }

effDict = {'Normal':1, 'Fire':1, 'Fighting':1,  'Water':1,  'Flying':1,  'Grass':1,  'Poison':1,  'Electric':1,  'Ground':1,  'Psychic':1,  'Rock':1,  'Ice':1,  'Bug':1,  'Dragon':1,  'Ghost':1,  'Dark':1,  'Steel':1,  'Fairy':1}