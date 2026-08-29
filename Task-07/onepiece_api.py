import random
import requests


BASE_URL = "https://onepieceapi.com/api"


def get_localized_name(value):

    if not value:
        return "Unknown"

    if isinstance(value, dict):

        return (
            value.get("en")
            or value.get("romaji")
            or value.get("jp")
            or "Unknown"
        )

    return str(value)


def get_random_character():

    response = requests.get(
        f"{BASE_URL}/characters",
        params={
            "page": 1,
            "limit": 100
        },
        timeout=10
    )

    response.raise_for_status()

    characters = response.json()

    if not characters:
        return None

    return random.choice(characters)


def get_random_devil_fruit():

    response = requests.get(
        f"{BASE_URL}/devil-fruits",
        params={
            "page": 1,
            "limit": 100
        },
        timeout=10
    )

    response.raise_for_status()

    fruits = response.json()

    if not fruits:
        return None

    return random.choice(fruits)


def get_character_bounty(character):

    bounties = character.get("bounties", [])

    if not bounties:
        return "Unknown"

    active_bounties = [
        bounty
        for bounty in bounties
        if bounty.get("is_active") is True
    ]

    if active_bounties:

        amount = active_bounties[0].get("amount")

        if amount is not None:
            return amount

    amount = bounties[0].get("amount")

    if amount is not None:
        return amount

    return "Unknown"


def get_logpose():

    character = get_random_character()
    fruit = get_random_devil_fruit()

    if character is None or fruit is None:
        return None

    character_name = get_localized_name(
        character.get("name")
    )

    fruit_name = get_localized_name(
        fruit.get("name")
    )

    model_name = get_localized_name(
        fruit.get("model")
    )

    fruit_type = fruit.get("type") or "Unknown"

    bounty = get_character_bounty(character)

    return {
        "character": character_name,
        "bounty": bounty,
        "fruit": fruit_name,
        "model": model_name,
        "type": fruit_type
    }
