import streamlit as st
import hashlib
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🏆 Darts AI Coach Pro")

# ✅ СИСТЕМА ПОДПИСК (session_state)
if 'plan' not in st.session_state: st.session_state.plan = 'TRIAL'
if 'uploads_count' not in st.session_state: st.session_state.uploads_count = 0
if 'trial_end' not in st.session_state: st.session_state.trial_end = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

# Тарифный план (sidebar)
st.sidebar.header("💎 Твой тариф")
plan = st.sidebar.selectbox("Тариф", 
    ["🆓 TRIAL (3 видео)", "💎 HOBBY (199₽/мес)", "🏆 PRO (499₽/мес)"], 
    index=['TRIAL', 'HOBBY', 'PRO'].index(st.session_state.plan))

# ✅ ЛИМИТЫ ПО ТАРИФУ
limits = {'TRIAL': 3, 'HOBBY': 30, 'PRO': 999}
used = st.session_state.uploads_count

st.sidebar.metric("📊 Использовано видео", f"{used}/{limits[plan.split()[0]]}")
st.sidebar.caption(f"TRIAL до: {st.session_state.trial_end}")

# ПРОВЕРКА ЛИМИТА
if used >= limits[plan.split()[0]]:
    st.error(f"🔒 {plan}: лимит {limits[plan.split()[0]]} видео/мес исчерпан!")
    st.info("💎 Обнови тариф или жди следующего месяца")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💎 Купить HOBBY (199₽)", use_container_width=True):
            st.session_state.plan = 'HOBBY'
            st.rerun()
    with col2:
        if st.button("🏆 Купить PRO (499₽)", use_container_width=True):
            st.session_state.plan = 'PRO'
            st.rerun()
else:
    # ✅ АНАЛИЗ ВИДЕО
    video_file = st.file_uploader("📹 Загрузи видео броска", 
                                  type=['mp4','mov','avi'], 
                                  key=f"video_{used}")
    
    if video_file:
        st.session_state.uploads_count += 1
        
        file_hash = hashlib.md5(video_file.read()).hexdigest()
        video_file.seek(0)
        
        st.video(video_file)
        st.success(f"✅ Анализ #{used} | Осталось: {limits[plan.split()[0]]-used-1}")
        
        # ✅ МЕТРИКИ (уникальные ключи)
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
        
        # 🎯 РЕКОМЕНДАЦИИ
        st.markdown("### 🎯 Твой план тренировок")
        recs = []
        if angle < 90: recs.append("🔴 **СТЕНА**: Локоть 10см от стены")
        if speed < 8.5: recs.append("⚡ **МЯЧИК**: Теннисный мячик 3x20")
        if stab > 2: recs.append("🧠 **ЛАЗЕР**: Лист на лоб")
        
        for rec in recs: st.error(rec)
        if not recs: st.success("🎉 Отличная техника!")
        
        # 💎 PRO ФИЧИ
        if plan == "🏆 PRO (499₽/мес)":
            col1, col2 = st.columns(2)
            with col1: st.download_button("📥 PDF отчёт", "Отчёт...", "pro-report.pdf")
            with col2: st.button("📱 История анализов")
        
        st.balloons()

st.markdown("---")
st.markdown("""
**💎 HOBBY (199₽/мес):** 30 видео + PDF  
**🏆 PRO (499₽/мес):** ∞ видео + 3D + история
**Оплата:** ЮKassa / Telegram Stars / Tinkoff
👉 [@dartsai_coach](t.me/dartsai_coach)
""")
