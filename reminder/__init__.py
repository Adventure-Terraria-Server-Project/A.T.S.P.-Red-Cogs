from .reminder import Reminder


def setup(bot):
    rmd = Reminder(bot)
    bot.add_cog(rmd)
