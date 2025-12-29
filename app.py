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


def startup_banner():
    print("========================================")
    print(" PHONE NUMBER LOOKUP TOOL (USA)")
    print(" ADL APPLICATIONS PREVIEW")
    print(" A FREE PRODUCT BY ADL | ASTRA CONSULTANCY | INFURATECHNOLOGIES")
    print("========================================\n")


def lookup_number(phone_number):
    base_url = "https://puck.nether.net/npa-nxx/new-lookup.cgi"
    query = urlencode({"number": phone_number})
    url = f"{base_url}?{query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; StreamlabsBot/1.0)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close"
    }

    request = Request(url, headers=headers)

    with urlopen(request, timeout=15) as response:
        html = response.read().decode("utf-8", errors="ignore")

    parser = LookupParser()
    parser.feed(html)

    return {
        "number": phone_number,
        "city": parser.city or "UNKNOWN",
        "carrier": parser.carrier or "UNKNOWN"
    }


if __name__ == "__main__":
    try:
        startup_banner()

        number = input("Enter phone number (digits only): ").strip()

        if not number.isdigit():
            print("ERROR: Phone number must contain digits only")
        else:
            result = lookup_number(number)

            print("\nSTREAMLABS LOOKUP RESULT")
            print("------------------------")
            print(f"Number  : {result['number']}")
            print(f"City    : {result['city']}")
            print(f"Carrier : {result['carrier']}")

            print("\n----------------------------------------")
            print("A FREE PRODUCT BY ADL | ASTRA CONSULTANCY | INFURATECHNOLOGIES")
            print("For higher volume usage, contact us on LinkedIn:")
            print("https://www.linkedin.com/in/aditya-ladva/")
            print()
            print("For proper tool development or custom product orders,")
            print("mail us at: productbyadl@gmail.com")
            print("or DM us on LinkedIn.")
            print("----------------------------------------")

    except Exception as e:
        print("Lookup failed:", str(e))
