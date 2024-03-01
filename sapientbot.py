import os
import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import spacy
from transformers import pipeline
import keepalive

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

nlp = spacy.load('en_core_web_sm')
sentiment_analysis = pipeline('sentiment-analysis')

chatbot = ChatBot('SAPIENTBOT')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

#BOT INTENTS & COOMMANDS !!
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=['/', '!'], intents=intents)
async def check_role(ctx, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role in ctx.author.roles:
        await ctx.send('You have this role.')
    else:
        await ctx.send('You do not have this role.')

#Restricted commands & Cooldowns
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def my_command(ctx):
    await ctx.send('This command has a cooldown of 5 seconds per user.')
@commands.has_role('Admin')
async def restricted(ctx):
    await ctx.send('You have access to this command.')

#Console bot is online
@bot.event
async def on_ready():
    print('SAPIENTBOT is online & ready.')

#NLP & Grammar
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        await message.channel.send('You mentioned me!')
        await message.channel.send('How can I help you today?')
    else:
        doc = nlp(message.content)
        entities = [ent.text for ent in doc.ents]
        result = sentiment_analysis(message.content)[0]
        response = f"I detected the following entities in your message: {', '.join(entities)}"
        response += f"\nThe sentiment of your message is {result['label']} with a score of {result['score']}."
        response += f"\nChatbot response: {chatbot.get_response(message.content)}"
        await message.channel.send(response)

    await bot.process_commands(message)

#SPOTIFY CODE
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=(keepalive.SPOTIFY_CLIENT_ID),
                                                           client_secret=(keepalive.SPOTIFY_CLIENT_SECRET)))
@bot.command()
async def play(ctx, *, song_name):
    results = sp.search(q=song_name, limit=1)
    if results['tracks']['items']:
        song = results['tracks']['items'][0]
        await ctx.send(f'Now playing: {song["name"]}\n{song["external_urls"]["spotify"]}')
    else:
        await ctx.send('Song not found')
    
#BOT RUN
def run_bot():
    bot.run(keepalive.DISCORD_BOT_TOKEN)
