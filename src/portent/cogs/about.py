import platform

import discord
from discord import app_commands
from discord.ext import commands

# Prefer dynamic metadata; fall back to hardcoded strings if missing
try:
    import importlib.metadata as im
    PKG = "portent"
    VERSION = im.version(PKG)
    META = im.metadata(PKG)
    DESC = META.get("Summary", "A slash-first Discord bot; successor to Harbinger.")
    HOMEPAGE = META.get("Home-page") or META.get("Project-URL") or ""
except Exception:
    VERSION = "0+unknown"
    DESC = "A slash-first Discord bot; successor to Harbinger."
    HOMEPAGE = ""

REPO_URL = HOMEPAGE or "https://github.com/notoriouslogank/portent-bot.git"

class About(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="about", description="Show bot version and repository link.")
    async def about(self, interaction: discord.Interaction):

        py = platform.python_version()
        dp = discord.__version__
        guilds = len(self.bot.guilds)

        embed = discord.Embed( title="Portent", description="DESC", color=discord.Color.purple(),)
        embed.add_field(name="Version", value=VERSION, inline=True)
        embed.add_field(name="discord.py", value=dp, inline=True)
        embed.add_field(name="Python", value=py, inline=True)
        embed.add_field(name="Servers", value=str(guilds), inline=True)
        if REPO_URL:
            embed.add_field(name="GitHub", value=REPO_URL, inline=False)

        if self.bot.user and self.bot.user.display_avatar:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(About(bot))

