import requests
import streamlit as st

URL = "https://miracle-tabien.streamlit.app"

# เช็คว่ามี key กรอกเข้ามาไหม
if "key" in st.query_params:
    # บันทึก key ล่าสุด
    st.session_state.key = st.query_params.get("key")
    
    try:
        response = requests.get(URL)
        st.write("Test1")
        # เช็ค response status ถ้า error ให้แสดงข้อความว่า กำลังรอ QR Code
        response.raise_for_status()
        st.write("Test2")
        st.write(response.json())
        st.session_state.url = response.json().url
        st.write("Success")
        st.write(st.session_state.url)
    except Exception as exception:
        st.write(exception)
        pass

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

