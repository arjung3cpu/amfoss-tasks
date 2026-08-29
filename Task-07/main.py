import os
import discord
from discord.ext import commands

from database import init_db
from commands import setup_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Berry Broker is ready!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    print(f"Error: {error}")


def main():
    init_db()
    setup_commands(bot)
    token = os.getenv("DISCORD_TOKEN")

    if not token:
        print("ERROR: DISCORD_TOKEN environment variable is not set.")
        return

    bot.run(token)


if __name__ == "__main__":
    main()
