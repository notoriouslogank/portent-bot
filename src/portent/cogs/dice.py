import random
import re

import discord
from discord import app_commands
from discord.ext import commands

_rng = random.SystemRandom()

DICE_RE = re.compile(
    r"""^\s*
        (?:(?P<count>\d*)d(?P<sides>\d+))   # NdM or dM
        (?P<mod>(?:\s*[+-]\s*\d+)*) ?       # optional +m -n ... (can chain)
        \s*$""",
    re.IGNORECASE | re.VERBOSE,
)

MAX_DICE = 100
MAX_SIDES = 1000
MAX_SUMMARY_LEN = 500


def parse_expression(expr: str) -> tuple[int, int, int]:
    m = DICE_RE.match(expr)
    if not m:
        raise ValueError("Use NdM format like '2d20', 'd6', or '4d6+2'.")

    count_str = m.group("count")
    sides = int(m.group("sides"))
    count = int(count_str) if count_str else 1

    mod = 0
    for token in re.findall(r"[+-]\s*\d+", m.group("mod") or ""):
        mod += int(token.replace(" ", ""))

    if not (1 <= count <= MAX_DICE):
        raise ValueError(f"Dice count must be 1-{MAX_DICE}.")
    if not (2 <= sides <= MAX_SIDES):
        raise ValueError(f"Sides must be 2-{MAX_SIDES}.")

    return count, sides, mod


class Dice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="roll", description="Roll dice with NdM notation (e.g., 2d20, 4d6+2, d100)."
    )
    @app_commands.describe(expression="Dice expression like 2d20, 4d6+2, d100")
    async def roll(self, interaction: discord.Interaction, expression: str):
        try:
            count, sides, mod = parse_expression(expression)
        except ValueError as e:
            await interaction.response.send_message(f"! {e}", ephemeral=True)
            return

        rolls = [_rng.randint(1, sides) for _ in range(count)]
        total = sum(rolls) + mod

        rolls_str = ", ".join(map(str, rolls))
        summary = f"**{count}d{sides}**"
        if mod:
            summary += f"{'+' if mod > 0 else ''}{mod}"
        detail = f"({rolls_str})"
        if len(detail) > MAX_SUMMARY_LEN:
            detail = f"({count} rolls... truncated)"

        embed = discord.Embed(
            title="Portent casts the bones",
            description=f"{summary} -> **{total}**\n{detail}",
            color=discord.Color.dark_purple(),
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Dice(bot))
