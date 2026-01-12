import streamlit as st
import hashlib

st.set_page_config(layout="wide")
st.title("🏆 Darts AI Coach Pro")

# ✅ УНИКАЛЬНЫЙ KEY по хэшу файла
video_file = st.file_uploader("📹 Загрузи видео броска", 
                              type=['mp4','mov','avi'], 
                              key="unique_video")

if video_file is not None:
    # ✅ ХЭШ файла для уникальных виджетов
    file_hash = hashlib.md5(video_file.read()).hexdigest()
    video_file.seek(0)  # Reset pointer
    
    st.video(video_file)
    st.success(f"✅ Видео: {video_file.name}")
    
    # ✅ УНИКАЛЬНЫЕ КЛЮЧИ по хэшу = СБРОС при новом видео
    col1, col2, col3 = st.columns(3)
    
    with col1:
        angle = st.slider("🎯 Локоть релиз", 60, 120, 98, 
                         key=f"angle_{file_hash}")
        st.metric("PDC эталон", f"{angle}°", "95-105°")
    
    with col2:
        speed = st.slider("⚡ Скорость кисти", 6.0, 12.0, 9.8,
                         key=f"speed_{file_hash}")
        st.metric("PDC эталон", f"{speed:.1f} м/с", "9-10.5")
    
    with col3:
        stab = st.slider("🧠 Стабильность головы", 0.5, 5.0, 1.2,
                        key=f"stab_{file_hash}")
        st.metric("PDC эталон", f"{stab:.1f} см", "<1.5")
    
    # Рекомендации (обновляются)
    st.markdown("### 🎯 Твой план:")
    if angle < 90:
        st.error("🔴 **СТЕНА**: Локоть 10см от стены")
    if speed < 8.5:
        st.error("⚡ **МЯЧИК**: Теннисный мячик")
    if stab > 2:
        st.error("🧠 **ЛАЗЕР**: Лист на лоб")
        
    st.success("✅ Анализ обновлён!")
    
    # ✅ Кнопка для следующего видео
    if st.button("➕ Следующий игрок", key="next_player"):
        st.rerun()
else:
    st.info("👆 Загрузи первое видео!")
