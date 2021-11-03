from .voteutils import VoteUtils


def setup(bot):
    bot.add_cog(VoteUtils(bot))
