import streamlit as st
import requests
from bs4 import BeautifulSoup

# ------------------ PAGE SETUP ------------------
st.set_page_config(page_title="USA HLR Demo", layout="centered")

st.markdown(
    """
    <h2>USA HLR / NPA-NXX Validation Demo</h2>
    <p><b>ASTRA CONSULTANCY | INFURA TECHNOLOGIES</b></p>
    <p>Free Phone Validation Product Sample</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ------------------ INPUTS (LIKE SMTP APP) ------------------
phone_number = st.text_input(
    "Enter USA Phone Number",
    placeholder="2031212212"
)

# ------------------ LOOKUP FUNCTION ------------------
def lookup_number(number):
    url = f"https://puck.nether.net/npa-nxx/new-lookup.cgi?number={number}"
    r = requests.get(url, timeout=10)

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(separator="\n")

    result = {
        "Country": "USA" if "USA" in text else "Unknown",
        "NPA-NXX": "Not available",
        "City": "Not available",
        "Carrier": "Not available",
    }

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("NPA-NXX"):
            result["NPA-NXX"] = line.replace("NPA-NXX", "").strip()

        elif line.startswith("City:"):
            val = line.replace("City:", "").strip()
            if val:
                result["City"] = val

        elif line.startswith("Telco:"):
            val = line.replace("Telco:", "").strip()
            if val:
                result["Carrier"] = val

    return result

# ------------------ ACTION BUTTON ------------------
if st.button("Validate Number"):
    if not phone_number:
        st.warning("Please enter a phone number")
    else:
        with st.spinner("Validating number..."):
            data = lookup_number(phone_number)

        st.success("Validation Result")

        st.write("**Country:**", data["Country"])
        st.write("**NPA-NXX:**", data["NPA-NXX"])
        st.write("**City:**", data["City"])
        st.write("**Carrier / Telco:**", data["Carrier"])

        st.markdown(
            """
            ---
            **A FREE PRODUCT BY ADL | ASTRA CONSULTANCY | INFURATECHNOLOGIES**

            For higher volume phone validation, HLR lookups,  
            or enterprise integrations, contact us on LinkedIn:  
            https://www.linkedin.com/in/aditya-ladva/
            """
        )
