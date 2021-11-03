from operator import itemgetter
from random import choice

import discord
from typing import Union
from datetime import datetime, timedelta
from redbot.core import commands
from redbot.core import checks
from redbot.core import Config
from redbot.core.utils.chat_formatting import pagify


class VoteUtils(commands.Cog):
    '''Some features for reaction based votes'''

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=847265212)
        default_guild = {
            'chan': ''
        }
        self.config.register_guild(**default_guild)

    @commands.group(pass_context=True, autohelp=False)
    @checks.admin_or_permissions(administrator=True)
    async def votes(self, ctx):
        channel = self.bot.get_channel(await self.config.chan())
        if not channel:
            await ctx.send('No channel set, use `[p]votes chan <channel>` first.')
            return
        if ctx.invoked_subcommand:
            return
        content_list = []
        voters = []
        after_days = datetime.utcnow() - timedelta(days=20)
        msgs = await channel.history(after=after_days).flatten()
        for msg in msgs:
            try:
                # This never happens
                if 'staff' in msg.author.roles:
                    continue
            except AttributeError:
                pass
            for reaction in msg.reactions:
                if reaction.emoji == '👍':
                    voters.extend(await reaction.users().flatten())
                    content_list.append((reaction.count, msg.author.mention, msg.content.split('\n')[0]))

        content_list.sort(key=itemgetter(0), reverse=True)
        content = ''
        for line in content_list:
            content += '{} - {}: {}\n'.format(*line)

        pages = pagify(content)
        for page in pages:
            embed = discord.Embed(description=page)
            embed.title = f'Votes in #{channel.name}'
            embed.colour = discord.Colour.green()
            embed.set_footer(text=f'A.T.S.P.', icon_url='https://yamahi.eu/favicon-512.png')
            await ctx.send(embed=embed)

        content_voter = ''
        for voter in voters:
            if voter.display_name not in content_voter:
                roles = [role.name for role in voter.roles]
                if 'Staff' not in roles:
                    content_voter += f'{voter.display_name}\n'
        pages = pagify(content_voter)
        for page in pages:
            embed = discord.Embed(description=page)
            embed.title = f'Voters in #{channel.name}'
            embed.colour = discord.Colour.green()
            embed.set_footer(text=f'A.T.S.P.', icon_url='https://yamahi.eu/favicon-512.png')
            await ctx.send(embed=embed)

    @votes.command(name='chan', pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def chan(self, ctx, chan: discord.TextChannel):
        '''Set the channel for the votes'''
        await self.config.chan.set(chan.id)
        await ctx.send(f'The channel {chan.mention} for votes is saved!')

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def raffle(self, ctx, message: discord.Message, emoji_name: Union[discord.Emoji, str]):
        '''Choose a winner between reactions from message id'''
        # To get default and custom emojis, Union is used
        participants = []
        try:
            emoji = discord.utils.get(ctx.message.guild.emojis, name=emoji_name.name)
        except AttributeError:
            emoji = emoji_name
        for reaction in message.reactions:
            if reaction.emoji != emoji:
                continue
            participants = await reaction.users().flatten()
            break
        try:
            winner = choice(participants)
        except IndexError:
            await ctx.send('No reactions with that emoji found')
            return
        participants_list = ''
        for participant in participants:
            participants_list += f'{participant.display_name}\n'
        embed = discord.Embed(description=f'... is the winner of the raffle!\nAll participants:\n{participants_list}')
        embed.title = winner.display_name
        embed.colour = discord.Colour.green()
        embed.set_footer(text=f'A.T.S.P.', icon_url='https://yamahi.eu/favicon-512.png')
        await ctx.send(embed=embed)
