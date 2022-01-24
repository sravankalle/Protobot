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
            player = await channel.connect()
        
    
        async with ctx.typing():
            player.play(discord.FFmpegPCMAudio(source=song.url), after=lambda e: play_next(ctx))
        await ctx.send(embed=song.play_embed())
    else:
        print(bot.voice_clients)
        song = music.playSong(ctx, search)
        await ctx.send(embed=song.queue_embed())

def play_next(ctx):
    if len(music.queue[ctx.message.guild.id]) >= 1:
        del music.queue[ctx.message.guild.id][0]
        vc = get(bot.voice_clients, guild=ctx.guild) 
        if len(music.queue[ctx.message.guild.id]) == 0:
            print("done")
        else:    
            song = music.queue[ctx.message.guild.id][0]
            vc.stop()
            vc.play(discord.FFmpegPCMAudio(source=song.url), after=lambda e: play_next(ctx))
            asyncio.run_coroutine_threadsafe(ctx.send(embed=song.play_embed()), bot.loop)
    else:
        print("done")

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
bot.run(os.getenv("key"))
