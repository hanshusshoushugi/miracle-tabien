from flask import Flask, request
import requests
import streamlit as st

URL = "https://miracle-tabien.streamlit.app/data"

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def get_data_from_post_request():
    if request.is_json:
        data = request.json
        st.write("json")
    else:
        data = request.form
        st.write("form")
    st.session_state.url = data.url
    return None

if st.button("json"):
    try:
        response = requests.post(
            json = { "url": "https://www.ministryoftesting.com/software-testing-glossary/test" },
            url = URL
        )
        response.raise_for_status()
    except Exception as exception:
        st.error(exception)

if st.button("data"):
    try:
        response = requests.post(
            data = { "url": "https://www.ministryoftesting.com/software-testing-glossary/test" },
            url = URL
        )
        response.raise_for_status()
    except Exception as exception:
        st.error(exception)

# บันทึก key ล่าสุดเมื่อมี Key กรอกเข้ามา
if "key" in st.query_params:
    st.session_state.key = st.query_params.get("key")

# สร้าง Page ย่อย
about_me = st.Page(
    default = False,
    icon = ":material/person:",
    page = "about_me.py",
    title = "About me",
    url_path = None
)
qr_code = st.Page(
    default = True,
    icon = ":material/qr_code_2:",
    page = "qr_code.py",
    title = "QR Code",
    url_path = None
)

# รัน Navigation ที่ใส่ Page ย่อยเข้าไปแล้ว
st.navigation(
    expanded = True,
    pages = [
        qr_code,
        about_me
    ],
    position = "sidebar"
).run()
