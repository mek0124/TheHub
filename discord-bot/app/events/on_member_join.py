"""
Updated on member join function to use the random library
to select a random greeting from the list of greetings
that the json engine retrieves, and adds it to the embed.

I'm not entirely sold on how it looks. lol

I also updated the settings.py file to use the "how-to" channel
id under the support category. I found a way to create a link for
the user to click it and it take them to the support category
through the welcome embed that is dm'd to them, however, it was
made using markdown []() and didn't look like the other mentions
so I created a text channel called how-to. Figured we could update
that whenever. But it matches the rest and is usable.
"""

from disnake.ext import commands

import random

from settings import (
    GUILD_ID, 
    MEMBER_ROLE_ID, 
    WELCOME_CHANNEL_ID,
    RULES_CHANNEL_ID,
    ANNOUNCEMENTS_CHANNEL_ID,
    INVITE_LINK_CHANNEL_ID,
    MEET_THE_TEAM_CHANNEL_ID,
    SUPPORT_CHANNEL_ID # renamed here and in settings.py
)

import disnake


class OnMemberJoinEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(GUILD_ID)
        member_role = guild.get_role(MEMBER_ROLE_ID)
        welcome_chan = guild.get_channel(WELCOME_CHANNEL_ID)
        ann_chan = guild.get_channel(ANNOUNCEMENTS_CHANNEL_ID)
        rules_chan = guild.get_channel(RULES_CHANNEL_ID)
        inv_link_chan = guild.get_channel(INVITE_LINK_CHANNEL_ID)
        team_chan = guild.get_channel(MEET_THE_TEAM_CHANNEL_ID)
        support_chan = guild.get_channel(SUPPORT_CHANNEL_ID)

        greeting = await self.get_greeting()

        welcome_embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = f"{guild.name} Welcomes You!",
            description = f"Welcome, {member.display_name}!"
        ).add_field(
            name = "\u200b",
            value = greeting,
            inline = False
        ).set_thumbnail(
            url = guild.icon
        )

        user_embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = f"Welcome, {member.display_name} to Mek's Hub!",
            description = "Welcome aboard friend! Below is some useful information for you to help with your starting journey!"
        ).add_field(
            name = "Important Channels",
            value = f"{ann_chan.mention}\n{rules_chan.mention}\n{inv_link_chan.mention}>\n{team_chan.mention}\n{welcome_chan.mention}\n{support_chan.mention}",
            inline = False
        ).set_thumbnail(
            url = guild.icon
        )

        await member.add_roles(member_role)
        await welcome_chan.send(embed=welcome_embed)
        
        try:
            return await member.send(embed=user_embed)
        except disnake.Forbidden:
            pass
        except Exception as e:
            raise e
        
    async def get_greeting(self):
        all_greetings = self.bot.json_engine.get_greetings()

        return random.choice(all_greetings)


def setup(bot):
    bot.add_cog(OnMemberJoinEvent(bot))