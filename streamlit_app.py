import requests
import streamlit as st

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
