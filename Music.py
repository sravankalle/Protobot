import json
from discord import colour, guild
from discord.utils import get
from youtube_dl.YoutubeDL import YoutubeDL
import discord
import asyncio

class Song():
    def __init__(self, title, url, thumbnail) -> None:
        self.title = title
        self.url = url
        self.thumbnail = thumbnail
    def play_embed(self):
        embed = discord.Embed(colour=colour.Color.dark_orange())
        embed.set_image(url=self.thumbnail)
        embed.title = "Now playing"
        embed.description = self.title
        return embed
    def queue_embed(self):
        embed = discord.Embed(colour=colour.Color.dark_orange())
        embed.set_image(url=self.thumbnail)
        embed.title = "Added to queue"
        embed.description = self.title
        return embed


class Music():
    def __init__(self):
        self.queue = {}
        self.servers = {}

    
    def searchSong(self, search):

        query = search

        ydl = YoutubeDL({})
        
        ydl.cache.remove()

        video = ydl.extract_info(f"ytsearch:{query}", download=False)
        
        return video["entries"][0]
        

    def playSong(self, ctx, search):
        concat_query = " ".join(search)

        result = self.searchSong(concat_query)
        
        song = Song(result["title"], result["formats"][0]["url"], result["thumbnails"][-1]["url"])
        if ctx.message.guild.id in self.queue:
            self.queue[ctx.message.guild.id].append(song)
        else:
            self.queue[ctx.message.guild.id] = [song]
        return song
                




