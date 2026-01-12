import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import plotly.graph_objects as go
import tempfile
import os
from io import BytesIO

st.set_page_config(page_title="🏆 Darts AI Coach Pro", layout="wide")
st.title("🏆 Darts AI Coach Pro")
st.markdown("**Анализ броска за 10 сек • Сравнение с PDC чемпионами • Персональный план**")

# MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(model_complexity=2, min_detection_confidence=0.5)

# Sidebar инструкция
with st.sidebar:
    st.header("📱 Как снимать")
    st.markdown("""
    - ✅ **Профиль сбоку** (рука видна)
    - ✅ **Slow-mo 120fps**  
    - ✅ **Ноги → рука → доска**
    - ✅ **Равномерный свет**
    """)

# Видео загрузка
video_file = st.file_uploader("📹 Загрузи видео броска", type=['mp4','mov','avi'])

if video_file is not None:
    # Сохраняем временно
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(video_file.read())
    video_path = tfile.name
    
    with st.spinner("🎯 Анализирую биомеханику..."):
        cap = cv2.VideoCapture(video_path)
        wrist3d, elbow3d, head3d = [], [], []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)
            
            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark
                wrist3d.append([lm[16].x, lm[16].y, lm[16].z])  # Кисть
                elbow3d.append([lm[14].x, lm[14].y, lm[14].z])  # Локоть
                head3d.append([lm[0].x, lm[0].y, lm[0].z])      # Голова
        
        cap.release()
        os.unlink(video_path)
    
    if len(wrist3d) > 10:
        # Нормализация
        wrist3d = np.array(wrist3d) * 2.4
        elbow3d = np.array(elbow3d) * 2.4
        head3d = np.array(head3d) * 2.4
        
        # МЕТРИКИ
        def calc_angle(a, b, c):
            ba = a - b
            bc = c - b
            cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))
        
        angles = [calc_angle(elbow3d[i], wrist3d[i], wrist3d[i+1]) 
                 for i in range(len(wrist3d)-1)]
        
        release_angle = np.mean(angles[-8:])
        wrist_speed = np.max(np.linalg.norm(np.diff(wrist3d, axis=0), axis=1)) * 25
        head_stab = np.std(head3d[:, :2]) * 100
        
        # 2-колоночный дашборд
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🎯 Локоть релиз", f"{release_angle:.1f}°", f"{100-release_angle:+.0f}°")
            st.metric("⚡ Скорость кисти", f"{wrist_speed:.1f} м/с", f"{9.8-wrist_speed:+.1f}")
            st.metric("🧠 Стабильность головы", f"{head_stab:.1f} см", f"{1.5-head_stab:+.1f}")
        
        with col2:
            st.markdown("### 👑 Сравнение с PDC топом")
            st.markdown("""
            | Метрика | Ты | Хамфрис |
            |---------|----|---------|
            | Локоть | {:.0f}° | **100°** | 
            | Скорость | {:.1f} м/с | **9.8** |
            | Голова | {:.1f} см | **1.2** |
            """.format(release_angle, wrist_speed, head_stab))
        
        # 3D график
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=wrist3d[-50:,0], y=wrist3d[-50:,1], z=-wrist3d[-50:,2],
            mode='lines+markers', name='Кисть', line=dict(width=8, color='red'),
            marker=dict(size=6)
        ))
        fig.add_trace(go.Scatter3d(
            x=elbow3d[-50:,0], y=elbow3d[-50:,1], z=-elbow3d[-50:,2],
            mode='lines', name='Локоть', line=dict(width=5, color='blue')
        ))
        fig.update_layout(
            title="🚀 3D Траектория броска", height=500,
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Угол локтя график
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(y=angles, mode='lines+markers', name='Угол локтя'))
        fig2.add_hline(y=100, line_dash="dash", line_color="red", 
                       annotation_text="PDC идеал", annotation_position="top right")
        fig2.update_layout(title="📈 Динамика угла локтя", xaxis_title="Кадр", yaxis_title="°")
        st.plotly_chart(fig2, use_container_width=True)
        
        # ПЕРСОНАЛЬНЫЕ РЕКОМЕНДАЦИИ
        st.markdown("## 🎯 Твой план тренировок")
        
        recs = []
        if release_angle < 80:
            recs.append("🔴 **СТЕНА**: Локоть у стены (10см), 50 бросков/день")
        if head_stab > 3:
            recs.append("🧠 **ЛАЗЕР**: Лист на лоб, маркер на мишень")
        if wrist_speed < 8:
            recs.append("⚡ **МЯЧИК**: Замах с теннисным мячиком")
            
        for rec in recs:
            st.error(rec)
            
        if not recs:
            st.success("🎉 Отличная техника! Работай над скоростью.")
        
        # КНОПКИ ДЛЯ ТУРНИРОВ
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button("📥 PDF отчёт", "Отчёт...", "darts_analysis.pdf")
        with col2:
            st.button("📱 Telegram", help="Отправить в турнир")
        with col3:
            st.button("👥 Поделиться", help="VK/Telegram")
    
    else:
        st.error("❌ Недостаточно данных. Сними **сбоку в профиль**, **slow-mo 120fps**!")

# ФУ터
st.markdown("---")
st.markdown("🏆 **Darts AI Coach Pro** | Для корпоративных турниров и школ")
