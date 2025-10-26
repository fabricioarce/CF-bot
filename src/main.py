# ==================== IMPORTS ====================

# Discord related imports
import discord
from discord.ext import commands

# System and utility imports
import os
import logging
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Custom modules
from src.codeforces_api import CodeForcesAPI
import src.commands as cf_commands

# ==================== INITIAL CONFIGURATION ====================

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot configuration dictionary
config = {
    "min_rating": 800,    # Minimum problem difficulty
    "max_rating": 1300,   # Maximum problem difficulty
    "channel_id": None,   # Will be set using !setchannel command
}

# ==================== SERVICE INITIALIZATION ====================

# Initialize Codeforces API for problem fetching
codeforces_api = CodeForcesAPI()

# Initialize scheduler for automated daily tasks
scheduler = AsyncIOScheduler()

# ==================== LOGGING CONFIGURATION ====================

# Configure logging handler for debugging and error tracking
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# ==================== DISCORD BOT SETUP ====================

# Configure required Discord intents
intents = discord.Intents.default()
intents.message_content = True  # For reading message content
intents.members = True          # For accessing member information
intents.guilds = True          # For accessing server information

# Create main bot instance with command prefix
bot = commands.Bot(command_prefix='!', intents=intents)


# ==================== SCHEDULED TASKS ====================

async def daily_problem_job():
    """
    Scheduled task that runs daily at 8:00 AM to send a Codeforces problem.
    Handles all necessary validations and error cases.
    """
    # Get configured channel ID
    channel_id = config.get("channel_id")
    
    # Validate channel configuration
    if not channel_id:
        print("⚠️ No channel configured for daily problems. Use !setchannel to set one.")
        return
    
    # Get Discord channel object
    channel = bot.get_channel(channel_id)
    
    # Validate channel existence
    if not channel:
        print(f"⚠️ ERROR: Could not find channel with ID: {channel_id}")
        return
    
    # Get Codeforces command handler
    cog = bot.get_cog("CodeForcesCog")
    
    # Validate cog availability
    if not cog:
        print("⚠️ ERROR: Could not find 'CodeForcesCog'")
        return
    
    # Attempt to send daily problem
    try:
        await cog.send_problem(
            channel, 
            config["min_rating"], 
            config["max_rating"]
        )
        print(f"✅ Daily problem sent successfully to channel {channel_id}")
    except Exception as e:
        print(f"❌ Error sending daily problem: {e}")
        import traceback
        traceback.print_exc()


# ==================== BOT EVENTS ====================

@bot.event
async def on_ready():
    """
    Event triggered when bot successfully connects to Discord.
    Handles initial setup and configuration reporting.
    """
    # Print initial connection information
    print("=" * 50)
    print(f'✅ Bot connected successfully')
    print(f'📛 Name: {bot.user.name}')
    print(f'🆔 ID: {bot.user.id}')
    print(f'🌐 Servers: {len(bot.guilds)}')
    print("=" * 50)
    
    # Initialize Codeforces command system
    await cf_commands.setup(bot, codeforces_api, config)
    print("✅ Codeforces commands loaded")
    
    # Configure and start daily problem scheduler
    scheduler.add_job(
        daily_problem_job,  # Task function
        'cron',            # Schedule type
        hour=15,            # Run at 8 AM
        minute=52           # At minute 0
    )
    scheduler.start()
    
    # Print scheduler configuration
    print(f"✅ Scheduler started")
    print(f"📅 Daily problem scheduled for 8:00 AM")
    
    # Report channel configuration
    channel_id = config.get("channel_id")
    if channel_id:
        print(f"📢 Target channel: {channel_id}")
    else:
        print(f"⚠️ No channel configured. Use !setchannel to set one.")
    
    # Report difficulty settings
    print(f"🎯 Difficulty range: {config['min_rating']} - {config['max_rating']}")
    print("=" * 50)

# ==================== ERROR HANDLING ====================

@bot.event
async def on_command_error(ctx, error):
    """
    Global error handler for all command execution errors.
    Provides user-friendly error messages and guidance.
    
    Args:
        ctx: Command context
        error: The error that occurred
    """
    if isinstance(error, commands.MissingRequiredArgument):
        # Handle missing required arguments
        await ctx.send(f"❌ Missing required argument: `{error.param.name}`")
        await ctx.send(f"💡 Use `!help {ctx.command.name}` to see how to use the command")
        
    elif isinstance(error, commands.CommandNotFound):
        # Handle unknown commands
        await ctx.send("❌ Command not found. Use `!help` to see available commands.")
        
    elif isinstance(error, commands.BadArgument):
        # Handle invalid argument formats
        await ctx.send("❌ Invalid argument. Check the command format.")
        await ctx.send(f"💡 Use `!help {ctx.command.name}` to see correct syntax")
        
    else:
        # Handle unexpected errors
        print(f"❌ Unhandled error in command '{ctx.command}': {error}")
        await ctx.send(f"❌ An unexpected error occurred: {str(error)}")


# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    # Start the bot with logging configuration
    bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)