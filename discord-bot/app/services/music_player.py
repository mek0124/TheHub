import yt_dlp
import disnake

class MusicPlayer:
    def __init__(self):
        self.voice_client = None
        self.ytdl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
            ],
            "quiet": True,
        }
        self.ytdl = yt_dlp.YoutubeDL(self.ytdl_opts)

    async def play_song(self, ctx, url):
        if not self.voice_client:
            if ctx.author.voice:
                self.voice_client = await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You need to be in a voice channel!")
                return

        data = self.ytdl.extract_info(url, download=False)
        song_url = data["url"]

        if self.voice_client.is_playing():
            self.voice_client.stop()

        self.voice_client.play(disnake.FFmpegPCMAudio(song_url))

        # Create an embed with song details
        embed = disnake.Embed(
            title="🎵 Now Playing",
            color=disnake.Color.green(),
        )
        embed.add_field(name="Title", value=f"[{data['title']}]({data['webpage_url']})", inline=False)
        embed.add_field(name="Uploader", value=data.get("uploader", "Unknown"), inline=True)
        embed.add_field(name="Duration", value=self._format_duration(data["duration"]), inline=True)
        embed.add_field(name="URL", value=f"[Click Here]({data['webpage_url']})", inline=False)
        embed.set_thumbnail(url=data.get("thumbnail", ""))
        embed.set_footer(text="Requested by " + ctx.author.display_name, icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)

    async def stop(self):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()

    def _format_duration(self, seconds):
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        if hours > 0:
            return f"{hours}:{mins:02}:{secs:02}"
        return f"{mins}:{secs:02}"
