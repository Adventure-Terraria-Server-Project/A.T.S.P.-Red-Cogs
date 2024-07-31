import re
from random import choice
import requests
import discord
from time import time
from redbot.core import commands

class ProtonDB(commands.Cog):
    def __init__(self):
        self.game_url = 'https://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json'
        self.protondb_url = 'https://www.protondb.com/api/v1/reports/summaries/'
        self.games = dict()
        self.games['time'] = None
        self.emojis = dict()
        self.emojis['platinum'] = ':medal:'
        self.emojis['gold'] = ':first_place:'
        self.emojis['silver'] = ':second_place:'
        self.emojis['bronze'] = ':third_place:'
        self.emojis['borked'] = [':face_vomiting:', ':person_facepalming:', ':skull_crossbones:', ':manual_wheelchair:', ':clown:']


    @commands.group(pass_context=True, autohelp=False)
    async def pdb(self, ctx, *, game: str):
        if not self.games['time'] or int(self.games['time']) < time() - 3600:
            r = requests.get(self.game_url)
            self.games['games'] = r.json()['applist']['apps']
            self.games['time'] = time()
        game_found = [game_index for game_index in self.games['games'] if re.sub(r'\W+', '', game_index['name']) == re.sub(r'\W+', '', game)]
        if game_found:
            game_found = game_found[0]
        else:
            await ctx.send('Game not found')
            return
        pr = requests.get(self.protondb_url + str(game_found['appid']) + '.json')
        try:
            tier = pr.json()['tier']
        except requests.exceptions.JSONDecodeError:
            await ctx.send('Game not on ProtonDB.')
            return
        if tier == 'borked':
            emoji = choice(self.emojis['borked'])
        else:
            emoji = self.emojis[tier]
        embed = discord.Embed(description=f'{emoji} {tier.capitalize()}')
        embed.title = game
        embed.url = f'https://www.protondb.com/app/{game_found["appid"]}'
        embed.colour = discord.Colour.red()
        embed.set_footer(text=f'AppID: {str(game_found["appid"])}',
                         icon_url='https://www.protondb.com/sites/protondb/images/favicon-16x16.png')
        await ctx.send(embed=embed)