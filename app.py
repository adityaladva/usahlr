from urllib.request import Request, urlopen
from urllib.parse import urlencode
from html.parser import HTMLParser


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
    url = "https://puck.nether.net/npa-nxx/new-lookup.cgi?" + urlencode({"number": phone_number})

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; StreamlabsChatbot/1.0)"
    }

    req = Request(url, headers=headers)
    html = urlopen(req, timeout=10).read().decode("utf-8", "ignore")

    parser = LookupParser()
    parser.feed(html)

    return parser.city or "UNKNOWN", parser.carrier or "UNKNOWN"


def Init():
    pass


def Execute(data):
    if not data.IsChatMessage():
        return

    msg = data.Message.strip()

    # COMMAND = !<10-digit-number>
    if not (msg.startswith("!") and len(msg) == 11 and msg[1:].isdigit()):
        return

    phone_number = msg[1:]

    city, carrier = lookup_number(phone_number)

    data.SendChatMessage(
        "📞 Phone Lookup\n"
        f"Number: {phone_number} | City: {city} | Carrier: {carrier}\n"
        "A FREE PRODUCT BY ADL | ASTRA CONSULTANCY | INFURATECHNOLOGIES\n"
        "Custom tools: productbyadl@gmail.com | linkedin.com/in/aditya-ladva"
    )


def Tick():
    pass
