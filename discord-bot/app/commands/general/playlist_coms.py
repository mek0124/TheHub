

class PlaylistCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "playlist",
        description = "Allows a member to create/edit/delete a playlist of youtube URLs",
        guild_ids = [GUILD_ID]
    )
    @commands.has_any_role('member')
    async def playlist(self, inter, playlist_name: str, action: str, url: str = None) -> None:
        await inter.response.defer(ephemeral=True)

        if action == "all":
            pass
        elif action == "create":
            pass
        elif action == "add":
            pass
        elif action == "edit":
            pass
        elif action == "remove":
            pass
        else:
            pass
    
    @playlist.autocomplete('playlist_name')
    async def autocomplete(self, inter, playlist_name):
        all_playlist_names = self.bot.db_engine.get_playlists(inter.author.id)
        all_names = [pl_name[0] for pl_name in all_playlist_names]
        values: list[str] = process.extract(playlist_name, all_names, limit=25)
        return [i[0] for i in values]
    
    @playlist.autocomplete('action')
    async def autocomplete2(self, inter, action):
        actions = ["all", "create", "add", "edit", "remove"]
        return [action for action in actions]