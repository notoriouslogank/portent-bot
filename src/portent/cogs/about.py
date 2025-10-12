import platform
import sys
from datetime import UTC, datetime
from importlib import metadata as importlib_metadata

import discord
from discord import app_commands
from discord.ext import commands


def get_meta():
    try:
        return importlib_metadata.metadata("portent")
    except Exception:
        return {}

ACCENT = discord.Color.from_rgb(139, 92, 246)


def py_version() -> str:
    return ".".join(map(str, sys.version_info[:3]))


VERSION, DESC, REPO_URL = get_meta()


class About(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="about", description="Show bot version and repository link.")
    async def about(self, interaction: discord.Interaction):
        guilds = len(self.bot.guilds)
        dp_ver = discord.__version__
        py_ver = py_version()
        platform_name = platform.system()

        embed = discord.Embed(
            title="Portent",
            description="*Occult-mechanical oracle for your server.*",
            color=ACCENT,
            timestamp=datetime.now(UTC),
        )

        if self.bot.user and self.bot.user.display_avatar:
            embed.set_author(name=str(self.bot.user), icon_url=self.bot.user.display_avatar.url)
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.add_field(name="Version", value=f"`{VERSION}`", inline=True)
        embed.add_field(name="Runtime", value=f"py `{py_ver}` - d.py `{dp_ver}`", inline=True)
        embed.add_field(name="Servers", value=f"{guilds}", inline=True)

        embed.add_field(name="Platform", value=f"{platform_name}", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)

        if REPO_URL:
            embed.add_field(
                name="GitHub", value=f"[notoriouslogank/portent-bot]({REPO_URL})", inline=False
            )

        embed.set_footer(text=f"Invoked by {interaction.user.display_name}")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(About(bot))
