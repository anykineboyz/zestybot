from flask import Flask, request
import requests
import os
import re
import random

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------

BOT_ID = os.environ.get("BOT_ID")

# -----------------------------
# NIKO BANNED WORDS
# -----------------------------

NIKO_ONLY_BANNED_WORDS = [
    "eva",
    "rene",
    "brendon",
    "drill sergeant",
    "clanker",
    "shh",
    "hehe",
    "haha",
    "die",
    "kill",
    "stupid",
    "dumb",
    "mom",
    "dad",
    "shhh",
    "idiot",
    "ass",
    "shut",
    "uncle",
    "aunty",
    "what",
    "no",
    "stop",
    "fine"
]

# -----------------------------
# STORAGE
# -----------------------------

niko_message_count = 0

# -----------------------------
# SEND MESSAGE
# -----------------------------

def send_message(text):

    if not BOT_ID:
        print("BOT_ID missing")
        return

    try:
        requests.post(
            "https://api.groupme.com/v3/bots/post",
            json={
                "bot_id": BOT_ID,
                "text": text
            },
            timeout=10
        )

    except Exception as error:
        print(
            "Error sending GroupMe message:",
            error
        )

# -----------------------------
# WEBHOOK
# -----------------------------

@app.route("/", methods=["POST"])
def webhook():

    global niko_message_count

    data = request.json

    if not data:
        return "ok", 200

    # Ignore bot messages
    if data.get("sender_type") == "bot":
        return "ok", 200

    name = data.get(
        "name",
        "Unknown"
    )

    name_lower = name.lower()

    message = data.get(
        "text",
        ""
    ).strip()

    message_lower = message.lower()

    # -----------------------------
    # ONLY WATCH NIKO
    # -----------------------------

    if "niko" not in name_lower:
        return "ok", 200

    # -----------------------------
    # COUNT NIKO'S MESSAGES
    # -----------------------------

    niko_message_count += 1

    print(
        f"Niko message #{niko_message_count}"
    )

    # -----------------------------
    # BANNED WORD CHECK
    # -----------------------------

    for word in NIKO_ONLY_BANNED_WORDS:

        if re.search(
            rf"\b{re.escape(word)}\b",
            message_lower
        ):

            send_message(
                f"NIKKOOOO😭 WATCH YOUR LANGUAGE!"
            )

            break

    # -----------------------------
    # EVERY 3RD MESSAGE
    # -----------------------------

    if niko_message_count % 7 == 0:

        zesty_messages = [

            "NIKOOOO 😭💅 YOU'RE MY FAVORITE SOURCE OF CHAOS!",

            "NIKO!!! ✨ WHY ARE YOU ALWAYS THIS ICONIC?! SLAYY💅",

            "BESTIEEEE 😭💅 I CAN'T HANDLE YOU!",

            "NIKO, YOU'RE ABSOLUTELY SERVING CHAOS TODAY GURLL 💅✨",

            "OMG NIKO 😭 YOU'RE REALLY TRYING TO BREAK THE CHAT AGAIN QUEEN! 💅",

            "NIKOOOO 💅 THE DRAMA NEVER ENDS WITH YOU BABE!",

            "BESTIE, PLEASE 😭 SAVE SOME ATTENTION FOR EVERYONE ELSE! 💅",

            "NIKO ✨ YOU'VE GOT THE WHOLE CHAT LOSING IT GURL! 💅",

            "NOT QUEEN NIKO BEING THE CENTER OF ATTENTION AGAIN 😭💅",

            "NIKO BESTIE!!! YOU KNOW YOU'RE TOO MUCH, RIGHT?! 💅😂",

            "BESTIEEEE 💅 WHAT WOULD WE DO WITHOUT YOUR CHAOS?!",

            "NIKO 😭 YOU REALLY KNOW HOW TO MAKE AN ENTRANCE, SLAYY!💅",

            "OMG NIKO ✨ YOU'RE SOMETHING ELSE QUEEN!💅",

            "NIKO 💅 PLEASE, THE GROUP CHAT ISN'T READY FOR THIS ENERGY GURL!",

            "BESTIE 😭 YOU'RE MAKING THIS CHAT WAY TOO ENTERTAINING!💅"

        ]

        send_message(
            random.choice(zesty_messages)
        )

    return "ok", 200


# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
