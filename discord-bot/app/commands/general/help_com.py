from disnake.ext import commands
from app.services.paginator import Paginator
from settings import GUILD_ID

import disnake


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "help",
        description = "Returns a paginator embed of the commands available to your highest ranking role",
        guild_ids = [GUILD_ID]
    )
    @commands.has_any_role('member')
    async def help(self, inter):
        await inter.response.defer(ephemeral=True)

        gen_dict, mod_dict, admin_dict, dev_dict, owner_dict = self.bot.json_engine.get_all_commands()

        user_highest_role = inter.author.top_role.name

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = f"{inter.guild.name}'s Help Menu",
            description = "In the pages to follow are the commands available to your highest ranking role."
        ).set_thumbnail(url = inter.guild.icon)

        if user_highest_role == "Owner":
            command_list = [gen_dict, mod_dict, admin_dict, dev_dict, owner_dict]
        elif user_highest_role == "Developer":
            command_list = [gen_dict, mod_dict, admin_dict, dev_dict]
        elif user_highest_role == "Administrators":
            command_list = [gen_dict, mod_dict, admin_dict]
        elif user_highest_role == "Moderators":
            command_list = [gen_dict, mod_dict]
        elif user_highest_role == "member":
            command_list = [gen_dict]

        all_embeds = await self.build_embeds(inter, command_list)
        all_embeds.insert(0, embed)

        return await inter.edit_original_message(
            embed = all_embeds[0],
            view = Paginator(all_embeds)
        )
        
    async def build_embeds(self, inter, commands):
        all_embeds = []

        for command_list in commands:
            for command in command_list:
                name = command.replace("_", " ").title() or command.capitolize()
                description = command_list[command]["description"]
                usage = command_list[command]["usage"]

                embed = disnake.Embed(
                    color = disnake.Colour.random(),
                    title = name,
                    description = description
                ).add_field(
                    name = "How To Use",
                    value = usage,
                    inline = False
                ).set_thumbnail(
                    url = inter.guild.icon
                )

                all_embeds.append(embed)

        return all_embeds

def setup(bot):
    bot.add_cog(HelpCommand(bot))