import discord
from discord.ext import commands

class CodeForcesCog(commands.Cog):
    """Cog containing all Codeforces-related commands"""
    
    def __init__(self, bot, codeforces_api, config):
        self.bot = bot
        self.cf_api = codeforces_api
        self.config = config
    
    async def send_problem(self, channel, min_rating, max_rating):
        """Fetches and sends a Codeforces problem to the specified channel"""
        problem = self.cf_api.get_random_problem(min_rating, max_rating)
        problem_data = self.cf_api.format_problem_data(problem)
        
        # ==================== CODEFORCES COG DEFINITION ====================

        if problem_data is None:
            await channel.send("❌ No problem found in that difficulty range.")
            return
        
        # Create embed with problem information
        embed = discord.Embed(
            title="💻 Daily Codeforces Problem", 
            color=0x3498db,
            description=f"**{problem_data['name']}**"
        )
        
        # Difficulty field with bars
        difficulty_text = f"{problem_data['difficulty_bars']} **{problem_data['rating']}**"
        embed.add_field(
            name="🎯 Difficulty",
            value=difficulty_text,
            inline=True
        )
        
        # Tags field
        if problem_data['tags']:
            tags_text = ", ".join([f"`{tag}`" for tag in problem_data['tags']])
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

    # ==================== COMMANDS ====================
    
    @commands.command(name="testdaily")
    async def test_daily(self, ctx):
        """Test manual sending of daily problem using configured range"""
        await self.send_problem(
            ctx.channel, 
            self.config["min_rating"], 
            self.config["max_rating"]
        )
    
    @commands.command(name="problem")
    async def problem_cmd(self, ctx, min_rating: int, max_rating: int):
        """Get a problem with custom difficulty range"""
        await self.send_problem(ctx.channel, min_rating, max_rating)
    
    @commands.command(name="showrange")
    async def showrange(self, ctx):
        """Show the current configured difficulty range"""
        await ctx.send(
            f"📘 Current difficulty range: **{self.config['min_rating']}** - **{self.config['max_rating']}**"
        )
    
    @commands.command(name="setrange")
    async def setrange(self, ctx, min_rating: int, max_rating: int):
        """Update the difficulty range for daily problems"""
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

    # ==================== COG SETUP FUNCTION ====================

async def setup(bot, codeforces_api, config):
    """Register the Cog with the bot"""
    await bot.add_cog(CodeForcesCog(bot, codeforces_api, config))