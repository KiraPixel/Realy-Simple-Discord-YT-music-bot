import disnake
from disnake.ext import commands
from pytube import YouTube
import nacl

intents = disnake.Intents.default()
intents.voice_states = True
intents.message_content = True  # Добавьте эту строку

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')


@bot.slash_command(
    name='play',
    description='Play a YouTube video in your current voice channel'
)
async def play(ctx: disnake.ApplicationCommandInteraction, url: str):
    voice_channel = ctx.author.voice.channel if ctx.author.voice else None
    if not voice_channel:
        await ctx.send('You are not connected to a voice channel.')
        return
    try:
        video = YouTube(url)
        video_url = video.streams.filter(only_audio=True).first().url
    except Exception as e:
        print(e)
        await ctx.send('Invalid YouTube video URL.')
        return
    try:
        voice_client = await voice_channel.connect()
        voice_client.play(disnake.FFmpegPCMAudio(video_url), after=lambda e: print('done', e))
    except Exception as e:
        print(e)
        await ctx.send('Error 0x1515')
        return
    await ctx.send(f'Playing: {video.title}')


@play.error
async def play_error(ctx: disnake.ApplicationCommandInteraction, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('Please provide a YouTube video URL.')


bot.run('')
