import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="USA HLR Demo", layout="centered")

st.markdown("""
## USA HLR / NPA-NXX Validation Demo  
**ASTRA CONSULTANCY | INFURA TECHNOLOGIES**  

Free Product Sample – USA Phone Number Validation  
---
""")

# INPUT
number = st.text_input("Enter USA Phone Number", placeholder="2031212212")

def lookup_number(num):
    url = f"https://puck.nether.net/npa-nxx/new-lookup.cgi?number={num}"
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
            value = line.replace("City:", "").strip()
            if value:
                result["City"] = value

        elif line.startswith("Telco:"):
            value = line.replace("Telco:", "").strip()
            if value:
                result["Carrier"] = value

    return result

# ACTION
if st.button("Validate Number"):
    if not number:
        st.warning("Please enter a phone number")
    else:
        with st.spinner("Validating number..."):
            data = lookup_number(number)

        st.success("Validation Complete")

        st.write("**Country:**", data["Country"])
        st.write("**NPA-NXX:**", data["NPA-NXX"])
        st.write("**City:**", data["City"])
        st.write("**Carrier:**", data["Carrier"])

        st.markdown("""
        ---
        **A FREE PRODUCT BY ADL | ASTRA CONSULTANCY | INFURATECHNOLOGIES**  

        For higher volume HLR, phone validation, or enterprise use cases,  
        contact us on LinkedIn:  
        https://www.linkedin.com/in/aditya-ladva/
        """)
