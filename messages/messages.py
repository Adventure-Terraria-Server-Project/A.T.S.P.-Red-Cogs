import discord
from asyncio import sleep, create_task
from redbot.core import commands
from redbot.core import Config
from redbot.core import checks
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils import predicates


class Messages(commands.Cog):
    '''Welcome message and periodic messages'''

    def __init__(self, bot):
        self.bot = bot
        self.bc = False
        self.config = Config.get_conf(self, identifier=847265238)
        default_global = {
            'bc': [],
            'chan': '',
            'delay': 300,
            'welcome': ['chan', 'text']
        }
        self.config.register_global(**default_global)
        create_task(self.startup())

    def cog_unload(self):
        self.terminate = True
        self.bc = False
        sleep(2)

    async def startup(self):
        await self.bot.wait_until_ready()
        chan = self.bot.get_channel(await self.config.chan())
        await self.msg(chan)

    # Welcome-Code
    @commands.group()
    @checks.admin_or_permissions(administrator=True)
    async def welcome(self, ctx):
        '''Set a channel and a message for new members'''
        pass

    @welcome.command(name='chan', pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def wchan(self, ctx, chan: discord.TextChannel):
        '''Set the channel for the welcome message'''
        async with self.config.welcome() as welcome:
            welcome[0] = chan.id
        await ctx.send(f'The channel #{chan.name} for Welcome is saved!')

    @welcome.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def text(self, ctx, *, text: str):
        '''Set the welcome message - put member.mention to mention the user'''
        async with self.config.welcome() as welcome:
            welcome[1] = text
        await ctx.send('Welcome message saved!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        chanid, text = await self.config.welcome()
        if chanid and text:
            chan = self.bot.get_channel(chanid)
            if chan:
                await chan.send(text.replace('member.mention', member.mention))

    # Broadcast-Code
    @commands.group()
    @checks.mod_or_permissions(manage_messages=True)
    async def msgs(self, ctx):
        '''Manage periodic messages (broadcast)'''
        pass

    @msgs.command()
    @checks.mod_or_permissions(manage_messages=True)
    async def stop(self, ctx):
        '''Stop the broadcast'''
        self.bc = False

    @msgs.command(pass_context=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def start(self, ctx):
        chan = self.bot.get_channel(await self.config.chan())
        await self.msg(chan)

    async def msg(self, chan):
        '''Start the broadcast'''
        bc = await self.config.bc()
        if self.bc:
            await self.bot.send_to_owners('Broadcast is already running!')
            return
        if len(bc) == 0:
            await self.bot.send_to_owners('You have no messages set...')
            return
        if not chan:
            await self.bot.send_to_owners('You didn\'t set a channel')
            return
        self.bc = True
        while self.bc:
            for msg in bc:
                if self.bc:
                    await chan.send(':loudspeaker: ' + msg)
                    for sec in range(await self.config.delay()):
                        await sleep(1)
                        if not self.bc:
                            break
                else:
                    break
        await self.msg_error('Broadcast stopped!')

    @msgs.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def list(self, ctx):
        '''List the Messages'''
        index = 0
        bc = await self.config.bc()
        if len(bc) != 0:
            msg = ''
            for i in bc:
                msg += f'*{index}*: {i}\n'
                index += 1
            for page in pagify(msg):
                embed = discord.Embed(description=page)
                embed.title = 'Broadcast Messages'
                embed.colour = discord.Colour.blue()
                chanid = await self.config.chan()
                delay = await self.config.delay()
                chan = self.bot.get_channel(chanid)
                if chan:
                    embed.set_footer(text=f'Channel: #{chan.name} - Delay: {delay} seconds', icon_url='https://yamahi.eu/favicon-512.png')
                    await ctx.send(embed=embed)
                else:
                    ctx.send('No channel set.')
        else:
            await ctx.send('You didn\'t set any messages...')

    @msgs.command(name='chan', pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def bchan(self, ctx, chan: discord.TextChannel):
        '''Set the channel for the broadcast'''
        await self.config.chan.set(chan.id)
        await ctx.send(f'The channel {chan.mention} for Broadcast is saved!')

    @msgs.command()
    @checks.admin_or_permissions(administrator=True)
    async def delay(self, ctx, seconds: int):
        '''Set the delay in seconds'''
        await self.config.delay.set(seconds)
        await ctx.send(f'Broadcast delay set to {seconds}!')

    @msgs.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def add(self, ctx, *, text: str):
        '''Add a message'''
        if self.bc:
            self.bc = False
        async with self.config.bc() as bc:
            bc.append(text)
        await ctx.send('New Broadcast message added!')

    @msgs.command()
    @checks.admin_or_permissions(administrator=True)
    async def rm(self, ctx, index: int):
        '''Remove a message'''
        try:
            if self.bc:
                self.bc = False
            async with self.config.bc() as bc:
                bc.pop(index)
                await ctx.send('Broadcast message removed!')
        except IndexError:
            await ctx.send('The number was wrong...')
