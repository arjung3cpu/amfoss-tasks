# 🏴‍☠️ Task 07 - Dunk Memer Discord Bot

## 🍖 Berry Broker - Pirate Economy Discord Bot

A Discord bot based on a fictional pirate economy.

Every Discord member is treated as a pirate with a Berry wallet.
Users can earn, trade, spend and raid Berries while interacting with
the bot through Discord commands.

---

## ✨ Features

The bot supports the following commands:

| Command | Description |
|---|---|
| `!bounty` | Check current Berry balance |
| `!setsail` | Claim a random daily Berry reward |
| `!trade @user <amount>` | Transfer Berries to another pirate |
| `!logpose` | Get random One Piece information using an API |
| `!shop` | Display items available for purchase |
| `!inventory` | Display owned items |
| `!buy <item>` | Purchase an item using Berries |
| `!worstgeneration` | Display the top 5 richest pirates |
| `!raid @user` | Attempt a chance-based raid |

---

## 🗄️ Database

SQLite is used for persistent storage through Python's built-in
`sqlite3` module.

The database stores:

- User IDs
- Usernames
- Berry balances
- Inventory items
- Transaction history

The database allows balances and purchases to remain available even
after restarting the bot.

---

## 📁 Project Structure

```text
Task-07/
│
├── main.py
├── commands.py
├── economy.py
├── database.py
├── onepiece_api.py
├── requirements.txt
├── README.md
│
└── screenshots/
    ├── task7-bounty-setsail.png
    ├── task7-trade.png
    ├── task7-logpose.png
    ├── task7-buy.png
    ├── task7-worstgeneration.png
    └── task7-raid.png
