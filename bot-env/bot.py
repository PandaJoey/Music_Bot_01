from calendar import c
from http import client
from discord.ext import commands
import discord
import logging
import asyncio
import discord
import youtube_dl
from youtube_dl import YoutubeDL
import yt_dlp
import os



bot = commands.Bot(command_prefix='$')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open("secrets.txt") as file:
    bot_token = file.read()


# bot commands
@bot.command()
async def test(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def play(ctx, *, url):
    channel = ctx.author.voice.channel
    await channel.connect()
    bot_voice = discord.VoiceClient(bot, channel)
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # ipv6 addresses cause issues sometimes
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }]
    }
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    song_queue = []

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        I_URL = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(I_URL, **FFMPEG_OPTIONS)
        voice.play(source)
        voice.is_playing()
    
    """
    if bot is inactive for x amount of time:
        disconnect from the authers channel

    print("before first while")
    while bot_voice.is_playing():  # Checks if voice is playing
        print("inside first while")
        await asyncio.sleep(1)  # While it's playing it sleeps for 1 second
    else:
        await asyncio.sleep(15)  # If it's not playing it waits 15 seconds
        print("before second while")
        while bot_voice.is_playing():  # and checks once again if the bot is not playing
            print("inside second while")
            break  # if it's playing it breaks
        else:
            print("should be disconnecting if got here")
            await bot_voice.voice_disconnect()  # if not it disconnects
    await ctx.send("This is the play fucntion")
    """
# need a way to take the users url and parse it in here


@bot.command()
async def stop(ctx):
    await ctx.send("This is the stop function")
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()


@bot.command()
async def pause(ctx):
    await ctx.send("This is the pause fucntion")
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.command()
async def skip(ctx):
    await ctx.send("This is the skip fucntion")


@bot.command()
async def random(ctx):
    await ctx.send("This is the random fucntion")


@bot.command()
async def disconnect(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
bot.run(bot_token)
