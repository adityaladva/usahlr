# =========================================
# Phone Number Lookup Tool (USA)
# Auto-detects phone numbers from chat
#
# A FREE PRODUCT BY:
# ADL | ASTRA CONSULTANCY | INFURATECHNOLOGIES
#
# For higher volume usage:
# https://www.linkedin.com/in/aditya-ladva/
#
# Custom tools / product orders:
# productbyadl@gmail.com
# =========================================

from urllib.request import Request, urlopen
from urllib.parse import urlencode
from html.parser import HTMLParser
import re


class LookupParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.city = None
        self.carrier = None

    def handle_data(self, data):
        data = data.strip()
        if data.startswith("City:"):
            self.city = data.replace("City:", "").strip()
        elif data.startswith("Telco:"):
            self.carrier = data.replace("Telco:", "").strip()


def lookup_number(phone_number):
    base_url = "https://puck.nether.net/npa-nxx/new-lookup.cgi"
    query = urlencode({"number": phone_number})
    url = f"{base_url}?{query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; StreamlabsChatbot/1.0)",
        "Accept": "text/html",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close"
    }

    request = Request(url, headers=headers)

    with urlopen(request, timeout=15) as response:
        html = response.read().decode("utf-8", errors="ignore")

    parser = LookupParser()
    parser.feed(html)

    return parser.city or "UNKNOWN", parser.carrier or "UNKNOWN"


# ================= REQUIRED BY STREAMLABS =================

def Init():
    return


def Execute(data):
    if not data.IsChatMessage():
        return

    message = data.Message.strip()

    # Detect 10-digit phone number anywhere in message
    match = re.search(r"\b\d{10}\b", message)
    if not match:
        return

    phone_number = match.group()

    try:
        city, carrier = lookup_number(phone_number)

        response = (
            "📞 Phone Lookup Result\n"
            "────────────────────────\n"
            f"Number  : {phone_number}\n"
            f"City    : {city}\n"
            f"Carrier : {carrier}\n"
            "────────────────────────\n"
            "A FREE PRODUCT BY ADL | ASTRA CONSULTANCY | INFURATECHNOLOGIES\n"
            "For higher volume usage:\n"
            "linkedin.com/in/aditya-ladva\n"
            "Custom tools / product orders:\n"
            "productbyadl@gmail.com"
        )

        data.SendChatMessage(response)

    except Exception:
        data.SendChatMessage("⚠️ Phone lookup failed. Please try again later.")


def Tick():
    return
