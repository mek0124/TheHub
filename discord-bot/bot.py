"""
File stayed the same
"""

from disnake.ext import commands
from app.services.json import JsonEngine
from app.services.db import DbEngine
from settings import DISCORD_BOT_TOKEN, GUILD_ID, TERMINAL_CHANNEL_ID, ANNOUNCEMENTS_CHANNEL_ID

import disnake
import os
import importlib
import inspect

class MyBot(commands.InteractionBot):
    def __init__(self, json_engine: JsonEngine, db_engine: DbEngine, guild_id: int, term_id: int, ann_id: int, *args, **kwargs):
        super().__init__(**kwargs)

        self.json_engine = json_engine
        self.db_engine = db_engine
        self.guild_id = guild_id
        self.term_id = term_id
        self.ann_id = ann_id

        self.notifications = []


    def load_cogs(self):
        paths = ["./app/commands", "./app/events", "./app/tasks"]

        for path in paths:
            for root, dir, modules in os.walk(path):
                for module in modules:
                    if not module.endswith('.py'):
                        continue

                    module_path = os.path.join(root, module)
                    module_path = (
                        module_path.replace(".py", "")
                                .replace(".", "")
                                .replace("/", ".")
                                .replace("\\", ".")
                    )[1:len(module_path)]

                    try:
                        imported_module = importlib.import_module(module_path)
                        class_names = [
                            cls[0] for cls in inspect.getmembers(imported_module, inspect.isclass)
                            if cls[1].__module__ == module_path
                        ]

                        bot.load_extension(module_path)

                        if class_names:
                            for class_name in class_names:
                                self.notifications.append(f"Loaded: {class_name}")
                        else:
                            self.notifications.append(f"Loaded: {module_path} (No class found)")

                    except Exception as e:
                        raise e
                    
    async def on_slash_command_error(self, inter, error):
        if isinstance(error, commands.MissingAnyRole):
            return await inter.response.send_message(
                f"{inter.author.mention} You are missing the required role(s) to execute this command!"
            )
        elif isinstance(error, commands.MissingPermissions):
            return await inter.response.send_message(
                f"{inter.author.mention} You are missing the required permission(s) to execute this command."
            )
        else:
            try:
                return await inter.response.send_message(
                    f"An unexpected error occured: {error}"
                )
            except Exception:
                return await inter.edit_original_message(
                    f"An unexpected error occured: {error}"
                )

    async def on_ready(self):
        guild = bot.get_guild(self.guild_id)
        terminal = guild.get_channel(self.term_id)
        ann_channel = guild.get_channel(self.ann_id)

        embed = disnake.Embed(
            color=disnake.Colour.green(),
            title=f"{bot.user.name} Is Online!",
            description="We're up and runnin' cap'n!"
        ).add_field(
            name = "Console Output",
            value = '\n'.join(self.notifications)
        ).set_thumbnail(
            url=bot.user.avatar
        )

        embed2 = disnake.Embed(
            color = disnake.Colour.green(),
            title = f"{bot.user.name} Is Online!",
            description = "We're up and runnin' cap'n!"
        ).set_thumbnail(url = guild.icon)

        print("~" * 30)
        print(f"{bot.user.name} Is Online!")
        print("~" * 30)

        await terminal.send(embed=embed)
        # await ann_channel.send(embed=embed2)

if __name__ == '__main__':
    json_engine = JsonEngine()
    db_engine = DbEngine()

    intents = disnake.Intents.all()

    bot = MyBot(
        json_engine=json_engine, 
        db_engine=db_engine, 
        guild_id=GUILD_ID, 
        term_id=TERMINAL_CHANNEL_ID, 
        ann_id=ANNOUNCEMENTS_CHANNEL_ID,
        intents=intents
    )
    
    bot.load_cogs()

    bot.run(DISCORD_BOT_TOKEN)
