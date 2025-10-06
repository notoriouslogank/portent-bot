import logging

import discord
from discord.ext.commands import Bot


async def sync_app_commands(bot: Bot, dev_guild_id: int | None, mode: str):
    log = logging.getLogger("portent")
    tree = bot.tree
    if mode == "guild" and dev_guild_id:
        guild = discord.Object(id=dev_guild_id)
        tree.copy_global_to(guild=guild)
        synced = await tree.sync(guild=guild)
        log.info(f"Synced {len(synced)} commands to dev guild {dev_guild_id}")
    elif mode == "global":
        synced = await tree.sync()
        log.info(f"Synced {len(synced)} global commands.")
    else:
        log.info("Skipping command sync (SYNC_MODE=none)")
