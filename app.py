import streamlit as st
import streamlit.components.v1 as components
import time
from contenidos import SECCIONES

st.set_page_config(
    page_title="Plataforma de Capacitación - ILEPSA",
    page_icon="🏢",
    layout="centered"
)

# Inicializar estados de sesión
if "iniciado" not in st.session_state:
    st.session_state.iniciado = False
if "cargando" not in st.session_state:
    st.session_state.cargando = False
if "cedula" not in st.session_state:
    st.session_state.cedula = ""
if "seccion_actual" not in st.session_state:
    st.session_state.seccion_actual = 0
if "respuestas_correctas" not in st.session_state:
    st.session_state.respuestas_correctas = 0
if "progreso_usuarios" not in st.session_state:
    st.session_state.progreso_usuarios = {}
if "chat_ia" not in st.session_state:
    st.session_state.chat_ia = []

# Estilos CSS avanzados: Animación visual de paso de página estilo libro
st.markdown("""
    <style>
    /* Animación de cambio de página de libro (Page Flip / Slide 3D) */
    @keyframes flipBook {
        0% {
            opacity: 0;
            transform: perspective(1000px) rotateY(-15deg) translateX(-30px);
            filter: blur(2px);
        }
        50% {
            opacity: 0.5;
            filter: blur(0px);
        }
        100% {
            opacity: 1;
            transform: perspective(1000px) rotateY(0deg) translateX(0px);
        }
    }

    .book-page {
        animation: flipBook 0.55s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 6px solid #0284c7;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 10px 10px 25px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }

    .welcome-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 35px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        margin-bottom: 25px;
    }

    .main-title {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .company-subtitle {
        font-size: 16px;
        font-weight: 600;
        color: #38bdf8;
        margin-bottom: 15px;
    }

    .question-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #0284c7;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .ia-box {
        background-color: #f1f5f9;
        border: 1px dashed #94a3b8;
        padding: 18px;
        border-radius: 10px;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Forzar scroll automático al borde superior del sitio
components.html(
    """
    <script>
        window.parent.scrollTo({top: 0, behavior: 'smooth'});
    </script>
    """,
    height=0,
)

# ---------------------------------------------------------
# PANTALLA 1: ACCESO E INGRESO DE CÉDULA
# ---------------------------------------------------------
if not st.session_state.iniciado and not st.session_state.cargando:
    st.markdown("""
    <div class="welcome-card">
        <div class="main-title">PROGRAMA DE FORMACIÓN INTEGRAL Y OBLIGATORIA</div>
        <div class="company-subtitle">COMPAÑÍA ILEPSA S.A.</div>
        <p style="opacity: 0.9; font-size: 15px;">Cumplimiento Normativo — Acuerdo Ministerial MDT-2025-006</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #ffffff; padding: 25px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 20px;">
        <h4 style="margin-top:0; color: #0f172a;">📋 Instrucciones del Sistema</h4>
        <ul>
            <li><b>Estructura Evaluativa:</b> 100 Secciones de aprendizaje en 4 ejes fundamentales.</li>
            <li><b>Guardado Automático:</b> El avance se registra automáticamente por cada sección aprobada.</li>
            <li><b>Certificación Oficial:</b> Disponible al culminar la totalidad del programa.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    cedula_input = st.text_input("Ingrese su Cédula de Identidad:", max_chars=10, type="password")
    
    if st.button("Ingresar al Sistema", type="primary"):
        cedula_limpia = cedula_input.strip()
        if len(cedula_limpia) >= 10:
            st.session_state.cedula = cedula_limpia
            st.session_state.cargando = True
            st.rerun()
        else:
            st.error("Por favor ingrese un número de cédula válido.")

# ---------------------------------------------------------
# PANTALLA 2: BIENVENIDA Y CARGA TEMPORIZADA (SPINNER)
# ---------------------------------------------------------
elif st.session_state.cargando:
    st.markdown(f"""
    <div class="welcome-card">
        <h2 style="color: #38bdf8; margin-bottom: 10px;">¡BIENVENIDO(A) AL SISTEMA!</h2>
        <h3 style="color: #ffffff; margin-top: 0;">Colaborador Cédula: N° {st.session_state.cedula}</h3>
        <p style="font-size: 15px; color: #cbd5e1;">Cargando contenido modular de la Compañía ILEPSA...</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Cargando su progreso y preparando el entorno de capacitación..."):
        time.sleep(2.5)  # Pausa visual para la experiencia de carga
        
    # Cargar progreso guardado
    if st.session_state.cedula in st.session_state.progreso_usuarios:
        st.session_state.seccion_actual = st.session_state.progreso_usuarios[st.session_state.cedula]
    else:
        st.session_state.seccion_actual = 0
        
    st.session_state.cargando = False
    st.session_state.iniciado = True
    st.rerun()

# ---------------------------------------------------------
# PANTALLA 3: CAPACITACIÓN CON ANIMACIÓN PÁGINA DE LIBRO
# ---------------------------------------------------------
else:
    total_secciones = len(SECCIONES)
    sec_idx = st.session_state.seccion_actual
    
    # Encabezado corporativo superior
    col_hdr1, col_hdr2, col_hdr3 = st.columns([2, 2, 1])
    col_hdr1.write("🏢 **Empresa:** ILEPSA S.A.")
    col_hdr2.write(f"👤 **Usuario:** {st.session_state.cedula}")
    if col_hdr3.button("Guardar y Salir"):
        st.session_state.iniciado = False
        st.session_state.cedula = ""
        st.rerun()
        
    st.divider()
    
    progreso_val = sec_idx / total_secciones
    st.progress(progreso_val, text=f"Progreso: Sección {sec_idx + 1} de {total_secciones} ({int(progreso_val*100)}%)")
    
    if sec_idx < total_secciones:
        seccion = SECCIONES[sec_idx]
        
        # Envoltorio CSS contenedor que simula pasar la página del libro en cada rerender
        st.markdown(f'<div class="book-page" key="book_page_{sec_idx}">', unsafe_allow_html=True)
        
        st.markdown(f"### 📖 {seccion['eje']}")
        st.markdown(f"## {seccion['titulo']}")
        
        st.markdown(seccion['contenido'])
        
        st.markdown(f"""
        <div class="question-box">
            <h4 style="margin-top:0;">📝 Evaluación de la Sección {sec_idx + 1}</h4>
            <p style="font-size:16px;"><b>{seccion['pregunta']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        respuesta_usuario = st.radio("Seleccione la opción correcta:", seccion['opciones'], key=f"p_radio_{sec_idx}")
        
        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            if st.button("Siguiente Sección ➔", type="primary"):
                if respuesta_usuario == seccion['correcta']:
                    st.success("¡Respuesta correcta! Volteando página...")
                    st.session_state.respuestas_correctas += 1
                    st.session_state.seccion_actual += 1
                    st.session_state.progreso_usuarios[st.session_state.cedula] = st.session_state.seccion_actual
                    time.sleep(0.4) # Pequeña pausa para apreciar la transición
                    st.rerun()
                else:
                    st.error("Respuesta incorrecta. Revise la teoría antes de continuar.")
                    
        st.markdown("""
        <div class="ia-box">
            <h5 style="margin:0 0 5px 0;">🤖 Asistente de Consulta ILEPSA</h5>
            <p style="font-size: 13px; color: #475569; margin-bottom:10px;">¿Dudas sobre esta sección? Escriba su consulta a continuación:</p>
        </div>
        """, unsafe_allow_html=True)
        
        pregunta_ia = st.text_input("Escriba su consulta:", key=f"ia_q_{sec_idx}")
        if st.button("Consultar Asistente", key=f"ia_btn_{sec_idx}"):
            if pregunta_ia.strip():
                st.info(f"Asistente ILEPSA: Respecto a '{pregunta_ia}', el marco del MDT-2025-006 exige cumplimiento riguroso y respeto a las garantías laborales.")
            else:
                st.warning("Escriba una pregunta válida.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # PANTALLA FINAL: CERTIFICADO
    # ---------------------------------------------------------
    else:
        st.balloons()
        st.markdown('<div class="book-page">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center;">
            <h2>📜 CERTIFICADO OFICIAL DE APROBACIÓN</h2>
            <h3>COMPAÑÍA ILEPSA S.A.</h3>
            <p>Se certifica que el colaborador con Cédula N° <b>{st.session_state.cedula}</b> ha completado y aprobado satisfactoriamente las <b>100 secciones</b> del Programa de Formación Integral bajo el marco del <b>Acuerdo Ministerial MDT-2025-006</b>.</p>
            <hr style="margin: 20px 0;">
            <p><b>Calificación Aciertos:</b> {st.session_state.respuestas_correctas} / {total_secciones}</p>
            <p style="color: #059669; font-weight: bold; font-size: 18px;">ESTADO: CERTIFICADO EMITIDO</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Finalizar y Salir"):
            st.session_state.iniciado = False
            st.session_state.cedula = ""
            st.session_state.seccion_actual = 0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
