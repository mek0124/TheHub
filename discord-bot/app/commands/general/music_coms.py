from disnake.ext import commands
from collections import deque
from settings import GUILD_ID, MUSIC_CHANNEL_ID


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_que = deque()
        self.currently_playing = False

    @commands.slash_command(
        name="join",
        description="Join a voice channel.",
        guild_ids=[GUILD_ID]
    )
    @commands.has_any_role('member')
    async def join(self, inter):
        if inter.author.voice:
            await inter.author.voice.channel.connect()
            return await inter.response.send_message("Joined the voice channel!")
        else:
            return await inter.response.send_message("You need to be in a voice channel for me to join!")

    @commands.slash_command(
        name="leave",
        description="Leave the voice channel.",
        guild_ids=[GUILD_ID]
    )
    @commands.has_any_role('member')
    async def leave(self, inter):
        if inter.guild.voice_client:
            await inter.guild.voice_client.disconnect()
            self.song_que.clear()
            self.currently_playing = False
            return await inter.response.send_message("Left the voice channel!")
        else:
            return await inter.response.send_message("I'm not connected to any voice channel!")

    @commands.slash_command(
        name="play",
        description="Play a song from a YouTube URL.",
        guild_ids=[GUILD_ID]
    )
    @commands.has_any_role('member')
    async def play(self, inter, url: str):
        await inter.response.defer()

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

    @commands.slash_command(
        name="stop",
        description="Stop playing music.",
        guild_ids=[GUILD_ID]
    )
    @commands.has_any_role('member')
    async def stop(self, inter):
        await self.music_player.stop()
        self.song_que.clear()
        self.currently_playing = False
        return await inter.response.send_message("Stopped the music!")


def setup(bot):
    bot.add_cog(MusicCommands(bot))
