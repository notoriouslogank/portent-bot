from __future__ import annotations

from random import randint
from typing import Literal

import aiohttp
import discord
import wikipediaapi
from discord import Interaction, app_commands
from discord.ext import commands

# from jokeapi import Jokes

ACCENT = discord.Color.from_rgb(139, 92, 248)
MAX_EMBED_DESC = 4096
HTTP_OK = 200
EVIL_INSULT_URL = "https://evilinsult.com/generate_insult.php?lang=en&type=json"


def make_bubble_wrap(rows: int = 12, cols: int = 18) -> str:
    cell = "||pop||"
    return "\n".join("".join(cell for _ in range(cols)) for _ in range(rows))


class Tools(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    tools = app_commands.Group(name="tools", description="Utilities and fun stuff")

    # /wiki
    @tools.command(name="wiki", description="Get a Wikipedia summary for a topic.")
    @app_commands.describe(query="Topic to search on Wikipedia.")
    async def wiki(self, itx: Interaction, query: str) -> None:
        await itx.response.defer(thinking=True)
        wiki = wikipediaapi.Wikipedia("PortentBot/1.0 (Discord)", "en")
        page = wiki.page(query)

        if not page.exists():
            await itx.followup.send(f"Couldn't find a page for **{query}**.")
            return

        title = page.title
        summary = page.summary or "No summary available"
        embed = discord.Embed(
            title=title,
            description=summary[:MAX_EMBED_DESC],
            color=ACCENT,
            url=f"https://wikipedia.org/wiki/{title.replace(' ', '_')}",
        )
        await itx.followup.send(embed=embed)

    # /bw
    @tools.command(name="bw", description="Unspool some bubble wrap.")
    async def bw(self, itx: Interaction) -> None:
        await itx.response.send_message(make_bubble_wrap())

    # /slang
    @tools.command(name="slang", description="Search Urban Dictionary.")
    @app_commands.describe(query="Term or phrase to define")
    async def slang(self, itx: Interaction, query: str) -> None:
        await itx.response.defer(thinking=True)
        url = f"https://www.urbandictionary.com/define.php?term={query.strip().replace(' ', '+')}"
        await itx.followup.send(f"Let me see what I can find for **{query}**...\n{url}")

    # /insult
    @tools.command(name="insult", description="Send a random insult to a user.")
    @app_commands.describe(member="who to insult")
    async def insult(self, itx: Interaction, member: discord.Member) -> None:
        await itx.response.defer(thinking=True)
        async with aiohttp.ClientSession() as session, session.get(EVIL_INSULT_URL) as resp:
            if resp.status != HTTP_OK:
                await itx.followup.send("Insult generator is grumpy right now!")
                return
        data = await resp.json()
        insult_text = str(data.get("insult", "You magnificent bastard!"))
        await itx.followup.send(f"{member.mention}: {insult_text}")

    # /lmgtfy
    @tools.command(name="lmgtfy", description="Let me Google that for you.")
    @app_commands.describe(query="Search query")
    async def lmgtfy(self, itx: Interaction, query: str) -> None:
        await itx.response.defer(thinking=True)
        url = f"https://google.com/search?q={query.strip().replace(' ', '+')}"
        await itx.followup.send(f"Here, let me just Google that for you...\n{url}")

    # /define
    @tools.command(name="define", description="Define a word.")
    @app_commands.describe(word="Word to define")
    async def define(self, itx: Interaction, word: str) -> None:
        await itx.response.defer(thinking=True)
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        async with aiohttp.ClientSession() as session, session.get(url) as resp:
            if resp.status != HTTP_OK:
                await itx.followup.send(f"Couldn't fetch a definition for **{word}**.")
                return
            try:
                payload = await resp.json()
                entry = payload[0]
                phonetics = entry.get("phonetics") or []
                meanings = entry.get("meanings") or []

                audio = (phonetics[0].get("audio") if phonetics else None) or None
                phon_text = (phonetics[0].get("text") if phonetics else None) or None
                definition = (
                    meanings[0].get("definitions")[0].get("definition")
                    if meanings and meanings[0].get("definitions")
                    else None
                )
                desc = "No phonetics guide available."
                if phon_text and not audio:
                    desc = phon_text
                elif phon_text and audio:
                    desc = f"[{phon_text}]({audio})"

                embed = discord.Embed(title=word, description=desc, color=ACCENT)
                if definition:
                    embed.add_field(name="\u200b", value=definition, inline=False)
                await itx.followup.send(embed=embed)
            except Exception:
                await itx.followup.send(
                    f"Something went sideways parsing the entry for **{word}**."
                )

    # /tools rps
    @tools.command(name="rps", description="Play rock, paper, scissors.")
    @app_commands.describe(choice="Your move")
    async def rps(self, itx: Interaction, choice: Literal["rock", "paper", "scissors"]) -> None:
        options = ["rock", "paper", "scissors"]
        bot_choice = options[randint(0, 2)]

        embed = discord.Embed(color=ACCENT, title="rock, paper, scissors")
        embed.add_field(name=str(itx.user), value=choice, inline=True)
        embed.add_field(name=str(self.bot.user), value=bot_choice, inline=True)

        result = "You lose!"
        if choice == bot_choice:
            result = "You tied!"
        elif (
            (bot_choice == "rock" and choice == "paper")
            or (bot_choice == "paper" and choice == "scissors")
            or (bot_choice == "scissors" and choice == "rock")
        ):
            result = "You win!"

        embed.add_field(name="result", value=result, inline=False)
        await itx.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Tools(bot))
