import os
import re
from asyncio import sleep, create_task
import time
import datetime
from dateutil.relativedelta import relativedelta

import discord
from discord.utils import get
from redbot.core import commands
from redbot.core import Config
from redbot.core import checks
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils import predicates


class Reminder(commands.Cog):
    '''Never forget anything anymore.'''

    def __init__(self, bot):
        self.bot = bot
        self.check = False
        self.config = Config.get_conf(self, identifier=847265238)
        default_user = {
            'reminders': []
        }
        self.config.register_user(**default_user)
        create_task(self.check_reminders())

    def cog_unload(self):
        self.check = False
        time.sleep(2)

    @commands.command(pass_context=True)
    async def remind(self, ctx, user: str, time_unit: str, *, text: str):
        '''Sends you <text> when the time is up

        Accepts: m, h, d, M, w, y
        Example:
        [p]remind me 3d6h Have sushi with Asu and JennJenn
        [p]remind Asu 2M2w Buy JennJenn a Coke'''

        if user == 'me':  # There might be a problem if a user exists with that name
            author = ctx.author
        else:
            author = get(ctx.bot.get_all_members(), display_name=user)
            if not author:
                await ctx.send(f'The user {user} doesn\'t exist!')
                return

        future_matches = re.findall(r'\d{1,2}\w', time_unit)
        unit_convert_dict = {
            'm': 'minutes',
            'h': 'hours',
            'd': 'days',
            'M': 'months',
            'w': 'weeks',
            'y': 'years'
        }

        delta = relativedelta()
        for m in future_matches:
            _, unit = re.split(r'\d+', m)
            delta_unit = unit_convert_dict.get(unit, 'minutes')
            delta += relativedelta(**{delta_unit: int(re.match(r'\d+', m).group())})
        future = (datetime.datetime.now() + delta)

        async with self.config.user(author).reminders() as reminders:
            reminders.append(
                {
                    'future': future.timestamp(),
                    'chan': ctx.channel.id,
                    'text': text
                }
            )
        await ctx.send(f'I will remind {author.name} that on {future.strftime("%c")}.')

    @commands.command(pass_context=True)
    async def forgetme(self, ctx):
        '''Removes all your upcoming notifications'''
        await self.config.user(ctx.author).clear()
        await ctx.send('All your notifications have been removed.')

    async def check_reminders(self):
        #await sleep(60)
        await self.bot.wait_until_ready()
        if not self.check:
            self.check = True
        while self.check:
            user_configs = await self.config.all_users()
            for user_id, user_config in list(user_configs.items()):
                for reminder in user_config['reminders']:
                    user = self.bot.get_user(user_id)
                    if int(reminder['future']) <= int(time.time()):
                        chan = self.bot.get_channel(reminder['chan'])
                        try:
                            await chan.send(f'{user.mention} remember to {reminder["text"]}')
                            async with self.config.user(user).reminders() as user_reminders:
                                user_reminders.remove(reminder)
                        except (discord.errors.Forbidden, discord.errors.NotFound, discord.errors.HTTPException):
                            pass
            await sleep(1)
