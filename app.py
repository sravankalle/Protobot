from quart import Quart
import asyncio
from asyncio.tasks import run_coroutine_threadsafe, sleep
import discord
import os
from discord import colour
from discord.colour import Colour
from discord.ext import commands
from discord.utils import get
from sqlalchemy.engine import url
from Music import Music
from tables import User
from work import Work

bot = commands.Bot(command_prefix="$")

app = Quart(__name__)

@app.route('/')
def index():
    return "<h1>Protobot is up and running!</h1>"

@bot.event
async def on_ready():
    print("Ready!")

@bot.command()
async def ping(ctx):
    User.createUser(ctx.author.id, ctx.author.name, 100)
    print(f"{ctx.author.id} just used ping!")
    await ctx.send("pong!")

@bot.command(description="Get your balance")
async def balance(ctx):
    balance = User.getUserBalance(ctx.author.id)
    embed = discord.Embed(colour=Colour.dark_orange())
    embed.title = "Balance"
    embed.description = f"**{ctx.author.name}**'s Balance: {balance[0]} :coin:"
    embed.set_thumbnail(url=ctx.author.avatar_url)

    await ctx.send(embed=embed)
    balance = User.getUserBalance(ctx.author.id)

@bot.command()
async def work(ctx):
    
    work_data = Work.getWorkStatement()
    User.updateUserBalance(ctx.author.id, work_data[1])
    await ctx.reply(work_data[0])

music = Music()

@bot.command()
async def play(ctx, *search):

    guild_id = ctx.message.guild.id

    if guild_id not in music.queue or (len(music.queue[guild_id]) == 0):
        song = music.playSong(ctx, search)

        if ctx.author.voice:
            print("voice detected")
        
        if ctx.author.voice.channel:
            print("channel detected")

        vc = get(bot.voice_clients, guild=ctx.guild)
        
        player = None
        channel = ctx.author.voice.channel

        if not vc:
            print("no player")
            player = await channel.connect()
        else:
            async with ctx.typing():
              player.play(discord.FFmpegPCMAudio(source=song.url), after=lambda e: play_next(ctx))
            return await ctx.send(embed=song.play_embed())    
    
        async with ctx.typing():
            player.play(discord.FFmpegPCMAudio(source=song.url), after=lambda e: play_next(ctx))
        await ctx.send(embed=song.play_embed())
    else:
        print(bot.voice_clients)
        song = music.playSong(ctx, search)
        await ctx.send(embed=song.queue_embed())

def play_next(ctx):
    if len(music.queue[ctx.message.guild.id]) >= 1:
        vc = get(bot.voice_clients, guild=ctx.guild)     
        song = music.queue[ctx.message.guild.id][0]
        vc.play(discord.FFmpegPCMAudio(source=song.url), after=lambda e: play_next(ctx))
        asyncio.run_coroutine_threadsafe(ctx.send(embed=song.play_embed()), bot.loop)
        music.queue[ctx.message.guild.id].pop()
    else:
        vc = get(bot.voice_clients, guild=ctx.guild)
        asyncio.run_coroutine_threadsafe(vc.disconnect(), bot.loop)
        print("done in else")

@bot.command()
async def skip(ctx):
    vc = get(bot.voice_clients, guild=ctx.guild)
    vc.stop()

@bot.command()
async def pause(ctx):
    vc = get(bot.voice_clients, guild=ctx.guild)
    vc.pause()
    await ctx.send("Paused")

@bot.command()
async def resume(ctx):
    vc = get(bot.voice_clients, guild=ctx.guild)
    vc.resume()
    await ctx.send("Resumed")
@bot.command()
async def queue(ctx):
    guild_id = ctx.message.guild.id
    if guild_id in music.queue:
        message = "```\n"
        for i ,song in enumerate(music.queue[guild_id]):
            message+=f"{i+1}. {song.title}\n"
        message+="```"
        await ctx.send(message)
    else:
        await ctx.send("Queue is empty")

@bot.command()
async def leave(ctx):
    guild_id = ctx.message.guild.id
    if guild_id in music.queue:
        music.queue[guild_id] = []
        vc = get(bot.voice_clients, guild=ctx.guild)
        await vc.disconnect()
        await ctx.send("Bye!") 
    else:
        await ctx.send("I'm not in a voice channel")

bot.loop.create_task(app.run_task(host="0.0.0.0", port=8080))
bot.run(os.getenv("key"))
