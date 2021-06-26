import discord
from redbot.core import commands
from redbot.core import checks


class NitroBoost(commands.Cog):
    '''Check for boost changes'''

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.premium_since is None and after.premium_since is not None:
            await self.bot.send_to_owners(f'{after.mention} just boosted')
        elif before.premium_since is not None and after.premium_since is None:
            await self.bot.send_to_owners(f'{after.mention} just removed boost')

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def booster(self, ctx):
        '''List all Nitro Booster'''
        boosters_list = ctx.message.guild.premium_subscribers
        boosts_count = ctx.message.guild.premium_subscription_count
        boost_level = ctx.message.guild.premium_tier
        boosters = ''
        boosters_count = len(boosters_list)
        for booster in boosters_list:
            boosters += f'{booster.premium_since.strftime("%y.%m.%d %H:%M")} - {booster.mention}\n'

        embed = discord.Embed(description=boosters)
        embed.title = f'{boosters_count} Current Nitro Boosters'
        embed.colour = discord.Colour.magenta()
        embed.set_footer(text=f'Level {boost_level} with {boosts_count} boosts',
                         icon_url='https://cdn.discordapp.com/attachments/264532095609602049/848216937950478356/Nitro.png')
        await ctx.send(embed=embed)
