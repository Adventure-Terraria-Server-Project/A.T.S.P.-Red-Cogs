from .todo import ToDo


async def setup(bot):
    await bot.add_cog(ToDo())
