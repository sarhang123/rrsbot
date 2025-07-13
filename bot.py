import feedparser
import time
import telegram
from config import BOT_TOKEN, RSS_URL, CHANNEL_ID

bot = telegram.Bot(token=BOT_TOKEN)
sent_links = set()

def get_feed():
    return feedparser.parse(RSS_URL)

def format_entry(entry):
    message = f"<b>{entry.get('title', '')}</b>\n\n{entry.get('summary', '')}"
    return message

while True:
    feed = get_feed()
    for entry in feed.entries:
        link = entry.get('link')
        if link and link not in sent_links:
            message = format_entry(entry)
            if 'media_content' in entry:
                img_url = entry.media_content[0].get('url')
                if img_url:
                    try:
                        bot.send_photo(chat_id=CHANNEL_ID, photo=img_url, caption=entry.get('title', ''), parse_mode="HTML")
                    except:
                        bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="HTML")
                else:
                    bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="HTML")
            else:
                bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="HTML")
            sent_links.add(link)
    time.sleep(60)
