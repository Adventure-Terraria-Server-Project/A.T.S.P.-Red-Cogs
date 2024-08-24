from dis import disco
from random import choice
import requests
import discord
from time import time
from rapidfuzz import utils
from rapidfuzz import process
from redbot.core import commands

class ProtonDB(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_url = 'https://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json'
        self.protondb_url = 'https://www.protondb.com/api/v1/reports/summaries/'
        self.games = dict()
        self.games['time'] = None
        self.reactions = ['1️⃣', '2️⃣', '3️⃣']
        self.ogames = {self.reactions[0]: None, self.reactions[1]: None, self.reactions[2]: None}
        self.emojis = dict()
        self.emojis['platinum'] = ':medal:'
        self.emojis['gold'] = ':first_place:'
        self.emojis['silver'] = ':second_place:'
        self.emojis['bronze'] = ':third_place:'
        self.emojis['pending'] = ':hourglass:'
        self.emojis['borked'] = [':face_vomiting:', ':person_facepalming:', ':skull_crossbones:', ':manual_wheelchair:', ':clown:']

    async def message_content(self, igame: str=None, appid: int=None):
        embed = None
        if not appid:
            if not self.games['time'] or int(self.games['time']) < time() - 3600:
                self.games['games'] = None
                r = requests.get(self.game_url)
                games_raw = r.json()['applist']['apps']
                self.games['games'] = {game['name']: game['appid'] for game in games_raw}
                self.games['time'] = time()
            games_found = process.extract(igame, self.games['games'].keys(), limit=4, processor=utils.default_process)
            if not games_found:
                embed = discord.Embed(description=':x: No games found on Steam.')
                embed.title = igame
            game_found = games_found[0][0]
            games = [(game[0], self.games['games'][game[0]]) for game in games_found]
            appid = games[0][1]
        else:
            games = None
            game_found = igame

        pr = requests.get(self.protondb_url + str(appid) + '.json')
        tier = None
        try:
            tier = pr.json()['tier']
        except requests.exceptions.JSONDecodeError:
            embed = discord.Embed(description=':x: Not on ProtonDB.')
            embed.title = game_found
        if tier:
            if tier == 'borked':
                emoji = choice(self.emojis['borked'])
            else:
                emoji = self.emojis[tier]
        if not embed:
            embed = discord.Embed(description=f'{emoji} {tier.capitalize()}')
            embed.title = game_found
            embed.url = f'https://www.protondb.com/app/{appid}'
            embed.colour = discord.Colour.red()
            embed.set_footer(text=f'AppID: {str(appid)}',
                             icon_url='https://www.protondb.com/sites/protondb/images/favicon-16x16.png')
        if games:
            other_games = ''
            for i, game in enumerate(games[1:]):
                other_games += f'{self.reactions[i]} {game[0]}\n'
            embed.add_field(name='Similar Games', value=other_games)
        return embed, games

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.author == user:
            return
        if reaction.message.author == self.bot.user:
            game = self.ogames.get(reaction.emoji)
            if game:
                embed, games = await self.message_content(igame=game[0], appid=game[1])
                await reaction.message.reply(embed=embed)

    @commands.group(pass_context=True, autohelp=False)
    async def pdb(self, ctx, *, igame: str):
        embed, games = await self.message_content(igame=igame)
        msg = await ctx.send(embed=embed)
        for i, game in enumerate(games[1:]):
            self.ogames[self.reactions[i]] = game
            await msg.add_reaction(self.reactions[i])
