import streamlit as st

# เปลี่ยนชื่อ เปลี่ยนที่อยู่ลิงค์ได้
name = "Miracle Tabien - รับจองเลขทะเบียนรถยนต์ - มอเตอร์ไซค์"
url = "https://www.facebook.com/people/Miracle-Tabien-%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%88%E0%B8%AD%E0%B8%87%E0%B9%80%E0%B8%A5%E0%B8%82%E0%B8%97%E0%B8%B0%E0%B9%80%E0%B8%9A%E0%B8%B5%E0%B8%A2%E0%B8%99%E0%B8%A3%E0%B8%96%E0%B8%A2%E0%B8%99%E0%B8%95%E0%B9%8C-%E0%B8%A1%E0%B8%AD%E0%B9%80%E0%B8%95%E0%B8%AD%E0%B8%A3%E0%B9%8C%E0%B9%84%E0%B8%8B%E0%B8%84%E0%B9%8C/61583616704853/#"

# ปรับขนาดข้อความได้ 3 ระดับ title, header, subheader
st.subheader(
    anchor = False,
    body = f"[{name}](%s)" % url,
    divider = False,
    help = None,
    text_alignment = "left",
    width = "stretch"
)
