from .messages import Messages


def setup(bot):
    msgs = Messages(bot)
    bot.add_cog(msgs)
