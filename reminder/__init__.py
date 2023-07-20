from .reminder import Reminder


async def setup(bot):
    rmd = Reminder(bot)
    await bot.add_cog(rmd)
