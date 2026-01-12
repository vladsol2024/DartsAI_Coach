import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🏆 Darts AI Coach Pro")

# ✅ Инициализация сессии
if 'plan' not in st.session_state: 
    st.session_state.plan = 'TRIAL'
if 'uploads_count' not in st.session_state: 
    st.session_state.uploads_count = 0
if 'trial_end' not in st.session_state: 
    st.session_state.trial_end = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

# ✅ ТАРИФЫ (sidebar)
st.sidebar.header("💎 Твой тариф")
plan_options = {
    "🆓 TRIAL (3 видео)": "TRIAL", 
    "💎 HOBBY (199₽/мес)": "HOBBY", 
    "🏆 PRO (499₽/мес)": "PRO"
}

selected_plan = st.sidebar.selectbox("Выбери тариф", list(plan_options.keys()))
st.session_state.plan = plan_options[selected_plan]

# ✅ ЛИМИТЫ
limits = {'TRIAL': 3, 'HOBBY': 30, 'PRO': 999}
used = st.session_state.uploads_count
plan_key = st.session_state.plan

st.sidebar.info(f"📊 {used}/{limits[plan_key]} видео использовано")
st.sidebar.caption(f"TRIAL до: {st.session_state.trial_end}")

# ✅ ПРОВЕРКА ЛИМИТА
if used >= limits[plan_key]:
    st.error(f"🔒 {selected_plan}: лимит {limits[plan_key]} видео исчерпан!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💎 Купить HOBBY (199₽)", use_container_width=True):
            st.session_state.plan = 'HOBBY'
            st.session_state.uploads_count = 0
            st.rerun()
    with col2:
        if st.button("🏆 Купить PRO (499₽)", use_container_width=True):
            st.session_state.plan = 'PRO'
            st.session_state.uploads_count = 0
            st.rerun()
else:
    # ✅ АНАЛИЗ
    st.info(f"✅ Осталось видео: {limits[plan_key] - used - 1}")
    
    video_file = st.file_uploader("📹 Загрузи видео броска", 
                                  type=['mp4','mov','avi'])
    
    if video_file:
        st.session_state.uploads_count += 1
        st.video(video_file)
        st.success(f"✅ Анализ #{used + 1}")
        
        # ✅ МЕТРИКИ (уникальные ключи)
        col1, col2, col3 = st.columns(3)
        with col1:
            angle = st.slider("🎯 Локоть релиз", 60, 120, 98, 
                            key=f"angle_{used}")
            st.metric("PDC эталон", f"{angle}°", "95-105°")
        with col2:
            speed = st.slider("⚡ Скорость кисти", 6.0, 12.0, 9.8,
                            key=f"speed_{used}")
            st.metric("PDC эталон", f"{speed:.1f} м/с", "9-10.5")
        with col3:
            stab = st.slider("🧠 Стабильность головы", 0.5, 5.0, 1.2,
                           key=f"stab_{used}")
            st.metric("PDC эталон", f"{stab:.1f} см", "<1.5")
        
        # 🎯 РЕКОМЕНДАЦИИ
        st.markdown("### 🎯 Твой план тренировок")
        recs = []
        if angle < 90: recs.append("🔴 **СТЕНА**: Локоть 10см от стены")
        if speed < 8.5: recs.append("⚡ **МЯЧИК**: Теннисный мячик")
        if stab > 2: recs.append("🧠 **ЛАЗЕР**: Лист на лоб")
        
        for rec in recs: 
            st.error(rec)
        if not recs: 
            st.success("🎉 **Отличная техника!**")
        
        # 💎 PRO ФУНКЦИИ
        if plan_key == "PRO":
            col1, col2 = st.columns(2)
            with col1: 
                st.download_button("📥 PDF отчёт", "Отчёт...", "pro-report.pdf")
            with col2: 
                st.button("📱 История")

st.markdown("---")
st.markdown("""
💎 **HOBBY (199₽/мес):** 30 видео + PDF  
🏆 **PRO (499₽/мес):** ∞ видео + история  
📧 [@dartsai_coach](t.me/dartsai_coach)
""")
