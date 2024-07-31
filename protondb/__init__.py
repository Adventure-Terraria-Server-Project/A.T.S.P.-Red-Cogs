from .protondb import ProtonDB


async def setup(bot):
    await bot.add_cog(ProtonDB())
