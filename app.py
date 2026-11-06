import streamlit as st
from datetime import datetime
from contenidos import SECCIONES

st.set_page_config(
    page_title="Programa de Formación Integral y Obligatoria",
    page_icon="🎓",
    layout="centered"
)

if "iniciado" not in st.session_state:
    st.session_state.iniciado = False
if "cedula" not in st.session_state:
    st.session_state.cedula = ""
if "seccion_actual" not in st.session_state:
    st.session_state.seccion_actual = 0
if "respuestas_correctas" not in st.session_state:
    st.session_state.respuestas_correctas = 0
if "chat_ia" not in st.session_state:
    st.session_state.chat_ia = []

if "registro_usuarios" not in st.session_state:
    st.session_state.registro_usuarios = {}

st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.6s ease-out forwards;
    }
    .main-header {
        font-size: 28px;
        font-weight: 800;
        color: #1b365d;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 16px;
        color: #5c768d;
        text-align: center;
        margin-bottom: 25px;
    }
    .hero-card {
        background: linear-gradient(135deg, #1b365d 0%, #2c5282 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(27, 54, 93, 0.2);
        margin-bottom: 25px;
    }
    .info-box {
        background-color: #f8fafc;
        border-left: 5px solid #2b6cb0;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .admin-box {
        background-color: #eef2f7;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #319795;
        margin-bottom: 20px;
    }
    .ia-box {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border: 2px dashed #cbd5e0;
        padding: 20px;
        border-radius: 12px;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.iniciado:
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-card">
        <h1 style="color: white; margin-top: 0; font-size: 26px;">🎓 Programa de Formación Integral y Obligatoria</h1>
        <p style="font-size: 16px; opacity: 0.9;">Capacitación general y corporativa orientada a la excelencia en el lugar de trabajo.</p>
        <hr style="border-color: rgba(255,255,255,0.2); margin: 15px 0;">
        <p style="font-size: 14px; margin-bottom: 0;">🛡️ Desarrollado en estricto cumplimiento con el <b>Acuerdo Ministerial MDT-2025-006</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box fade-in">
        <h3>📌 Indicaciones Importantes para el Personal:</h3>
        <ul>
            <li><b>Estructura Completa:</b> El programa consta de <b>1
