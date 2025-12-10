from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler, HTTPServer
from streamlit_gsheets import GSheetsConnection
from urllib.parse import urljoin
import requests
import streamlit as st
import time

CORRECT_KEY_INPUT_TEXT = "โปรดกรอก Key ที่ถูกต้อง"
WAITING_TEXT = ["กำลังรอ QR Code   ", "กำลังรอ QR Code .  ", "กำลังรอ QR Code .. ", "กำลังรอ QR Code ..."]
WAITING_TEXT_LENGTH = len(WAITING_TEXT)
WAITING_TEXT_SPEED = 1.25

left, center, right = st.columns(
    border = False,
    gap = "small",
    spec = [1, 6, 1],
    vertical_alignment = "center",
    width = "stretch"
)
start_time = time.perf_counter()
waiting_indicator = 0

# แสดงข้อความ กำลังรอ QR Code
def SHOW_TEXT(text):
    st.subheader(
        anchor = False,
        body = text,
        divider = False,
        help = None,
        text_alignment = "left",
        width = "stretch"
    )
    return None

# ถ้าไม่มี key ใน url ให้แสดงข้อความ "โปรดกรอก Key ที่ถูกต้อง"
if "key" not in st.query_params:
    SHOW_TEXT(CORRECT_KEY_INPUT_TEXT)
else:
    try:
        # ดึงข้อมูลจาก Google Sheet
        data_frame = st.connection(
            "gsheets",
            type = GSheetsConnection
        ).read(
            nrows = 2,
            ttl = "600",
            usecols = [0, 1],
            worksheet = "Sheet"
        )
        key = ""

        for index, data_row in data_frame.iterrows():
            key = data_row["key"]
            
            # ถ้า key เป็น float ให้แปลงเป็น integer
            if type(key) == float:
                key = int(key)
            
            # เช็ค key เทียบกับ key ใน Google Sheet
            if str(key) == st.query_params.get("key"):
                st.session_state.key = key
                st.session_state.url = data_row["url"]
                break
    except Exception as exception:
        pass

    # ถ้า key ไม่ตรงกับใน Google Sheet ให้แสดงข้อความ "โปรดกรอก Key ที่ถูกต้อง"
    if "key" not in st.session_state:
        SHOW_TEXT(CORRECT_KEY_INPUT_TEXT)
    else:
        with center, st.empty():
            while True:
                try:
                    response = requests.get(url = st.session_state.url)

                    # เช็ค response status ถ้า error ให้แสดงข้อความว่า กำลังรอ QR Code
                    response.raise_for_status()

                    # ค้นหา component ที่เป็น tag <img> ทั้งหมดใน response
                    img_tags = BeautifulSoup(response.content, 'html.parser').find_all('img')

                    # นำรูปแรกสุด (รูป QR Code) ที่เจอมาแสดง ถ้าไม่เจอรูปให้แสดงข้อความว่า กำลังรอ QR Code
                    if(len(img_tags) > 0):
                        src = img_tags[0].get('src')
                        if src:
                            absolute_src = urljoin(st.session_state.url, src)
                            st.image(
                                caption = "โปรดสแกน QR Code",
                                channels = "RGB",
                                clamp = False,
                                image = absolute_src,
                                output_format = "auto",
                                width = "content"
                            )
                    else:
                        SHOW_TEXT(WAITING_TEXT[int((time.perf_counter() - start_time) * WAITING_TEXT_SPEED) % WAITING_TEXT_LENGTH])
                except Exception as exception:
                    SHOW_TEXT(WAITING_TEXT[int((time.perf_counter() - start_time) * WAITING_TEXT_SPEED) % WAITING_TEXT_LENGTH])
                    pass
