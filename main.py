import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ==================== INITIAL CONFIGURATION ====================

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Import custom modules
from codeforces_api import CodeForcesAPI
import commands as cf_commands

# ==================== BOT CONFIGURATION ====================

# Problem difficulty configuration
config = {
    "min_rating": 800,   # Minimum problem difficulty
    "max_rating": 1300,  # Maximum problem difficulty
}

# Create instance of Codeforces API
# This instance handles all requests to Codeforces
codeforces_api = CodeForcesAPI()

# Create scheduler for scheduled tasks (daily problems)
scheduler = AsyncIOScheduler()

# ==================== LOGGING CONFIGURATION ====================

# Configure log file for debugging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# ==================== INTENTS CONFIGURATION ====================

# Intents define which events the bot can receive
intents = discord.Intents.default()
intents.message_content = True  # Allows reading message content
intents.members = True          # Allows access to member information
intents.guilds = True           # Allows access to server information

# ==================== CREATE BOT INSTANCE ====================

# Create bot with command prefix "!" and configured intents
bot = commands.Bot(command_prefix='!', intents=intents)

# ==================== SCHEDULED TASKS ====================

async def daily_problem_job():
    """
    Scheduled task that runs daily at 8:00 AM
    Sends a Codeforces problem to the configured channel
    """
    # Get the channel where the problem will be sent
    channel = bot.get_channel(CHANNEL_ID)
    
    if channel:
        # Get the Cog containing Codeforces commands
        cog = bot.get_cog("CodeForcesCog")
        
        if cog:
            # Send problem using the Cog's method
            await cog.send_problem(
                channel, 
                config["min_rating"], 
                config["max_rating"]
            )
        else:
            print("⚠️ ERROR: Could not find the 'CodeForcesCog' Cog")
    else:
        print(f"⚠️ ERROR: Could not find the channel with ID: {CHANNEL_ID}")

# ==================== BOT EVENTS ====================

@bot.event
async def on_ready():
    """
    Event that runs when the bot successfully connects to Discord
    """
    print("=" * 50)
    print(f'✅ Bot connected successfully')
    print(f'📛 Name: {bot.user.name}')
    print(f'🆔 ID: {bot.user.id}')
    print(f'🌐 Servers: {len(bot.guilds)}')
    print("=" * 50)
    
    # Load Codeforces commands (Cog)
    await cf_commands.setup(bot, codeforces_api, config)
    print("✅ Codeforces commands loaded")
    
    # Configure and start the scheduler for daily problems
    # Will run every day at 8:00 AM
    scheduler.add_job(
        daily_problem_job,  # Function to execute
        'cron',             # Type: cron schedule
        hour=15,             # Hour: 8 AM
        minute=31            # Minute: 00
    )
    scheduler.start()
    
    print(f"✅ Scheduler started")
    print(f"📅 Daily problem scheduled for 8:00 AM")
    print(f"📢 Target channel: {CHANNEL_ID}")
    print(f"🎯 Difficulty range: {config['min_rating']} - {config['max_rating']}")
    print("=" * 50)

@bot.event
async def on_command_error(ctx, error):
    """
    Event that handles errors when executing commands
    
    Parameters:
        ctx: Command context
        error: The error that occurred
    """
    if isinstance(error, commands.MissingRequiredArgument):
        # A required argument is missing in the command
        await ctx.send(f"❌ Missing required argument: `{error.param.name}`")
        await ctx.send(f"💡 Use `!help {ctx.command.name}` to see how to use the command")
        
    elif isinstance(error, commands.CommandNotFound):
        # The command does not exist
        await ctx.send("❌ Command not found. Use `!help` to see available commands.")
        
    elif isinstance(error, commands.BadArgument):
        # Argument with incorrect format
        await ctx.send("❌ Invalid argument. Check the command format.")
        await ctx.send(f"💡 Use `!help {ctx.command.name}` to see the correct syntax")
        
    else:
        # Error not specifically handled
        print(f"❌ Unhandled error in command '{ctx.command}': {error}")
        await ctx.send(f"❌ An unexpected error occurred: {str(error)}")

# ==================== RUN THE BOT ====================

if __name__ == "__main__":
    # Run the bot with the token and logging configuration
    bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)