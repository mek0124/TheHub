from disnake.ext import commands
from collections import deque
from settings import GUILD_ID, MUSIC_CHANNEL_ID
from thefuzz import process


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_que = deque()
        self.currently_playing = False

    @commands.slash_command(
        name = "music",
        description = "Allows a member to control the music portion of The Hub's bot",
        guild_ids = [GUILD_ID]
    )
    @commands.has_any_role('member')
    async def music(self, inter, action: str, url: str = None) -> None:
        await inter.response.defer(ephemeral=True)

        if action == "join":
            await self.were_joining(inter)
        elif action == "leave":
            await self.were_leaving(inter)
        elif action == "stop":
            await self.were_not_playing(inter)
        elif action == "play":
            await self.were_playing(inter, action, url)
        else:
            if action not in ["join", "leave", "play", "stop"]:
                return await inter.edit_original_message(
                    f"{inter.author.mention} That action is not usable with this command!"
                )
    
    async def were_joining(self, inter):
        if inter.author.voice:
            await inter.author.voice.channel.connect()
            return await inter.edit_original_message("Joined the voice channel!")
        else:
            return await inter.edit_original_message("You need to be in a voice channel for me to join!")
        
    async def were_leaving(self, inter):
        if inter.guild.voice_client:
            await inter.guild.voice_client.disconnect()
            self.song_que.clear()
            self.currently_playing = False
            return await inter.edit_original_message("Left the voice channel!")
        else:
            return await inter.edit_original_message("I'm not connected to any voice channel!")
        
    async def were_not_playing(self, inter):
        await self.bot.music_player.stop()
        self.song_que.clear()
        self.currently_playing = False
        return await inter.edit_original_message("Stopped the music!")

    async def were_playing(self, inter, action, url):
        if action == "play" and url == None:
            return await inter.edit_original_message(
                f"{inter.author.mention} You must provide a URL to play!"
            )
        else:
            mus_chn = inter.guild.get_channel(MUSIC_CHANNEL_ID)

            if not inter.channel.id == mus_chn.id:
                return await inter.edit_original_message(
                    f"{inter.author.mention} You must be in the {
                        mus_chn.mention} channel to use this command!"
                )

            self.song_que.append(url)

            await inter.channel.send(f"Added to que: {url}")

            if not self.currently_playing:
                await self._play_next_song(inter)

    async def _play_next_song(self, inter):
        if self.song_que:
            self.currently_playing = True

            next_song = self.song_que.popleft()

            await inter.followup.send(f"Now Playing: {next_song}")
            await self.bot.music_player.play_song(inter, next_song)
            await self.bot.music_player.wait_for_song_end()
            await self._play_next_song()

    @music.autocomplete('action')
    async def autocomplete(self, inter, action: str) -> str:
        actions = ["join", "leave", "play", "stop"]
        return [action for action in actions]


def setup(bot):
    bot.add_cog(MusicCommands(bot))
