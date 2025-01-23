from disnake.ext import commands
from app.services.json import JsonEngine
from app.services.paginator import Paginator
from settings import GUILD_ID

import disnake


class DeveloperCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "get_suggestions",
        description = "Retrieves all suggestions from the database",
        guild_ids = [GUILD_ID]
    )
    @commands.has_any_role('Owner', 'Developer')
    async def get_suggestions(self, inter):
        await inter.response.defer()

        all_suggestions = self.bot.db_engine.get_all_suggestions()
        open_suggestions = []
        closed_suggestions = []

        primary_embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = f"{inter.guild.name}'s Suggestions",
            description = "In the following pages are the details about the open suggestions"
        )

        all_embeds = [primary_embed]

        for suggestion in all_suggestions:
            id, date, time, user_id, join_date, sugg, stat = suggestion

            if stat == "closed":
                continue

            embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = f"Suggestion ID: {id}",
                description = sugg
            ).add_field(
                name = "Sender Info",
                value = f"Date: {date}\nTime: {time}\nID: {user_id}\nJoin Date: {join_date}",
                inline = False
            ).add_field(
                name = "Status",
                value = stat,
                inline = False
            )

            all_embeds.append(embed)

            if stat == "open":
                open_suggestions.append(suggestion)
            else:
                closed_suggestions.append(suggestion)

        primary_embed.add_field(
            name = "Total Open Suggestions",
            value = len(open_suggestions),
            inline = False
        ).add_field(
            name = "Total Closed Suggestions",
            value = len(closed_suggestions),
            inline = False
        )

        return await inter.edit_original_message(
            embed = all_embeds[0],
            view = Paginator(all_embeds)
        )


def setup(bot):
    bot.add_cog(DeveloperCommands(bot))