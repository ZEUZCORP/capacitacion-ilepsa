import streamlit as st
import time
from contenidos import SECCIONES

st.set_page_config(
    page_title="Capacitación ILEPSA - Módulos",
    page_icon="📖",
    layout="centered"
)

# Seguridad: Si intentan entrar directo por la URL sin loguearse
if "cedula" not in st.session_state or not st.session_state.cedula:
    st.warning("Debe iniciar sesión con su cédula primero.")
    if st.button("Ir al Inicio"):
        st.switch_page("app.py")
    st.stop()

# Inicializar estados de progreso
if "seccion_actual" not in st.session_state:
    st.session_state.seccion_actual = 0
if "respuestas_correctas" not in st.session_state:
    st.session_state.respuestas_correctas = 0
if "progreso_usuarios" not in st.session_state:
    st.session_state.progreso_usuarios = {}

# Recuperar progreso si ya lo tenía guardado en memoria
if st.session_state.cedula in st.session_state.progreso_usuarios:
    st.session_state.seccion_actual = st.session_state.progreso_usuarios[st.session_state.cedula]

total_secciones = len(SECCIONES)
sec_idx = st.session_state.seccion_actual

# Estilos limpios
st.markdown("""
    <style>
    .card-seccion {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 6px solid #0284c7;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .header-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .pregunta-box {
        background-color: #f1f5f9;
        border-left: 4px solid #0284c7;
        padding: 18px;
        border-radius: 0 8px 8px 0;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado institucional con Nombre y Cédula
st.markdown(f"""
    <div class="header-box">
        <table style="width:100%; border:none; margin:0;">
            <tr>
                <td style="border:none;">🏢 <b>Empresa:</b> ILEPSA S.A.</td>
                <td style="border:none;">👤 <b>Colaborador:</b> {st.session_state.nombre_usuario}</td>
                <td style="border:none;">🪪 <b>Cédula:</b> {st.session_state.cedula}</td>
            </tr>
        </table>
    </div>
""", unsafe_allow_html=True)

col_h1, col_h2 = st.columns([5, 1])
with col_h2:
    if st.button("Salir"):
        st.session_state.cedula = ""
        st.switch_page("app.py")

progreso = sec_idx / total_secciones
st.progress(progreso, text=f"Progreso general: Sección {sec_idx + 1} de {total_secciones}")

# Desarrollo de la sección activa
if sec_idx < total_secciones:
    seccion = SECCIONES[sec_idx]
    
    st.markdown(f"""
    <div class="card-seccion">
        <span style="color: #0284c7; font-weight: bold; font-size: 14px;">{seccion['eje']}</span>
        <h2 style="margin-top: 5px; color: #0f172a;">{seccion['titulo']}</h2>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 15px 0;">
        <div style="font-size: 16px; line-height: 1.6; color: #334155;">
            {seccion['contenido']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="pregunta-box">
        <h4 style="margin-top:0; color: #0f172a;">Evaluación Obligatoria</h4>
        <p style="font-size: 16px; font-weight: 600; color: #1e293b;">{seccion['pregunta']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form(key=f"form_sec_{sec_idx}"):
        respuesta = st.radio("Seleccione la respuesta correcta:", seccion['opciones'])
        
        submitted = st.form_submit_button("Siguiente Sección ➔", type="primary")
        if submitted:
            if respuesta == seccion['correcta']:
                st.session_state.respuestas_correctas += 1
                st.session_state.seccion_actual += 1
                st.session_state.progreso_usuarios[st.session_state.cedula] = st.session_state.seccion_actual
                st.success("¡Respuesta correcta! Abriendo siguiente página...")
                time.sleep(0.4)
                st.rerun()
            else:
                st.error("Respuesta incorrecta. Revise la teoría superior e intente de nuevo.")

else:
    # Pantalla de Certificado Final
    st.balloons()
    st.markdown(f"""
    <div class="card-seccion" style="text-align: center;">
        <h2 style="color: #0f172a;">📜 CERTIFICADO OFICIAL DE APROBACIÓN</h2>
        <h4 style="color: #0284c7;">COMPAÑÍA ILEPSA S.A.</h4>
        <p>Se otorga el presente certificado a:</p>
        <h3 style="color: #0f172a; text-decoration: underline;">{st.session_state.nombre_usuario}</h3>
        <p>Con Cédula N° <b>{st.session_state.cedula}</b> por haber completado y aprobado con éxito las 100 secciones del programa bajo la normativa MDT-2025-006.</p>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;">
        <p><b>Calificación Final:</b> {st.session_state.respuestas_correctas} / {total_secciones} aciertos.</p>
        <p style="color: #059669; font-weight: bold;">ESTADO: APROBADO CON ÉXITO</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Finalizar y Salir"):
        st.session_state.cedula = ""
        st.switch_page("app.py")
