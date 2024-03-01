import logging
import sys
import threading

from flask import Flask, request
import discord
from discord.ext import commands
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
from flask import request
import keepalive

# Set up logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler = logging.FileHandler(r'G:\SAPIENTBOT\SAPIENTBOT0.0.2.0\Logs\SBLogs.log')
handler.setFormatter(formatter)

log.addHandler(handler)

app = Flask(__name__)

chatbot = ChatBot('SAPIENTBOT')
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus


trainer.train("chatterbot.corpus.english")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["user_input"]
    response = chatbot.get_response(user_input)
    return {"response": str(response)}

@app.route('/')
def home():
    app.logger.debug('This is a DEBUG message')
    app.logger.info('This is an INFO message')
    app.logger.warning('This is a WARNING message')
    app.logger.error('This is an ERROR message')
    app.logger.critical('This is a CRITICAL message')
    return 'Hello SAPIENTBOT is Online & Ready.'

# Create a new bot instance
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print('SAPIENTBOT is online & ready.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        await message.channel.send('You mentioned me!')
        await message.channel.send('How can I help you today?')
    else:
        response = chatbot.get_response(message.content)
        await message.channel.send(response)

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
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        headlines = [article['title'] for article in articles]
        await ctx.send('\n'.join(headlines[:5]))
    else:
        await ctx.send('Unable to fetch news at the moment.')

#Tells Bot to log on with credentials
def run_bot():
    bot.run(keepalive.DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    run_bot()
    app.run(host='0.0.0.0', port=8000)
