import streamlit as st
import cv2
import numpy as np
import hashlib
import tempfile
import os
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🏆 Darts AI Coach Pro")

# Система тарифов (упрощённая)
if 'uploads_count' not in st.session_state: 
    st.session_state.uploads_count = 0

st.sidebar.info(f"📊 Анализов: {st.session_state.uploads_count}")

# ✅ РЕАЛЬНЫЙ АНАЛИЗ ВИДЕО
video_file = st.file_uploader("📹 Видео броска (сбоку, slow-mo)", 
                              type=['mp4','mov','avi'])

if video_file is not None:
    st.session_state.uploads_count += 1
    
    # Сохранение видео
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(video_file.read())
    video_path = tfile.name
    
    st.video(video_file)
    st.success(f"✅ Видео загружено: {video_file.name}")
    
    try:
        # ✅ MediaPipe Pose анализ
        import mediapipe as mp
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.5)
        
        cap = cv2.VideoCapture(video_path)
        wrist_y, elbow_y, angles = [], [], []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)
            
            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark
                # Кисть (16), локоть (14), плечо (12)
                wrist_y.append(lm[16].y * frame.shape[0])
                elbow_y.append(lm[14].y * frame.shape[0])
                
                # Угол локтя
                if len(wrist_y) > 1:
                    p1 = np.array([lm[12].x, lm[12].y])  # плечо
                    p2 = np.array([lm[14].x, lm[14].y])  # локоть  
                    p3 = np.array([lm[16].x, lm[16].y])  # кисть
                    angle = np.degrees(np.arccos(np.clip(np.dot(p1-p2, p3-p2) / 
                               (np.linalg.norm(p1-p2) * np.linalg.norm(p3-p2)), -1, 1)))
                    angles.append(angle)
        
        cap.release()
        os.unlink(video_path)
        
        if len(angles) > 5:
            # 🎯 РЕЗУЛЬТАТЫ
            release_angle = np.mean(angles[-10:])  # последние 0.3 сек
            angle_stability = np.std(angles[-20:])
            wrist_speed = np.std(wrist_y[-30:]) * 30  # пикселей/сек
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🎯 Локоть релиз", f"{release_angle:.1f}°", "95-105°")
            with col2:
                st.metric("⚡ Скорость кисти", f"{wrist_speed:.1f} пкс/с", "8-12")
            with col3:
                st.metric("📊 Стабильность угла", f"{angle_stability:.1f}°", "<3°")
            
            # 🔥 РЕКОМЕНДАЦИИ по результатам
            st.markdown("### 🎯 Твой план тренировок")
            
            if release_angle < 92:
                st.error("🔴 **СТЕНА**: Локоть 10см от стены, 50 бросков/день")
            if wrist_speed < 6:
                st.error("⚡ **МЯЧИК**: Теннисный мячик в замахе 3x20")
            if angle_stability > 4:
                st.error("🧠 **ФИКСАЦИЯ**: Взгляд на одну точку T20")
            
            if release_angle > 95 and wrist_speed > 8 and angle_stability < 3:
                st.success("🎉 **Профессиональная техника!** Работай над точностью.")
            
            # 📈 ГРАФИК
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=angles[-100:], mode='lines+markers', 
                                   name='Угол локтя', line=dict(color='red')))
            fig.add_hline(y=100, line_dash="dash", line_color="green", 
                         annotation_text="PDC идеал")
            fig.update_layout(title="📈 Динамика угла локтя", height=400)
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("⚠️ Недостаточно данных. Сними **строго сбоку**, **slow-mo 120fps**")
            
    except ImportError:
        st.error("❌ MediaPipe недоступен. Используй Colab для полного анализа")
        st.info("👉 [Colab 3D анализ](https://colab.research.google.com/drive/твой_ноутбук)")
        
else:
    st.info("""
    👆 **Загрузи видео броска** (сбоку, slow-mo 120fps)
    
    **Что получишь:**
    • 🎯 Реальный угол локтя из видео
    • ⚡ Скорость кисти (пкс/сек)  
    • 📊 Стабильность техники
    • 🎯 3 персональных упражнения
    """)
