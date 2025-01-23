from disnake.ext import commands
from disnake.ext.commands import Param
from disnake import File
from thefuzz import process
from settings import (
    GUILD_ID,
    AUTHOR,
    REPO_LINK,
    WELCOME_CHANNEL_ID
)

import disnake
import json 
import io


class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="hub",
        description="Returns all Mek's Hub public information",
        guild_ids=[GUILD_ID]
    )
    @commands.has_any_role('member')
    async def hub(self, inter):
        await inter.response.defer(ephemeral=True)

        author = AUTHOR
        repo_link = REPO_LINK

        embed = disnake.Embed(
            color=disnake.Color.random(),
            title=f"{inter.guild.name} Information",
            description="Below you can find all the publicly available information for the hub",
        ).add_field(
            name="Hub Author",
            value=author
        ).add_field(
            name="Public Repo",
            value=f"[click here]({repo_link})"
        ).set_thumbnail(
            url=self.bot.user.avatar
        )

        return await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="welcome",
        description="Welcome a new user to the discord!",
        guild_ids=[GUILD_ID]
    )
    @commands.has_any_role('member')
    async def welcome(self, inter, member: str, *, details: str = Param(max_length=256)):
        await inter.response.defer(ephemeral=True)

        member_id = member.split(":")[1]
        member = inter.guild.get_member(int(member_id))

        welcome_chan = inter.guild.get_channel(WELCOME_CHANNEL_ID)

        embed = disnake.Embed(
            color=disnake.Colour.random(),
            title=f"Hello {member.display_name}!",
            description=details
        ).set_image(
            url=member.avatar
        ).set_thumbnail(
            url=inter.author.avatar
        )

        await welcome_chan.send(embed=embed)

        return await inter.edit_original_message("Your welcome message has been sent!", embed=embed)
    
    @commands.slash_command(
        name = "restricted_words",
        description = "Returns the complete list of Restricted Words in the database",
        guild_ids = [GUILD_ID]
    )
    @commands.has_any_role('member')
    async def restricted_words(self, inter):
        await inter.response.defer(ephemeral=True)

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = f"{inter.guild.name}'s Restricted Words List",
            description = "See the file below for the complete list of Restricted Words"
        ).set_thumbnail(
            url = inter.guild.icon
        )

        all_words = self.bot.db_engine.get_all_words()

        file_data = io.StringIO()
        json.dump(all_words, file_data, indent=4)
        file_data.seek(0)

        file = File(file_data, filename="restricted_words.json")

        return await inter.edit_original_message(
            embed = embed,
            file = file
        )

    @welcome.autocomplete("member")
    async def autocomplete(self, inter, member):
        members = [f"{member.name}:{member.id}" for member in inter.guild.members]
        values: list[str] = process.extract(member, members, limit=25)
        return [i[0] for i in values]


def setup(bot):
    bot.add_cog(GeneralCommands(bot))
