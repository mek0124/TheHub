from disnake.ext import commands
from disnake.ui import View, Button

import disnake


class Paginator(View):
    def __init__(self, embeds: list[disnake.Embed]):
        super().__init__(timeout=None)

        self.embeds = embeds
        self.current_page = 0

        self.first_button = Button(label="<<", style=disnake.ButtonStyle.primary)
        self.prev_button = Button(label="<", style=disnake.ButtonStyle.primary)
        self.next_button = Button(label=">", style=disnake.ButtonStyle.primary)
        self.last_button = Button(label=">>", style=disnake.ButtonStyle.primary)

        self.first_button.callback = self.go_to_first
        self.prev_button.callback = self.go_to_prev
        self.next_button.callback = self.go_to_next
        self.last_button.callback = self.go_to_last

        self.add_item(self.first_button)
        self.add_item(self.prev_button)
        self.add_item(self.next_button)
        self.add_item(self.last_button)

    async def update_message(self, interaction: disnake.MessageInteraction):
        await interaction.response.edit_message(
            embed = self.embeds[self.current_page], view=self
        )

    async def go_to_first(self, interaction: disnake.MessageInteraction):
        self.current_page = 0
        await self.update_message(interaction)

    async def go_to_prev(self, interaction: disnake.MessageInteraction):
        if self.current_page > 0:
            self.current_page -= 1
        
        await self.update_message(interaction)

    async def go_to_next(self, interaction: disnake.MessageInteraction):
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
        
        await self.update_message(interaction)

    async def go_to_last(self, interaction: disnake.MessageInteraction):
        self.current_page = len(self.embeds) - 1
        await self.update_message(interaction)
