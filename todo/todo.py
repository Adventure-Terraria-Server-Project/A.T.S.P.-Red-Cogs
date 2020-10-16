import discord
from redbot.core import commands
from redbot.core import Config
from redbot.core.utils.chat_formatting import pagify


class ToDo(commands.Cog):
    '''Manage your ToDo list'''

    def __init__(self):
        self.config = Config.get_conf(self, identifier=847265238)
        default_member = {
            'todos': []
        }
        self.config.register_member(**default_member)

    @commands.group(pass_context=True, autohelp=False)
    async def todo(self, ctx):
        '''Make your own ToDo list and manage it'''
        if ctx.invoked_subcommand is None:
            member_todos = await self.config.member(ctx.author).todos()
            index = 0
            if len(member_todos) == 0 or not member_todos:
                await ctx.send('You have nothing to do! :D')
                return
            msg = ''
            for i in member_todos:
                msg += f'*{index}*: {i}\n'
                index += 1
            page_index = 1
            pages = pagify(msg)
            for page in pages:
                nick = ctx.author.nick or ctx.author.name
                embed = discord.Embed(description=page)
                embed.title = f'{nick}\'s ToDo of {len(member_todos)} things'
                embed.colour = discord.Colour.green()
                embed.set_footer(text=f'Part {page_index}', icon_url='https://yamahi.eu/favicon-512.png')
                await ctx.send(embed=embed)
                page_index += 1

    @todo.command(pass_context=True)
    async def add(self, ctx, *, text: str):
        '''Add something to do'''
        if len(text) <= 200:
            async with self.config.member(ctx.author).todos() as member_todos:
                member_todos.append(text)
            await ctx.send('New ToDo added!')
        else:
            await ctx.send('Max. 200 characters allowed!')

    @todo.command(pass_context=True)
    async def insert(self, ctx, index: int, *, text: str):
        '''Add something to do'''
        if len(text) <= 200:
            async with self.config.member(ctx.author).todos() as member_todos:
                member_todos.insert(index, text)
            await ctx.send('New ToDo added!')
        else:
            await ctx.send('Max. 200 characters allowed!')

    @todo.command(pass_context=True)
    async def rm(self, ctx, index: int):
        '''Remove something you did already'''
        try:
            async with self.config.member(ctx.author).todos() as member_todos:
                member_todos.pop(index)
            await ctx.send('ToDo removed!')
        except IndexError:
            await ctx.send('The number was wrong...')
