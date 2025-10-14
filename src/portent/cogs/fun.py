from __future__ import annotations

from random import randint
from typing import Literal

import aiohttp
import discord
from discord import Interaction, app_commands
from discord.ext import commands

# from jokeapi import Jokes

ACCENT = discord.Color.from_rgb(139, 92, 248)
MAX_EMBED_DESC = 4096
HTTP_OK = 200
EVIL_INSULT_URL = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
MEDIAWIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_ICON = "https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png"


def brand_embed(title: str, desc: str | None = None) -> discord.Embed:
    e = discord.Embed(title=title, description=desc, color=ACCENT)
    e.set_footer(text="Portent | tools")
    e.timestamp = discord.utils.utcnow()
    return e


def make_bubble_wrap(rows: int = 12, cols: int = 18) -> str:
    cell = "||pop||"
    return "\n".join("".join(cell for _ in range(cols)) for _ in range(rows))


class LinkRow(discord.ui.View):
    def __init__(self, *, url: str, label: str = "Open", timeout: float | None = 30):
        super().__init__(timeout=timeout)
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.link, url=url, label=label))


class Tools(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    tools = app_commands.Group(name="tools", description="Utilities and fun stuff")

    # /wiki
    @tools.command(name="wiki", description="Get a Wikipedia summary for a topic.")
    @app_commands.describe(query="Topic to search on Wikipedia.", private="Send only to yourself!")
    async def wiki(self, itx: Interaction, query: str, private: bool = False) -> None:
        await itx.response.defer(thinking=True, ephemeral=private)
        params = {
            "action": "query",
            "prop": "pageimages|info|extracts",
            "inprop": "url",
            "exintro": "True",
            "explaintext": "True",
            "titles": query,
            "pithumbsize": "512",
            "format": "json",
            "origin": "*",
        }

        try:
            async with aiohttp.ClientSession() as s, s.get(MEDIAWIKI_API, params=params) as r:
                if r.status != HTTP_OK:
                    await itx.followup.send("Wikipedia is being moody.  Try again later!")
                    return
                data = await r.json()
        except Exception as e:
            await itx.followup.send(f"Couldn't reach Wikipedia right now. \n{e}")
            return

        pages = data.get("query", {}).get("pages", {})
        if not pages or "-1" in pages:
            await itx.followup.send(f"Couldn't find a page for **{query}**.")
            return

        page = next(iter(pages.values()))
        title = page.get("title", query)
        url = page.get("fullurl", f"https://wikipedia.org/wiki/{title.replace(' ', '_')}")
        thumb = page.get("thumbnail", {}).get("source")
        extract = (page.get("extract") or "No summary available.")[:MAX_EMBED_DESC]

        embed = brand_embed(title, extract)
        embed.set_author(name="Wikipedia", icon_url=WIKI_ICON, url=url)
        if thumb:
            embed.set_thumbnail(url=thumb)

        await itx.followup.send(embed=embed, view=LinkRow(url=url), ephemeral=private)

    #    @wiki.autocomplete("query")
    #    async def ac_wiki(self, itx: Interaction, current: str):
    #        if not current:
    #            return []
    #        params = {
    #            "action": "opensearch",
    #            "search": current,
    #            "limit": 10,
    #            "namespace": 0,
    #            "format": "json",
    #            "origin": "*",
    #        }
    #        try:
    #            async with aiohttp.ClientSession() as s, s.get(MEDIAWIKI_API, params=params) as r:
    #                if r.status != HTTP_OK:
    #                    return []
    #                data = await r.json()
    #                titles = data[1] if isinstance(data, list) and len(data) > 1 else []
    #        except Exception:
    #            return []
    #        return [app_commands.Choice(name=t[:100], value=t[:100]) for t in titles]

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
        await itx.followup.send(
            f"Let me see what I can find for **{query}**...",
            view=LinkRow(url=url, label="Open results"),
        )

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
