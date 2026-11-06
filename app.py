import streamlit as st
import streamlit.components.v1 as components
import time
from datetime import datetime
from supabase import create_client, Client
from contenidos import SECCIONES

st.set_page_config(
    page_title="Plataforma ILEPSA",
    page_icon="🏢",
    layout="centered"
)

@st.cache_resource
def init_supabase() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_supabase()

# Inicialización de estados de sesión
if "paso" not in st.session_state:
    st.session_state.paso = "login"
if "cedula" not in st.session_state:
    st.session_state.cedula = ""
if "nombre_usuario" not in st.session_state:
    st.session_state.nombre_usuario = ""
if "es_admin" not in st.session_state:
    st.session_state.es_admin = False
if "seccion_actual" not in st.session_state:
    st.session_state.seccion_actual = 0
if "sub_paso" not in st.session_state:
    st.session_state.sub_paso = "teoria"
if "respuestas_correctas" not in st.session_state:
    st.session_state.respuestas_correctas = 0

COLORES_SECCION = [
    {"borde": "#0284c7", "fondo_etiqueta": "#e0f2fe", "texto_etiqueta": "#0369a1"},
    {"borde": "#7c3aed", "fondo_etiqueta": "#ede9fe", "texto_etiqueta": "#6d28d9"},
    {"borde": "#059669", "fondo_etiqueta": "#d1fae5", "texto_etiqueta": "#047857"},
    {"borde": "#d97706", "fondo_etiqueta": "#fef3c7", "texto_etiqueta": "#b45309"},
    {"borde": "#dc2626", "fondo_etiqueta": "#fee2e2", "texto_etiqueta": "#b91c1c"}
]

# Estilos CSS (Texto justificado y opciones del radio en cajitas separadas y letra grande)
st.markdown("""
    <style>
    @keyframes fadeInPage {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .pagina-nueva-transicion {
        animation: fadeInPage 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .card-principal {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
        position: relative;
    }
    .badge-seccion-derecha {
        position: absolute;
        top: 20px;
        right: 25px;
        padding: 5px 14px;
        border-radius: 15px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .header-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 12px 18px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 15px;
    }
    .contenido-texto {
        font-size: 18.5px;
        line-height: 1.8;
        color: #334155;
        text-align: justify;
    }
    .pregunta-box {
        background-color: #f8fafc;
        border-left: 4px solid #0f172a;
        padding: 22px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    /* Opciones del radio en cajitas separadas, bien espaciadas y con letra grande */
    div.stRadio > label { 
        font-size: 18px !important; 
        font-weight: 600 !important; 
        color: #1e293b !important; 
        margin-bottom: 15px !important;
    }
    div.stRadio div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 12px !important;
    }
    div.stRadio div[role="radiogroup"] > label {
        background-color: #f8fafc !important;
        padding: 14px 18px !important;
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
        font-size: 16.5px !important;
        font-weight: 500 !important;
        color: #334155 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }
    div.stRadio div[role="radiogroup"] > label:hover {
        background-color: #f1f5f9 !important;
        border-color: #0284c7 !important;
    }
    </style>
""", unsafe_allow_html=True)
