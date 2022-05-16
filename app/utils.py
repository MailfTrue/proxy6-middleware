import httpx
import threading
from django.conf import settings


def send_tg_notify(text):
    print("sending...", text)
    try:
        thread = threading.Thread(target=httpx.post,
                                  args=[f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"],
                                  kwargs={"data": {"chat_id": settings.TG_CHAT_ID, "text": text}})
        thread.start()
    except httpx.HTTPError:
        print("cannot send tg notify")

