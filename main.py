import streamlit as st
import os

# 🎯 ФИКС ПОРТА ДЛЯ RENDER
port = int(os.environ.get("PORT", 8501))

st.set_page_config(layout="wide", page_title="Darts AI Coach Pro")
st.title("🏆 Darts AI Coach Pro")

video_file = st.file_uploader("📹 Загрузи видео броска", type=['mp4','mov'])

if video_file:
    st.video(video_file)
    st.success(f"✅ Видео: {video_file.name}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        angle = st.slider("🎯 Локоть", 60, 120, 98)
        st.metric("PDC", f"{angle}°", "95-105°")
    with col2:
        speed = st.slider("⚡ Скорость", 6.0, 12.0, 9.8)
        st.metric("PDC", f"{speed:.1f} м/с", "9-10.5")
    with col3:
        stab = st.slider("🧠 Стабильность", 0.5, 5.0, 1.2)
        st.metric("PDC", f"{stab:.1f} см", "<1.5")
    
    if angle < 90:
        st.error("🔴 **СТЕНА**: Локоть у стены 10см")
    st.success("🎯 Готово!")
else:
    st.info("👆 Загрузи видео!")
