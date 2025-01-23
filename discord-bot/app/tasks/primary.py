"""
File stayed the same
"""

from disnake.ext import commands
from disnake.ext import commands, tasks
from itertools import cycle

import disnake


class PrimaryTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.change_status.start()

    @tasks.loop(seconds=90)
    async def change_status(self):
        await self.bot.wait_until_ready()

        stats = cycle([
            "Using `/help_menu` for help",
            "Playing with the birds",
            "Watching the chat channels"
        ])

        await self.bot.change_presence(
            activity = disnake.CustomActivity(
                state = next(stats),
                name = "Custom Status"
            )
        )


def setup(bot):
    bot.add_cog(PrimaryTasks(bot))
    