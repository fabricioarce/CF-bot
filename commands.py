# ==================== IMPORTS ====================

import discord
from discord.ext import commands

# ==================== COG DEFINITION ====================

class CodeForcesCog(commands.Cog):
    """
    Cog containing all Codeforces-related commands and functionality.
    Handles problem fetching, channel management, and configuration.
    """
    
    def __init__(self, bot, codeforces_api, config):
        """
        Initialize the Codeforces command handler.
        
        Args:
            bot: The Discord bot instance
            codeforces_api: Instance of CodeForcesAPI for problem fetching
            config: Configuration dictionary
        """
        self.bot = bot
        self.cf_api = codeforces_api
        self.config = config
    
    # ==================== CORE FUNCTIONALITY ====================
    
    async def send_problem(self, channel, min_rating, max_rating):
        """Fetches and sends a Codeforces problem to the specified channel"""
        problem = self.cf_api.get_random_problem(min_rating, max_rating)
        problem_data = self.cf_api.format_problem_data(problem)
        
        if problem_data is None:
            await channel.send("❌ No problem found in that difficulty range.")
            return
        
        # Create embed with problem information
        embed = discord.Embed(
            title="💻 Daily Codeforces Problem", 
            color=0x3498db,
            description=f"**{problem_data['name']}**"
        )
        
        # Difficulty field with bars (with safety check)
        difficulty_bars = problem_data.get('difficulty_bars', '')
        rating = problem_data.get('rating', 'N/A')
        difficulty_text = f"{difficulty_bars} **{rating}**" if difficulty_bars else f"**{rating}**"
        
        embed.add_field(
            name="🎯 Difficulty",
            value=difficulty_text,
            inline=True
        )
        
        # Tags field
        tags = problem_data.get('tags', [])
        if tags:
            tags_text = ", ".join([f"`{tag}`" for tag in tags])
        else:
            tags_text = "No tags"
        
        embed.add_field(
            name="🏷️ Tags",
            value=tags_text,
            inline=False
        )
        
        # Problem link
        embed.add_field(
            name="🔗 Link",
            value=f"[Solve problem]({problem_data['url']})",
            inline=False
        )
        
        embed.set_footer(text="Good luck! 🚀")
        
        await channel.send(embed=embed)
    
    # ==================== TESTING COMMANDS ====================
    
    @commands.command(name="testdaily")
    async def test_daily(self, ctx):
        """
        Test manual sending of daily problem using the configured range.
        Useful for verifying bot functionality.
        """
        await self.send_problem(
            ctx.channel, 
            self.config["min_rating"], 
            self.config["max_rating"]
        )
    
    # ==================== PROBLEM COMMANDS ====================
    
    @commands.command(name="problem")
    async def problem_cmd(self, ctx, min_rating: int, max_rating: int):
        """
        Get a problem with custom difficulty range.
        
        Args:
            min_rating: Minimum problem difficulty
            max_rating: Maximum problem difficulty
        """
        await self.send_problem(ctx.channel, min_rating, max_rating)
    
    # ==================== CONFIGURATION COMMANDS ====================
    
    @commands.command(name="showrange")
    async def showrange(self, ctx):
        """
        Show the current configured difficulty range.
        Displays both minimum and maximum ratings.
        """
        await ctx.send(
            f"📘 Current difficulty range: **{self.config['min_rating']}** - **{self.config['max_rating']}**"
        )
    
    @commands.command(name="setrange")
    async def setrange(self, ctx, min_rating: int, max_rating: int):
        """
        Update the difficulty range for daily problems.
        
        Args:
            min_rating: New minimum problem difficulty
            max_rating: New maximum problem difficulty
        
        Validates that:
        - Minimum is less than maximum
        - Ratings are within typical Codeforces range (800-3500)
        """
        if min_rating >= max_rating:
            await ctx.send("❌ Minimum rating must be less than maximum rating.")
            return
        
        if min_rating < 800 or max_rating > 3500:
            await ctx.send("⚠️ Warning: Typical Codeforces range is 800-3500.")
        
        self.config["min_rating"] = min_rating
        self.config["max_rating"] = max_rating
        
        await ctx.send(
            f"✅ Difficulty range updated to: **{min_rating}** - **{max_rating}**"
        )
    
    # ==================== CHANNEL MANAGEMENT ====================
    
    @commands.command(name="setchannel")
    async def set_channel(self, ctx, channel: discord.TextChannel = None):
        """
        Set the channel where daily problems will be sent.
        
        Args:
            channel: Target channel (optional, defaults to current channel)
        
        Usage: 
            !setchannel #channel-name
            !setchannel (uses current channel)
        """
        # If no channel specified, use current channel
        target_channel = channel if channel else ctx.channel
        
        # Update config with new channel ID
        self.config["channel_id"] = target_channel.id
        
        await ctx.send(
            f"✅ Daily problems will be sent to {target_channel.mention}"
        )
    
    @commands.command(name="showchannel")
    async def show_channel(self, ctx):
        """Show the currently configured channel for daily problems"""
        channel_id = self.config.get("channel_id")
        
        if not channel_id:
            await ctx.send("⚠️ No channel configured. Use `!setchannel` to set one.")
            return
        
        channel = self.bot.get_channel(channel_id)
        
        if channel:
            await ctx.send(f"📢 Daily problems channel: {channel.mention}")
        else:
            await ctx.send("❌ Configured channel not found. Please set a new one with `!setchannel`.")
    
    @commands.command(name="config")
    async def show_config(self, ctx):
        """Show all current bot configuration"""
        channel_id = self.config.get("channel_id")
        channel = self.bot.get_channel(channel_id) if channel_id else None
        
        embed = discord.Embed(
            title="⚙️ Bot Configuration",
            color=0x2ecc71
        )
        
        embed.add_field(
            name="🎯 Difficulty Range",
            value=f"**{self.config['min_rating']}** - **{self.config['max_rating']}**",
            inline=False
        )
        
        embed.add_field(
            name="📢 Daily Problems Channel",
            value=channel.mention if channel else "❌ Not configured",
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot, codeforces_api, config):
    """Register the Cog with the bot"""
    await bot.add_cog(CodeForcesCog(bot, codeforces_api, config))