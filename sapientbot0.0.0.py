import discord
import requests
from discord.ext import commands
import keepalive
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
import tkinter as tk
from tkinter import messagebox
import threading
import sys
from flask import Flask  

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello SAPIENTBOT is Online & Ready.'

# Bot run command modification to allow Flask to run in a separate thread
if __name__ == "__main__":
    from threading import Thread
    def run():
        app.run(host='0.0.0.0', port=8000)
    # Start the Flask server in a new thread
    t = Thread(target=run)
    t.start()

# Create a new bot instance
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print('SAPIENTBOT is online & ready.')

@bot.event
async def on_message(message):
    if bot.user in message.mentions:
        await message.channel.send('You mentioned me!')
        await message.channel.send('How can I help you today?')
    await bot.process_commands(message)

@bot.command()
async def play(ctx, *, song_name):
    sp = Spotify(client_credentials_manager=SpotifyClientCredentials())
    results = sp.search(q=song_name, limit=1)
    if results['tracks']['items']:
        await ctx.send(f'Now playing: {song_name}')
    else:
        await ctx.send('Song not found on Spotify.')

@bot.command()
async def recommend_streamers(ctx):
    streamers = ['Streamer1', 'Streamer2', 'Streamer3']
    await ctx.send(f'Check out these Twitch streamers: {", ".join(streamers)}')

@bot.command()
async def news(ctx):
    news_api_key = 'your_news_api_key_here'
    news_url = f'https://newsapi.org/v2/top-headlines?category=technology&apiKey={news_api_key}'
    response = requests.get(news_url)
    articles = response.json()['articles']
    headlines = [article['title'] for article in articles]
    await ctx.send('\n'.join(headlines[:5]))

#Tells Bot to log on with credentials
bot.run(keepalive.DISCORD_BOT_TOKEN)
