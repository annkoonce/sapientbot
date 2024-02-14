import discord
from discord.ext import commands

# Create a new bot instance
bot = commands.Bot(command_prefix='!')

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Command to greet users
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello! How can I help you today?')

# Command to get the current time
@bot.command(name='time')
async def time(ctx):
    # Implement logic to get the current time
    await ctx.send('The current time is: <current_time>')

# Command to start a trivia game
@bot.command(name='trivia')
async def trivia(ctx):
    # Implement logic to start a trivia game
    await ctx.send('Let\'s start a trivia game! Get ready...')

# Run the bot with the specified token
bot.run('YOUR_DISCORD_BOT_TOKEN')
