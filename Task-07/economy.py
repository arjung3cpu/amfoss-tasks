import random

from database import (
    create_user,
    get_bounty,
    update_bounty,
    log_transaction,
    add_inventory_item
)


def ensure_user(user_id, username):
    create_user(user_id, username)


def get_balance(user_id):
    return get_bounty(user_id)


def add_berries(user_id, amount, action):
    update_bounty(user_id, amount)
    log_transaction(user_id, action, amount)


def daily_reward(user_id):
    reward = random.randint(50, 150)

    add_berries(
        user_id,
        reward,
        "setsail"
    )

    return reward


def transfer(sender_id, receiver_id, amount):

    if amount <= 0:
        return False, "Amount must be greater than 0."

    sender_balance = get_balance(sender_id)

    if sender_balance < amount:
        return False, "You don't have enough Berries."

    update_bounty(
        sender_id,
        -amount
    )

    update_bounty(
        receiver_id,
        amount
    )

    log_transaction(
        sender_id,
        "trade_sent",
        -amount,
        receiver_id
    )

    log_transaction(
        receiver_id,
        "trade_received",
        amount,
        sender_id
    )

    return True, "Trade successful."


def raid(attacker_id, target_id):

    if attacker_id == target_id:
        return False, "You cannot raid yourself.", 0

    attacker_balance = get_balance(attacker_id)
    target_balance = get_balance(target_id)

    if target_balance <= 0:
        return False, "That pirate has no Berries to raid.", 0

    success = random.choice(
        [True, False]
    )

    if success:

        steal_amount = max(
            1,
            int(
                target_balance *
                random.uniform(0.10, 0.30)
            )
        )

        update_bounty(
            target_id,
            -steal_amount
        )

        update_bounty(
            attacker_id,
            steal_amount
        )

        log_transaction(
            attacker_id,
            "raid_success",
            steal_amount,
            target_id
        )

        log_transaction(
            target_id,
            "raided",
            -steal_amount,
            attacker_id
        )

        return True, "Raid successful!", steal_amount

    else:

        penalty = min(
            10,
            attacker_balance
        )

        if penalty > 0:

            update_bounty(
                attacker_id,
                -penalty
            )

            log_transaction(
                attacker_id,
                "raid_failed",
                -penalty,
                target_id
            )

        return False, "Raid failed!", penalty


SHOP = {
    "strawhat": {
        "price": 100,
        "description": "A legendary straw hat."
    },

    "jollyroger": {
        "price": 150,
        "description": "A pirate flag for your inventory."
    },

    "den-den-mushi": {
        "price": 250,
        "description": "A mysterious communication snail."
    },

    "sake": {
        "price": 300,
        "description": "A bottle for celebrating victories."
    }
}


def get_shop():
    return SHOP


def buy_item(user_id, item_name):

    item_name = item_name.lower()

    if item_name not in SHOP:

        return (
            False,
            "That item is not available in the shop."
        )

    price = SHOP[item_name]["price"]

    balance = get_balance(user_id)

    if balance < price:

        return (
            False,
            "You don't have enough Berries."
        )

    update_bounty(
        user_id,
        -price
    )

    add_inventory_item(
        user_id,
        item_name
    )

    log_transaction(
        user_id,
        "purchase",
        -price
    )

    return True, item_name
