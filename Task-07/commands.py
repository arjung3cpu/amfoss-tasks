import discord
import requests

from discord.ext import commands

from economy import (
    ensure_user,
    get_balance,
    daily_reward,
    transfer,
    raid as perform_raid,
    get_shop,
    buy_item
)

from database import get_inventory, get_top_users

from onepiece_api import get_logpose


def setup_commands(bot):

    @bot.command()
    async def bounty(ctx):
        ensure_user(ctx.author.id, str(ctx.author))

        balance = get_balance(ctx.author.id)

        await ctx.send(
            f"🏴‍☠️ {ctx.author.mention}, your current bounty is "
            f"**{balance} Berries**."
        )

    @bot.command()
    async def setsail(ctx):
        ensure_user(ctx.author.id, str(ctx.author))

        reward = daily_reward(ctx.author.id)
        balance = get_balance(ctx.author.id)

        await ctx.send(
            f"🏴‍☠️ {ctx.author.mention} set sail and earned "
            f"**{reward} Berries**!\n"
            f"💰 Current bounty: **{balance} Berries**"
        )

    @bot.command()
    async def trade(ctx, member: discord.Member, amount: int):

        ensure_user(ctx.author.id, str(ctx.author))
        ensure_user(member.id, str(member))

        if member.id == ctx.author.id:
            await ctx.send("❌ You cannot trade with yourself.")
            return

        success, message = transfer(
            ctx.author.id,
            member.id,
            amount
        )

        if success:

            sender_balance = get_balance(ctx.author.id)
            receiver_balance = get_balance(member.id)

            await ctx.send(
                f"🏴‍☠️ **Trade successful!**\n"
                f"💰 {ctx.author.mention} sent **{amount} Berries** "
                f"to {member.mention}.\n"
                f"Your new balance: **{sender_balance} Berries**\n"
                f"{member.mention}'s balance: "
                f"**{receiver_balance} Berries**"
            )

        else:
            await ctx.send(f"❌ {message}")

    @bot.command()
    async def logpose(ctx):

        await ctx.send("🧭 Reading the Log Pose...")

        try:

            data = get_logpose()

            if data is None:
                await ctx.send(
                    "❌ The Log Pose could not find any information."
                )
                return

            await ctx.send(
                f"🧭 **LOG POSE**\n"
                f"🏴‍☠️ Pirate: **{data['character']}**\n"
                f"💰 Bounty: **{data['bounty']} Berries**\n"
                f"🍈 Devil Fruit: **{data['fruit']}**\n"
                f"🔮 Model: **{data['model']}**\n"
                f"⚡ Type: **{data['type']}**"
            )

        except requests.RequestException as error:

            print(f"Log Pose API error: {error}")

            await ctx.send(
                "❌ The Log Pose failed to connect to the Grand Line."
            )

        except Exception as error:

            print(f"Log Pose error: {error}")

            await ctx.send(
                "❌ Something went wrong while reading the Log Pose."
            )

    @bot.command()
    async def shop(ctx):

        shop = get_shop()

        message = "🏪 **PIRATE SHOP**\n\n"

        for name, item in shop.items():

            message += (
                f"🏴‍☠️ **{name}** — "
                f"**{item['price']} Berries**\n"
                f"   {item['description']}\n\n"
            )

        await ctx.send(message)

    @bot.command()
    async def inventory(ctx):

        ensure_user(ctx.author.id, str(ctx.author))

        items = get_inventory(ctx.author.id)

        if not items:

            await ctx.send(
                f"🎒 {ctx.author.mention}, your inventory is empty."
            )

            return

        message = (
            f"🎒 **{ctx.author.display_name}'s Inventory**\n\n"
        )

        for item in items:
            message += f"🏴‍☠️ {item}\n"

        await ctx.send(message)

    @bot.command()
    async def buy(ctx, item_name: str):

        ensure_user(ctx.author.id, str(ctx.author))

        success, result = buy_item(
            ctx.author.id,
            item_name
        )

        if not success:

            await ctx.send(f"❌ {result}")

            return

        balance = get_balance(ctx.author.id)

        await ctx.send(
            f"🛒 **Purchase successful!**\n"
            f"🏴‍☠️ You bought **{result}**.\n"
            f"💰 Remaining balance: **{balance} Berries**"
        )

    @bot.command()
    async def worstgeneration(ctx):

        users = get_top_users(5)

        if not users:

            await ctx.send("❌ No pirates found.")

            return

        message = (
            "🏴‍☠️ **WORST GENERATION — TOP 5 RICHEST PIRATES**\n\n"
        )

        for position, (username, berries) in enumerate(
            users,
            start=1
        ):

            message += (
                f"**{position}.** 🏴‍☠️ {username} — "
                f"💰 **{berries} Berries**\n"
            )

        await ctx.send(message)

    @bot.command()
    async def raid(ctx, member: discord.Member):

        ensure_user(ctx.author.id, str(ctx.author))
        ensure_user(member.id, str(member))

        if member.id == ctx.author.id:

            await ctx.send(
                "❌ You cannot raid yourself, Pirate King!"
            )

            return

        success, message, amount = perform_raid(
            ctx.author.id,
            member.id
        )

        if success:

            attacker_balance = get_balance(ctx.author.id)

            await ctx.send(
                f"⚔️ **RAID SUCCESSFUL!**\n"
                f"🏴‍☠️ {ctx.author.mention} raided "
                f"{member.mention}!\n"
                f"💰 You stole **{amount} Berries**!\n"
                f"💰 Your new bounty: **{attacker_balance} Berries**"
            )

        else:

            attacker_balance = get_balance(ctx.author.id)

            await ctx.send(
                f"💀 **RAID FAILED!**\n"
                f"🏴‍☠️ {member.mention} defended their stash!\n"
                f"💸 You lost **{amount} Berries**.\n"
                f"💰 Your bounty: **{attacker_balance} Berries**"
            )
