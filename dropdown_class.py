import disnake

from data_functions import pro_repel, headbutt_check_func, do_moves, do_ability, do_item, dig_func2, dig_func3, get_data, dex_embed, smogon_embed

from mod_data import emote_id
from keys import location_keys, spawn_keys


class Dropdown(disnake.ui.Select):
    def __init__(self, options, category, command_name, place, user):

        # Set the options that will be presented inside the dropdown
        options = options
        self.category = category
        self.command_name = command_name
        self.place = place
        self.user = user
        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder=place, min_values=1, max_values=1, options=options)

    async def callback(self, interaction: disnake.MessageInteraction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's 
        # selected options. We only want the first one.
        #await interaction.response.send_message(f'Your pokemon is {self.values[0]}')
        if interaction.user.id == self.user:
          if self.command_name == "repel":
            pro = pro_repel(self.values[0],self.category)
            msg = '\n'
            for data in pro:
              if len(msg) + len(data) >= 2000-6:
                msg = ''.join(['```', msg, '```'])
                await interaction.response.send_message(msg)
                msg = '\n'
              msg += data + '\n'
            msg = ''.join(['```', msg, '```'])
            await interaction.response.send_message(msg)
          elif self.command_name == "spawns":
            if self.values[0] in location_keys: category = '#Pokémon'
            elif self.values[0] in spawn_keys: category = '#Map'
            else:
              category = 'Item'
            spawns = get_data(self.values[0], category)
            if spawns == None: await interaction.response.send_message('Pokémon/Map could not be found.')
            else:
              msg = ''
              for data in spawns:
                if len(msg) + len(data) >= 2000-6:
                  msg = ''.join(['```', msg, '```'])
                  await interaction.channel.send(msg)
                  msg = '\n'
                msg += data + '\n'
              msg = ''.join(['```', msg, '```'])
              await interaction.response.send_message(msg)
          elif self.command_name == "headbutt":
            head = headbutt_check_func(self.values[0])
            msg = '\n'
            for data in head:
              if len(msg) + len(data) >= 2000-6:
                msg = ''.join(['```', msg, '```'])
                await interaction.channel.send_message(msg)
                msg = '\n'
              msg += data + '\n'
            msg = ''.join(['```', msg, '```'])
            await interaction.response.send_message(msg)
          elif self.command_name == "info":
            check = self.category[self.values[0]]
            if check == "move":
              data = do_moves(self.values[0])
            elif check == "ability":
              data = do_ability(self.values[0])
            elif check == "item":
              data = do_item(self.values[0])
            await interaction.response.send_message(data)
          elif self.command_name == "smogon":
            smogonEmbed = smogon_embed(self.values[0])
            await interaction.response.send_message(embed = smogonEmbed)
          elif self.command_name == "dex":
            dexEmbed = dex_embed(self.values[0])
            if dexEmbed == None: await interaction.response.send_message('Pokémon could not be found.')
            else: await interaction.response.send_message(embed = dexEmbed)
          elif self.command_name == "digspots":
            if self.values[0] == "All Locations only":
              data = dig_func2(self.category)
            else:
              data = dig_func3(self.category, self.values[0])
            await interaction.response.send_message(embed = data)
          self.view.stop()


class DropdownView(disnake.ui.View):
    def __init__(self, options, category, command_name, place, user):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(options, category, command_name, place, user))
        
