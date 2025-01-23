from disnake.ext import commands
from disnake import File
from settings import GUILD_ID, ANNOUNCEMENTS_CHANNEL_ID

import disnake
import json
import sys
import os
import io


class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="restart",
        description="Allows the Owners to restart the bot if necessary",
        guild_ids=[GUILD_ID]
    )
    @commands.has_any_role('Owner')
    async def restart(self, inter, reason: str = "Development"):
        await inter.response.defer()

        guild = inter.guild

        announce_chan = guild.get_channel(ANNOUNCEMENTS_CHANNEL_ID)

        embed = disnake.Embed(
            color=disnake.Colour.red(),
            title=f"{self.bot.user.name} Is Restarting... Please Wait...",
            description="Bot Rebooting"
        ).add_field(
            name="Reason",
            value=reason,
            inline=False
        ).set_thumbnail(
            url=inter.guild.icon
        )

        log_dict = {
            "date": str(inter.created_at.date()),
            "time": str(inter.created_at.time()),
            "user_id": inter.author.id,
            "action": "bot restart",
            "reason": reason,
            "details": "None"
        }

        self.bot.db_engine.save_log(log_dict)

        await announce_chan.send(embed=embed)

        await inter.edit_original_message(f"{self.bot.user.name} Is Restarting... Please Wait...")
        return self.restart_bot()

    def restart_bot(self):
        return os.execv(sys.executable, ['python'] + sys.argv)

    @commands.slash_command(
        name = "restrict_words",
        description = "Add/Remove words to/from the database",
        guild_ids = [GUILD_ID]
    )
    @commands.has_any_role('Owner')
    async def restrict_words(self, inter, action: str, word: str, *, reason: str) -> None:
        await inter.response.defer(ephemeral=True)

        does_word_exist = self.bot.db_engine.search_word(word)

        if action == "add" and does_word_exist:
            return await inter.edit_original_message(
                f"{inter.author.mention} That word already exist. Try again"
            )
        
        if action == "remove" and not does_word_exist:
            return await inter.edit_original_message(
                f"{inter.author.mention} That word does not exist. Try Again"
            )

        if action == "add":
            self.bot.db_engine.save_word(word)
        elif action == "remove":
            self.bot.db_engine.remove_word(word)

        to_from = "to" if action == "add" else "from"

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = f"{inter.guild.name}'s Restricted Word Editor",
            description = f"{inter.author.display_name}, you have successfully {action} {word} {to_from} the database"
        ).add_field(
            name = "Reason",
            value = reason,
            inline = False
        ).set_thumbnail(url = inter.guild.icon)
        
        all_words = self.bot.db_engine.get_all_words()

        embed.add_field(
            name = "Total Restricted Words",
            value = len(all_words),
            inline = False
        )

        file_data = io.StringIO()
        json.dump(all_words, file_data, indent=4)
        file_data.seek(0)

        file = File(file_data, filename="restricted_words.json")

        return await inter.edit_original_message(
            embed=embed, 
            file=file
        )

    @restrict_words.autocomplete("action")
    async def autocomplete(self, inter, action):
        actions = ["add", "remove"]
        return [action for action in actions]

def setup(bot):
    bot.add_cog(OwnerCommands(bot))
