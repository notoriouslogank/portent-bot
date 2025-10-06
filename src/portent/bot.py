import asyncio
import logging

import discord
from discord.ext import commands

from portent.command_sync import sync_app_commands
from portent.config import settings
from portent.logging_setup import setup_logging

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.guilds = True
INTENTS.members = False
extensions = [
    "portent.cogs.core",
]


async def _main():
    setup_logging(settings.log_level)
    log = logging.getLogger("portent")

    bot = commands.Bot(command_prefix="!", intents=INTENTS)
    for ext in extensions:
        await bot.load_extension(ext)

    @bot.event
    async def on_ready():
        log.info(f"[bold]Portent[/] online as [cyan]{bot.user}[/] (id={bot.user.id})")
        await sync_app_commands(bot, dev_guild_id=settings.dev_guild_id, mode=settings.sync_mode)

    await bot.start(settings.token)


def main():
    asyncio.run(_main())
