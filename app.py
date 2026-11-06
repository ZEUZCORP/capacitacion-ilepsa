import streamlit as st
from contenidos import SECCIONES

# Configuración inicial de la página
st.set_page_config(
    page_title="Programa de Formación Integral y Obligatoria",
    page_icon="📚",
    layout="centered"
)

# Inicializar variables de sesión
if "iniciado" not in st.session_state:
    st.session_state.iniciado = False
if "cedula" not in st.session_state:
    st.session_state.cedula = ""
if "seccion_actual" not in st.session_state:
    st.session_state.seccion_actual = 0
if "respuestas_correctas" not in st.session_state:
    st.session_state.respuestas_correctas = 0

# Estilo visual limpio y profesional
st.markdown("""
    <style>
    .main-header {
        font-size: 24px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PANTALLA DE INICIO / LOGIN CON CÉDULA E INTRODUCCIÓN
# ---------------------------------------------------------
if not st.session_state.iniciado:
    st.markdown('<div class="main-header">Programa de Formación y Capacitación Integral</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>Bienvenido al Programa Obligatorio</h3>
        <p>En cumplimiento con la normativa legal vigente y el <b>Acuerdo Ministerial MDT-2025-006</b>, este programa de capacitación está diseñado de manera general para todo el entorno laboral, promoviendo espacios seguros, justos y libres de violencia.</p>
        <p><b>Indicaciones importantes:</b></p>
        <ul>
            <li>El programa consta de <b>100 secciones formativas</b> divididas en cuatro ejes fundamentales.</li>
            <li>Se recomienda un tiempo de dedicación de al menos <b>30 minutos diarios</b> para asegurar un correcto aprendizaje.</li>
            <li>Para obtener tu <b>certificado oficial de aprobación</b>, debes culminar y aprobar satisfactoriamente la totalidad de las secciones y evaluaciones del programa.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Acceso al Sistema")
    cedula_input = st.text_input("Ingrese su número de Cédula de Identidad:", max_chars=10)
    
    if st.button("Iniciar Capacitación", type="primary"):
        if len(cedula_input.strip()) >= 10:
            st.session_state.iniciado = True
            st.session_state.cedula = cedula_input.strip()
            st.rerun()
        else:
            st.error("Por favor, ingrese un número de cédula válido para continuar.")

# ---------------------------------------------------------
# DESARROLLO DE LAS SECCIONES Y EVALUACIONES
# ---------------------------------------------------------
else:
    total_secciones = len(SECCIONES)
    sec_idx = st.session_state.seccion_actual
    
    # Barra de progreso general
    progreso = (sec_idx / total_secciones)
    st.progress(progreso, text=f"Progreso general: Sección {sec_idx + 1} de {total_secciones}")
    
    if sec_idx < total_secciones:
        seccion = SECCIONES[sec_idx]
        
        st.markdown(f"### {seccion['eje']}")
        st.markdown(f"## {seccion['titulo']}")
        
        # Contenido de lectura
        st.markdown(seccion['contenido'])
        
        st.divider()
        
        # Evaluación de la sección
        st.markdown("#### Evaluación de Aprendizaje")
        respuesta_usuario = st.radio(seccion['pregunta'], seccion['opciones'], key=f"p_{sec_idx}")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Enviar Respuesta", type="primary"):
                if respuesta_usuario == seccion['correcta']:
                    st.success("¡Respuesta correcta!")
                    st.session_state.respuestas_correctas += 1
                    st.session_state.seccion_actual += 1
                    st.rerun()
                else:
                    st.error("Respuesta incorrecta. Por favor, lee nuevamente el contenido y selecciona la opción correcta.")
    
    # ---------------------------------------------------------
    # PANTALLA FINAL Y EMISIÓN DE CERTIFICADO
    # ---------------------------------------------------------
    else:
        st.balloons()
        st.markdown('<div class="main-header">¡Felicitaciones! Has Culminado el Programa Exitosamente</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-box">
            <h3>Certificado Oficial de Aprobación</h3>
            <p>Se certifica que el colaborador con Cédula N° <b>{st.session_state.cedula}</b> ha completado satisfactoriamente las <b>100 secciones</b> del Programa de Formación Integral bajo el marco del <b>Acuerdo Ministerial MDT-2025-006</b>.</p>
            <p>Aciertos registrados en evaluaciones: <b>{st.session_state.respuestas_correctas} / {total_secciones}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Reiniciar o Salir"):
            st.session_state.iniciado = False
            st.session_state.seccion_actual = 0
            st.session_state.respuestas_correctas = 0
            st.rerun()
