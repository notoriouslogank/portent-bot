import asyncio
import logging

import discord
from discord.ext import commands

from portent.command_sync import sync_app_commands
from portent.config import settings
from portent.logging_setup import setup_logging
from portent.utils.assets import path_branding

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.guilds = True
INTENTS.members = False
extensions = [
    "portent.cogs.core",
    "portent.cogs.dice",
]


class PortentBot(commands.Bot):
    async def setup_hook(self):
        for ext in extensions:
            await self.load_extension(ext)
        await sync_app_commands(self, dev_guild_id=settings.dev_guild_id, mode=settings.sync_mode)

async def _main():
    setup_logging(settings.log_level)
    log = logging.getLogger("portent")

    bot = PortentBot(
        command_prefix="!",
        intents=INTENTS,
        application_id=settings.app_id,
    )

    @bot.event
    async def on_ready():
        log.info(f"[bold]Portent[/] online as [cyan]{bot.user}[/] (id={bot.user.id})")
#    icon_path = path_branding("icon.png")
#    with open(icon_path, "rb") as f:
#        asset = await bot.user.display_avatar.replace()
    await bot.start(settings.token)


def main():
    asyncio.run(_main())
