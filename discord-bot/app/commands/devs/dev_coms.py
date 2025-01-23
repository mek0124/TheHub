from disnake.ext import commands
from app.services.json import JsonEngine
from app.services.paginator import Paginator
from settings import GUILD_ID

import disnake


class DeveloperCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "get_all_suggestions",
        description = "Retrieves all suggestions from the database",
        guild_ids = [GUILD_ID]
    )
    @commands.has_any_role('Owner', 'Developer')
    async def get_all_suggestions(self, inter):
        await inter.response.defer(ephemeral = True)

        all_suggestions = self.bot.db_engine.get_all_suggestions()

        if len(all_suggestions) == 0:
            return await inter.edit_original_message(
                f"{inter.author.mention} There are no suggestions to show. Try Again Later!"
            )

        open_suggestions = []
        closed_suggestions = []

        primary_embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = f"{inter.guild.name}'s Suggestions",
            description = "In the following pages are the details about all suggestions"
        )

        for suggestion in all_suggestions:
            stat = suggestion[-1]
            
            if stat == "open":
                open_suggestions.append(suggestion)
            else:
                closed_suggestions.append(suggestion)

        all_embeds = []

        for suggestion in open_suggestions:
            _id, date, time, user_id, join_date, sugg, stat = suggestion

            embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = f"Suggestion ID: {_id}",
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

        for suggestion in closed_suggestions:
            _id, date, time, user_id, join_date, sugg, stat = suggestion

            embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = f"Suggestion ID: {_id}",
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

        primary_embed.add_field(
            name = "Total Open Suggestions",
            value = len(open_suggestions),
            inline = False
        ).add_field(
            name = "Total Closed Suggestions",
            value = len(closed_suggestions),
            inline = False
        )

        all_embeds.insert(0, primary_embed)

        return await inter.edit_original_message(
            embed = all_embeds[0],
            view = Paginator(all_embeds)
        )
    
    @commands.slash_command(
        name = "get_open_suggestions",
        description = "Allows the developers to get all open suggestions.",
        guild_ids = [GUILD_ID]
    )
    @commands.has_any_role('Owner', 'Developer')
    async def get_open_suggestions(self, inter):
        await inter.response.defer(ephemeral = True)

        all_suggestions = self.bot.db_engine.get_open_suggestions()

        if len(all_suggestions) == 0:
            return await inter.edit_original_message(
                f"{inter.author.mention} There are currently no open suggestions. Try Again Later!"
            )

        all_embeds = []

        for suggestion in all_suggestions:
            _id, date, time, user_id, join_date, sugg, stat = suggestion

            embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = f"Suggestion ID: {_id}",
                description = sugg
            ).add_field(
                name = "Sender",
                value = f"ID: {user_id}\nJoin Date: {join_date}",
                inline = False
            ).add_field(
                name = "Date & Time",
                value = f"Date: {date}\nTime: {time}"
            ).add_field(
                name = "Status",
                value = stat,
                inline = False
            )

            all_embeds.append(embed)

        primary_embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = f"{inter.guild.name}'s Open Suggestions",
            description = "In the following pages are the details about all open suggestions"
        ).add_field(
            name = "Total Open Suggestions",
            value = len(all_suggestions),
            inline = False
        ).set_thumbnail(url = inter.guild.icon)

        all_embeds.insert(0, primary_embed)

        return await inter.edit_original_message(
            embed = all_embeds[0],
            view = Paginator(all_embeds)
        )
    
    @commands.slash_command(
        name = "get_closed_suggestions",
        description = "Allows the developers to get all closed suggestions.",
        guild_ids = [GUILD_ID]
    )
    @commands.has_any_role('Owner', 'Developer')
    async def get_closed_suggestions(self, inter):
        await inter.response.defer(ephemeral = True)

        all_suggestions = self.bot.db_engine.get_closed_suggestions()

        if len(all_suggestions) == 0:
            return await inter.edit_original_message(
                f"{inter.author.mention} There are currently no closed suggestions. Try Again Later!"
            )

        all_embeds = []

        for suggestion in all_suggestions:
            _id, date, time, user_id, join_date, sugg, stat = suggestion

            embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = f"Suggestion ID: {_id}",
                description = sugg
            ).add_field(
                name = "Sender",
                value = f"ID: {user_id}\nJoin Date: {join_date}",
                inline = False
            ).add_field(
                name = "Date & Time",
                value = f"Date: {date}\nTime: {time}"
            ).add_field(
                name = "Status",
                value = stat,
                inline = False
            )

            all_embeds.append(embed)

        primary_embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = f"{inter.guild.name}'s Open Suggestions",
            description = "In the following pages are the details about all closed suggestions"
        ).add_field(
            name = "Total Closed Suggestions",
            value = len(all_suggestions),
            inline = False
        ).set_thumbnail(url = inter.guild.icon)

        all_embeds.insert(0, primary_embed)

        return await inter.edit_original_message(
            embed = all_embeds[0],
            view = Paginator(all_embeds)
        )
    
    @commands.slash_command(
        name = "close_suggestion",
        description = "Allows a developer to close a suggestion",
        guild_ids = [GUILD_ID]
    )
    @commands.has_any_role('Owner', 'Developer')
    async def close_suggestion(self, inter, _id: str):
        await inter.response.defer(ephemeral=True)

        does_exist = self.bot.db_engine.search_suggestion(_id)

        if not does_exist:
            return await inter.edit_original_message(
                f"{inter.author.mention} That ID does not exist. Try Again!"
            )
        
        did_close = self.bot.db_engine.close_suggestion(_id)

        if not did_close:
            return await inter.edit_original_message(
                f"{inter.author.mention} There was a problem closing that suggestion. Try Again Later!"
            )
        
        embed = disnake.Embed(
            color = disnake.Colour.green(),
            title = f"{inter.guild.name}'s Suggestion Editor",
            description = f"You successfully closed suggestion: {_id}"
        ).set_thumbnail(url = inter.guild.icon)

        return await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(DeveloperCommands(bot))