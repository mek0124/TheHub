from disnake.ext import commands
from disnake.ext.commands import Param
from settings import GUILD_ID

import disnake


class SuggestionCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "suggest",
        description = "Send a suggestion to the developers! MAX 1024 CHARACTERS",
        guild_ids = [GUILD_ID]
    )
    @commands.has_any_role('member')
    async def suggest(self, inter, *, details: str = Param(max_length=1024)):
        """
        This command needs to be updated to be placed on a 24 hour cooldown after the member executes it
        """
        await inter.response.defer(ephemeral=True)

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = f"Incoming Suggestion My Dudes!!!",
            description = "We have an inter-galactic transmission coming aboard bitches :D"
        ).add_field(
            name = "Author",
            value = inter.author.display_name,
        ).add_field(
            name = "ID",
            value = inter.author.id
        ).add_field(
            name = "Join Date",
            value = inter.author.joined_at
        ).add_field(
            name = "Suggestion",
            value = details,
            inline = False
        ).set_thumbnail(
            url = inter.author.avatar
        )

        json_dict = {
            "date": str(inter.created_at.date()),
            "time": str(inter.created_at.time()),
            "user_id": inter.author.id,
            "join_date": str(inter.author.joined_at),
            "details": details,
            "status": "open"
        }

        self.bot.db_engine.save_suggestion(json_dict)
        return await inter.edit_original_message(f"{inter.author.mention}, Your suggestion has been submitted!")


def setup(bot):
    bot.add_cog(SuggestionCommand(bot))