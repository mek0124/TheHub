from disnake.ext import commands
from settings import GUILD_ID
from app.services.paginator import Paginator

import disnake


class SuggestionCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name = "suggest",
        description = "Create/Get/Close Suggestions",
        guild_ids = [GUILD_ID]
    )
    @commands.has_any_role('member')
    async def suggest(self, inter, choice: str, details: str = None):
        await inter.response.defer(ephemeral = True)

        if inter.author.top_role.name not in ['Owner', 'Developer'] and choice == "create":
            if not details:
                return await inter.edit_original_message(
                    f"{inter.author.mention} You must include details in your suggestion."
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
        
        elif inter.author.top_role.name not in ['Owner', 'Developer'] and choice in ["all", "open", "closed"]:
            return await inter.edit_original_message(
                f"{inter.author.mention} You must be an Owner or Developer to use that command!"
            )
        else:
            if choice == "all":
                all_suggestions = self.bot.db_engine.get_all_suggestions()
            elif choice == "open":
                all_suggestions = self.bot.db_engine.get_open_suggestions()
            elif choice == "closed":
                all_suggestions = self.bot.db_engine.get_closed_suggestions()

            if len(all_suggestions) == 0:
                return await inter.edit_original_message(
                    f"{inter.author.mention} There are no suggestions to show. Try Again Later!"
                )

            all_embeds = []
            open_suggestions = []
            closed_suggestions = []

            for suggestion in all_suggestions:
                stat = suggestion[-1]
                
                if stat == "open":
                    open_suggestions.append(suggestion)
                else:
                    closed_suggestions.append(suggestion)
        
            if choice == "all":
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
            elif choice == "open":
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
            elif choice == "close":
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

            primary_embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = f"{inter.guild.name}'s Suggestions",
                description = "In the following pages are the details about all suggestions"
            ).add_field(
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

    @suggest.autocomplete('choice')
    async def autocomplete(self, inter, choice):
        choices = ["all", "open", "closed", "create"]
        choices.sort()
        return [choice for choice in choices]


def setup(bot):
    bot.add_cog(SuggestionCommand(bot))