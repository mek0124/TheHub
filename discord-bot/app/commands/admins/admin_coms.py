from disnake.ext import commands
from thefuzz import process
from app.services.json import JsonEngine
from app.services.message_log import delete_messages_log
from settings import (
    GUILD_ID,
    PURGE_THREAD_ID
)

import disnake
import asyncio


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="ping",
        description="Test the response time of the bot",
        guild_ids=[GUILD_ID]
    )
    @commands.has_any_role('Owner', 'Administrators')
    async def ping(self, inter):
        await inter.response.defer(ephemeral=True)
        bot_latency = self.bot.latency
        rounded_latency = round(bot_latency * 1000, 2)  # Convert to milliseconds
        return await inter.edit_original_message(f"Current Latency: {rounded_latency}ms")

    @commands.slash_command(
        name="purge",
        description="Remove n number of message(s) from the channel, or from a user in the channel.",
        guild_ids=[GUILD_ID]
    )
    @commands.has_any_role("Owner", "Administrators")
    async def purge(self, inter, member: str = None, amount: int = None, *, reason: str):
        await inter.response.defer()

        if amount:
            amount += 1

        try:
            if member:
                member_id = member.split(":")[1]
                member = inter.guild.get_member(int(member_id))

                if not member:
                    return await inter.edit_original_message("Member not found.")
                
                check = lambda message: message.author.id == member.id
                message_history = await inter.channel.purge(limit=amount, check=check)
            else:
                message_history = await inter.channel.purge(limit=amount)

            if not message_history:
                return await inter.edit_original_message("No messages were deleted.")

            _file = delete_messages_log(message_history, reason)

            json_dict = {
                "date": str(inter.created_at.date()),
                "time": str(inter.created_at.time()),
                "user_id": inter.author.id,
                "action": "purge",
                "reason": reason,
                "details": ', '.join([f"{msg.author.name}: {str(msg.created_at)}: {msg.content}" for msg in message_history])
            }

            self.bot.db_engine.save_log(json_dict)

            embed = disnake.Embed(
                color=disnake.Colour.random(),
                title=f"{self.bot.user.name}'s Purge Notification",
                description=f"{inter.author.name} Has Purged {len(message_history)} Messages From Channel {inter.channel.name}"
            ).add_field(
                name="Are Messages From Member?",
                value="yes" if member else "no",
                inline=False
            ).add_field(
                name="Reason",
                value=reason,
                inline=False
            ).set_thumbnail(url=inter.author.avatar)

            purge_thread = inter.guild.get_thread(PURGE_THREAD_ID)
            await purge_thread.send(embed=embed, file=_file)

            await asyncio.sleep(3)
            msg = await inter.channel.send(":mega:Purge Finished. Continue Messaging:mega:")
            await asyncio.sleep(3)
            await msg.delete()

        except Exception as e:
            await inter.edit_original_message(f"An error occurred: {e}")

    @purge.autocomplete("member")
    async def autocomplete(self, inter, member):
        members = [f"{member.name}:{member.id}" for member in inter.guild.members]
        values: list[str] = process.extract(member, members, limit=25)
        return [i[0] for i in values]


def setup(bot):
    bot.add_cog(AdminCommands(bot))
