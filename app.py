import requests
from bs4 import BeautifulSoup

def lookup_number(number):
    url = f"https://puck.nether.net/npa-nxx/new-lookup.cgi?number={number}"
    r = requests.get(url, timeout=10)

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(separator="\n")

    data = {
        "number": number,
        "country": "USA" if "USA" in text else "UNKNOWN",
        "npa_nxx": None,
        "city": None,
        "carrier": None,
    }

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("NPA-NXX"):
            data["npa_nxx"] = line.replace("NPA-NXX", "").strip()

        elif line.startswith("City:"):
            data["city"] = line.replace("City:", "").strip() or "NOT AVAILABLE"

        elif line.startswith("Telco:"):
            data["carrier"] = line.replace("Telco:", "").strip() or "NOT AVAILABLE"

    return data


# DEMO
if __name__ == "__main__":
    result = lookup_number("2031212212")
    print(result)
