import discord
from discord import app_commands
from discord.ext import commands


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Latency check.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong")


async def setup(bot: commands.Bot):
    await bot.add_cog(Core(bot))
