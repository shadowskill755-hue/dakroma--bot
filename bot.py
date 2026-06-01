import telebot
import yt_dlp
import os
import requests
import math
import random
import xml.etree.ElementTree as ET
from datetime import datetime

BOT_TOKEN = "8940652640:AAHcdloBLHb-mmc9-qF67kZ3liUNMymk1lg"  # ← paste your token here

bot = telebot.TeleBot(BOT_TOKEN)
DOWNLOAD_DIR = "/sdcard/dakroma_bot/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ─────────────────────────────────────────
# 🖤 Dark Quotes Bank
# ─────────────────────────────────────────
QUOTES = [
    "🖤 The dark is not empty — it's full of everything you fear to face.",
    "🥀 Even broken flowers bloom in the dark.",
    "🖤 Pain is the ink. Scars are the art.",
    "🌑 The moon never apologizes for the dark side it carries.",
    "🖤 Be the storm they never saw coming.",
    "🥀 Not all who wander in darkness are lost — some are hunting.",
    "🖤 Silence is the loudest scream.",
    "🌹 A rose born in ash still blooms.",
    "🖤 The strongest souls carry wounds no one can see.",
    "🥀 Darkness isn't the absence of light — it's the birth of something stronger.",
    "🖤 I don't chase. I attract. What belongs to me will find me.",
    "🌑 They tried to bury me. They forgot I was a seed.",
    "🖤 Walk like you've already survived the worst.",
    "🥀 Even the devil was once an angel.",
    "🖤 Be feared. Not forgotten.",
    "🌹 A flower with broken leaves still carries its beauty.",
    "🖤 The night is darkest just before it becomes part of you.",
    "🥀 Cold hearts burn the brightest.",
]

# ══════════════════════════════════════════
# /start
# ══════════════════════════════════════════
@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, (
        "🖤 *Welcome to DAKROMA BOT* 🖤\n\n"
        "I'm your personal dark assistant.\n\n"
        "Type /help to see all commands."
    ), parse_mode="Markdown")

# ══════════════════════════════════════════
# /help
# ══════════════════════════════════════════
@bot.message_handler(commands=["help"])
def help_cmd(msg):
    bot.reply_to(msg, (
        "📋 *DAKROMA BOT — All Commands*\n\n"
        "🎵 /music `<song>` — Download & send MP3\n"
        "🔍 /search `<query>` — Search YouTube\n"
        "🎤 /lyrics `<artist - title>` — Get lyrics\n"
        "🌤️ /weather `<city>` — Live weather\n"
        "😂 /joke — Random joke\n"
        "🖤 /quote — Dark quote\n"
        "🔢 /calc `<expression>` — Calculator\n"
        "🪪 /id — Your Telegram ID info\n"
        "📰 /news — BBC top headlines\n"
        "🔁 /repeat `<text>` — Bot echoes you\n"
        "📡 /ping — Check bot is alive\n"
        "ℹ️ /info — About this bot"
    ), parse_mode="Markdown")

# ══════════════════════════════════════════
# /ping
# ══════════════════════════════════════════
@bot.message_handler(commands=["ping"])
def ping(msg):
    bot.reply_to(msg, "🟢 *DAKROMA BOT* is alive and running.", parse_mode="Markdown")

# ══════════════════════════════════════════
# /info
# ══════════════════════════════════════════
@bot.message_handler(commands=["info"])
def info(msg):
    bot.reply_to(msg, (
        "🖤 *DAKROMA BOT*\n"
        "━━━━━━━━━━━━━━━\n"
        "👤 Built by: @DAKROMA\n"
        "📱 Platform: Termux / Android\n"
        "🎵 Engine: yt-dlp + ffmpeg\n"
        "🌍 News: BBC RSS Feed\n"
        "🌤️ Weather: wttr.in\n"
        "🎤 Lyrics: lyrics.ovh\n"
        "🟢 Status: Online"
    ), parse_mode="Markdown")

# ══════════════════════════════════════════
# /music <song>
# ══════════════════════════════════════════
@bot.message_handler(commands=["music"])
def music(msg):
    query = msg.text.replace("/music", "").strip()
    if not query:
        bot.reply_to(msg, "⚠️ Usage: `/music <song name>`\nExample: `/music Blinding Lights`", parse_mode="Markdown")
        return

    wait_msg = bot.reply_to(msg, f"🔍 Searching for *{query}*...", parse_mode="Markdown")
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "default_search": "ytsearch1",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
        "noplaylist": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_data = ydl.extract_info(query, download=True)
            if "entries" in info_data:
                info_data = info_data["entries"][0]
            title = info_data.get("title", "Unknown")

        mp3_file = next(
            (os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".mp3")),
            None
        )
        if mp3_file:
            bot.edit_message_text(
                f"⬆️ Uploading *{title}*...",
                chat_id=wait_msg.chat.id,
                message_id=wait_msg.message_id,
                parse_mode="Markdown"
            )
            with open(mp3_file, "rb") as audio:
                bot.send_audio(
                    msg.chat.id, audio,
                    title=title,
                    caption=f"🎵 *{title}*\n🖤 via DAKROMA BOT",
                    parse_mode="Markdown"
                )
            os.remove(mp3_file)
            bot.delete_message(wait_msg.chat.id, wait_msg.message_id)
        else:
            bot.edit_message_text("❌ Download failed. Try a different song name.", chat_id=wait_msg.chat.id, message_id=wait_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", chat_id=wait_msg.chat.id, message_id=wait_msg.message_id)

# ══════════════════════════════════════════
# /search <query>
# ══════════════════════════════════════════
@bot.message_handler(commands=["search"])
def search(msg):
    query = msg.text.replace("/search", "").strip()
    if not query:
        bot.reply_to(msg, "⚠️ Usage: `/search <query>`", parse_mode="Markdown")
        return
    ydl_opts = {"default_search": "ytsearch5", "quiet": True, "skip_download": True, "noplaylist": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_data = ydl.extract_info(query, download=False)
            entries = info_data.get("entries", [])
            results = ""
            for i, entry in enumerate(entries[:5], 1):
                title = entry.get("title", "N/A")
                url = entry.get("webpage_url", "")
                duration = entry.get("duration", 0)
                mins, secs = divmod(duration, 60)
                results += f"{i}. [{title}]({url}) `{mins}:{secs:02d}`\n"
        bot.reply_to(msg, f"🎵 *Results for:* _{query}_\n\n{results}", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(msg, f"❌ Search failed: {str(e)}")

# ══════════════════════════════════════════
# /lyrics <artist - title>
# ══════════════════════════════════════════
@bot.message_handler(commands=["lyrics"])
def lyrics(msg):
    query = msg.text.replace("/lyrics", "").strip()
    if not query or " - " not in query:
        bot.reply_to(msg, (
            "⚠️ Usage: `/lyrics Artist - Song`\n"
            "Example: `/lyrics Eminem - Lose Yourself`"
        ), parse_mode="Markdown")
        return

    artist, title = query.split(" - ", 1)
    artist, title = artist.strip(), title.strip()
    wait_msg = bot.reply_to(msg, f"🎤 Fetching lyrics for *{title}* by *{artist}*...", parse_mode="Markdown")

    try:
        url = f"https://api.lyrics.ovh/v1/{requests.utils.quote(artist)}/{requests.utils.quote(title)}"
        resp = requests.get(url, timeout=10)
        data = resp.json()

        if "lyrics" in data:
            text = data["lyrics"]
            if len(text) > 3800:
                text = text[:3800] + "\n\n_... (truncated)_"
            bot.edit_message_text(
                f"🎤 *{title}* — _{artist}_\n\n{text}",
                chat_id=wait_msg.chat.id,
                message_id=wait_msg.message_id,
                parse_mode="Markdown"
            )
        else:
            bot.edit_message_text(
                "❌ Lyrics not found.\nTip: Use exact spelling → `/lyrics Juice WRLD - Lucid Dreams`",
                chat_id=wait_msg.chat.id,
                message_id=wait_msg.message_id,
                parse_mode="Markdown"
            )
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", chat_id=wait_msg.chat.id, message_id=wait_msg.message_id)

# ══════════════════════════════════════════
# /weather <city>
# ══════════════════════════════════════════
@bot.message_handler(commands=["weather"])
def weather(msg):
    city = msg.text.replace("/weather", "").strip()
    if not city:
        bot.reply_to(msg, "⚠️ Usage: `/weather <city>`\nExample: `/weather Lagos`", parse_mode="Markdown")
        return

    try:
        url = f"https://wttr.in/{requests.utils.quote(city)}?format=j1"
        resp = requests.get(url, timeout=10)
        data = resp.json()

        cur = data["current_condition"][0]
        area = data["nearest_area"][0]
        area_name = area["areaName"][0]["value"]
        country = area["country"][0]["value"]

        desc = cur["weatherDesc"][0]["value"]
        temp_c = cur["temp_C"]
        temp_f = cur["temp_F"]
        feels_c = cur["FeelsLikeC"]
        humidity = cur["humidity"]
        wind = cur["windspeedKmph"]
        visibility = cur["visibility"]

        # Pick emoji by condition
        condition = desc.lower()
        if "sun" in condition or "clear" in condition:
            icon = "☀️"
        elif "cloud" in condition:
            icon = "☁️"
        elif "rain" in condition or "drizzle" in condition:
            icon = "🌧️"
        elif "thunder" in condition or "storm" in condition:
            icon = "⛈️"
        elif "snow" in condition:
            icon = "❄️"
        elif "fog" in condition or "mist" in condition:
            icon = "🌫️"
        else:
            icon = "🌤️"

        bot.reply_to(msg, (
            f"{icon} *Weather — {area_name}, {country}*\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🌡️ Temp: *{temp_c}°C* / {temp_f}°F\n"
            f"🤔 Feels Like: *{feels_c}°C*\n"
            f"💧 Humidity: *{humidity}%*\n"
            f"💨 Wind: *{wind} km/h*\n"
            f"👁️ Visibility: *{visibility} km*\n"
            f"☁️ Condition: *{desc}*"
        ), parse_mode="Markdown")
    except Exception:
        bot.reply_to(msg, f"❌ City *{city}* not found. Check spelling.", parse_mode="Markdown")

# ══════════════════════════════════════════
# /joke
# ══════════════════════════════════════════
@bot.message_handler(commands=["joke"])
def joke(msg):
    try:
        resp = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=10)
        data = resp.json()
        bot.reply_to(msg,
            f"😂 *{data['setup']}*\n\n_{data['punchline']}_",
            parse_mode="Markdown"
        )
    except Exception:
        bot.reply_to(msg, "😂 *Why did the bot fail to get a joke?*\n\n_Because even humor has dark days._", parse_mode="Markdown")

# ══════════════════════════════════════════
# /quote
# ══════════════════════════════════════════
@bot.message_handler(commands=["quote"])
def quote_cmd(msg):
    bot.reply_to(msg, random.choice(QUOTES))

# ══════════════════════════════════════════
# /calc <expression>
# ══════════════════════════════════════════
@bot.message_handler(commands=["calc"])
def calc(msg):
    expr = msg.text.replace("/calc", "").strip()
    if not expr:
        bot.reply_to(msg, (
            "⚠️ Usage: `/calc <expression>`\n"
            "Examples:\n"
            "`/calc 25 * 4 + 10`\n"
            "`/calc (100 / 5) ** 2`\n"
            "`/calc 999 % 7`"
        ), parse_mode="Markdown")
        return
    try:
        allowed = set("0123456789+-*/(). %**")
        if not all(c in allowed for c in expr.replace(" ", "")):
            bot.reply_to(msg, "❌ Only numbers and `+ - * / ( ) % **` are allowed.", parse_mode="Markdown")
            return
        result = eval(expr, {"__builtins__": {}}, {"math": math})
        # Round long floats
        if isinstance(result, float):
            result = round(result, 8)
        bot.reply_to(msg, f"🔢 `{expr}`\n= *{result}*", parse_mode="Markdown")
    except ZeroDivisionError:
        bot.reply_to(msg, "❌ Division by zero is not possible.", parse_mode="Markdown")
    except Exception:
        bot.reply_to(msg, "❌ Invalid expression. Check your syntax.", parse_mode="Markdown")

# ══════════════════════════════════════════
# /id
# ══════════════════════════════════════════
@bot.message_handler(commands=["id"])
def get_id(msg):
    u = msg.from_user
    c = msg.chat
    full_name = f"{u.first_name} {u.last_name or ''}".strip()
    username = f"@{u.username}" if u.username else "None"

    bot.reply_to(msg, (
        f"🪪 *Your Telegram Info*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 Name: *{full_name}*\n"
        f"🔖 Username: {username}\n"
        f"🆔 User ID: `{u.id}`\n"
        f"🌐 Language: {u.language_code or 'Unknown'}\n\n"
        f"💬 *Chat Info*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🆔 Chat ID: `{c.id}`\n"
        f"📂 Type: *{c.type}*"
    ), parse_mode="Markdown")

# ══════════════════════════════════════════
# /news
# ══════════════════════════════════════════
@bot.message_handler(commands=["news"])
def news(msg):
    wait_msg = bot.reply_to(msg, "📰 Fetching latest headlines...", parse_mode="Markdown")
    try:
        resp = requests.get("https://feeds.bbci.co.uk/news/rss.xml", timeout=10)
        root = ET.fromstring(resp.content)
        items = root.findall(".//item")[:7]

        headlines = ""
        for i, item in enumerate(items, 1):
            title_el = item.find("title")
            link_el = item.find("link")
            t = title_el.text if title_el is not None else "N/A"
            l = link_el.text if link_el is not None else "#"
            headlines += f"{i}\\. [{t}]({l})\n"

        time_str = datetime.now().strftime("%d %b %Y, %H:%M")
        bot.edit_message_text(
            f"📰 *BBC News — Top Headlines*\n"
            f"━━━━━━━━━━━━━━━\n"
            f"{headlines}\n"
            f"🕐 Updated: {time_str}",
            chat_id=wait_msg.chat.id,
            message_id=wait_msg.message_id,
            parse_mode="MarkdownV2"
        )
    except Exception as e:
        bot.edit_message_text(f"❌ Failed to load news: {str(e)}", chat_id=wait_msg.chat.id, message_id=wait_msg.message_id)

# ══════════════════════════════════════════
# /repeat <text>
# ══════════════════════════════════════════
@bot.message_handler(commands=["repeat"])
def repeat(msg):
    text = msg.text.replace("/repeat", "").strip()
    if not text:
        bot.reply_to(msg, "⚠️ Usage: `/repeat <your text>`\nExample: `/repeat DAKROMA is the goat`", parse_mode="Markdown")
        return
    bot.reply_to(msg, f"🔁 {text}")

# ══════════════════════════════════════════
# Unknown command handler
# ══════════════════════════════════════════
@bot.message_handler(func=lambda msg: msg.text and msg.text.startswith("/"))
def unknown(msg):
    bot.reply_to(msg, "❓ Unknown command. Type /help to see all commands.")

# ══════════════════════════════════════════
# Start bot
# ══════════════════════════════════════════
print("🖤 DAKROMA BOT is running...")
bot.infinity_polling()
