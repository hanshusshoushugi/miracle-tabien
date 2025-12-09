import requests
import streamlit as st
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

CORRECT_KEY_INPUT_TEXT = "โปรดกรอก Key ที่ถูกต้อง"
URL = "https://miracle-tabien.streamlit.app/data"
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
    st.header(
        anchor = False,
        body = text,
        divider = False,
        help = None,
        text_alignment = "left",
        width = "stretch"
    )
    return None

if st.button("Data"):
    try:
        response = requests.post(
            json = {
                "url" : "https://www.ministryoftesting.com/software-testing-glossary/test"
            },
            url = URL
        )
        response.raise_for_status()
        st.write("Success")
    except Exception as exception:
        st.error(exception)

if "key" in st.session_state:
    with center, st.empty():
        while True:
            try:
                response = requests.get(URL)

                # เช็ค response status ถ้า error ให้แสดงข้อความว่า กำลังรอ QR Code
                response.raise_for_status()
                st.write("Test")
                st.session_state.url = response.json().url
                st.write(st.session_state.url)
            except Exception as exception:
                pass
            
            # เช็คว่ามี url บันทึกไว้ใน session หรือไม่
            if "url" in st.session_state:
                try:         
                    response = requests.get(st.session_state.url)

                    # เช็ค response status ถ้า error ให้แสดงข้อความว่า กำลังรอ QR Code
                    response.raise_for_status()

                    # ค้นหา component ที่เป็น tag <img> ทั้งหมดใน response
                    img_tags = BeautifulSoup(response.content, 'html.parser').find_all('img')

                    # นำรูปแรกสุด (รูป QR Code) ที่เจอมาแสดง ถ้าไม่เจอรูปให้แสดงข้อความว่า กำลังรอ QR Code
                    if(len(img_tags) > 0):
                        src = img_tags[0].get('src')
                        if src:
                            absolute_src = urljoin(url, src)
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
            else:
                SHOW_TEXT(WAITING_TEXT[int((time.perf_counter() - start_time) * WAITING_TEXT_SPEED) % WAITING_TEXT_LENGTH])
else:
    SHOW_TEXT(CORRECT_KEY_INPUT_TEXT)
