import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from contenidos import SECCIONES

st.set_page_config(
    page_title="Plataforma de Capacitación - ILEPSA",
    page_icon="🏢",
    layout="centered"
)

# Inicializar estados
if "iniciado" not in st.session_state:
    st.session_state.iniciado = False
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

# Estilos con animación de "paso de página / libro" (Page Flip effect)
st.markdown("""
    <style>
    @keyframes bookFlip {
        0% {
            opacity: 0;
            transform: translateY(20px) scale(0.99);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    .page-container {
        animation: bookFlip 0.4s ease-out forwards;
    }
    
    .main-title {
        font-size: 26px;
        font-weight: 700;
        color: #0f172a;
        text-align: center;
        margin-bottom: 0px;
    }
    .company-subtitle {
        font-size: 16px;
        font-weight: 600;
        color: #0284c7;
        text-align: center;
        margin-bottom: 20px;
    }
    .exam-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
    }
    .question-box {
        background-color: #f8fafc;
        border-left: 5px solid #0284c7;
        padding: 20px;
        border-radius: 0 8px 8px 0;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .ia-box {
        background-color: #f1f5f9;
        border: 1px dashed #cbd5e1;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Forzar al navegador padre a subir hasta arriba mediante iframe de componentes
components.html(
    """
    <script>
        window.parent.scrollTo({top: 0, behavior: 'smooth'});
    </script>
    """,
    height=0,
)

# ---------------------------------------------------------
# PANTALLA DE ACCESO / PORTADA OFICIAL ILEPSA
# ---------------------------------------------------------
if not st.session_state.iniciado:
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">PROGRAMA DE FORMACIÓN INTEGRAL Y OBLIGATORIA</div>', unsafe_allow_html=True)
    st.markdown('<div class="company-subtitle">COMPAÑÍA ILEPSA</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="exam-card">
        <h3>Bienvenido al Sistema de Capacitación</h3>
        <p>En cumplimiento con la normativa legal vigente y el Acuerdo Ministerial MDT-2025-006, este programa de capacitación está diseñado para promover un entorno laboral seguro, equitativo y libre de violencia.</p>
        <hr style="margin: 15px 0; border: none; border-top: 1px solid #e2e8f0;">
        <ul>
            <li>Estructura: 100 Secciones evaluadas en 4 ejes fundamentales.</li>
            <li>Guardado Automático: Su progreso se almacena de forma automática por cada sección completada. Si sale y vuelve a ingresar con su cédula, continuará exactamente donde se quedó.</li>
            <li>Certificación: Al completar el 100% de las secciones, el sistema emitirá su certificado oficial.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    cedula_input = st.text_input("Ingrese su Cédula de Identidad para iniciar:", max_chars=10, type="password")
    
    if st.button("Iniciar / Continuar Sesión", type="primary"):
        cedula_limpia = cedula_input.strip()
        if len(cedula_limpia) >= 10:
            st.session_state.iniciado = True
            st.session_state.cedula = cedula_limpia
            if cedula_limpia in st.session_state.progreso_usuarios:
                st.session_state.seccion_actual = st.session_state.progreso_usuarios[cedula_limpia]
            else:
                st.session_state.seccion_actual = 0
            st.rerun()
        else:
            st.error("Por favor ingrese un número de cédula válido.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# DESARROLLO DE LA EVALUACIÓN (EFECTO PÁGINA DE LIBRO)
# ---------------------------------------------------------
else:
    total_secciones = len(SECCIONES)
    sec_idx = st.session_state.seccion_actual
    
    col_info1, col_info2, col_info3 = st.columns([2, 2, 1])
    col_info1.write("Compañía: ILEPSA")
    col_info2.write(f"Usuario (Cédula): {st.session_state.cedula}")
    if col_info3.button("Guardar y Salir"):
        st.session_state.iniciado = False
        st.session_state.cedula = ""
        st.rerun()
        
    st.divider()
    
    progreso_val = sec_idx / total_secciones
    st.progress(progreso_val, text=f"Progreso General: Sección {sec_idx + 1} de {total_secciones} ({int(progreso_val*100)}%)")
    
    if sec_idx < total_secciones:
        seccion = SECCIONES[sec_idx]
        
        # Envoltorio con la clase page-container para forzar la animación de cambio de hoja
        st.markdown(f'<div class="page-container" key="page_{sec_idx}">', unsafe_allow_html=True)
        
        st.markdown(f"### {seccion['eje']}")
        st.markdown(f"## {seccion['titulo']}")
        
        st.markdown(f"""
        <div class="exam-card">
            {seccion['contenido']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="question-box">
            <h4>Evaluación de la Sección {sec_idx + 1}</h4>
            <p>{seccion['pregunta']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        respuesta_usuario = st.radio("Seleccione la respuesta correcta:", seccion['opciones'], key=f"eval_p_{sec_idx}")
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("Continuar a la Siguiente Sección ➔", type="primary"):
                if respuesta_usuario == seccion['correcta']:
                    st.success("¡Respuesta correcta registrada con éxito!")
                    st.session_state.respuestas_correctas += 1
                    st.session_state.seccion_actual += 1
                    st.session_state.progreso_usuarios[st.session_state.cedula] = st.session_state.seccion_actual
                    st.rerun()
                else:
                    st.error("Respuesta incorrecta. Por favor revise nuevamente el contenido teórico de la sección.")
                    
        st.markdown("""
        <div class="ia-box">
            <h5 style="margin:0 0 5px 0;">Asistente de Consulta ILEPSA</h5>
            <p style="font-size: 13px; color: #475569; margin-bottom:10px;">¿Tiene alguna duda sobre el contenido de esta sección? Realice su consulta:</p>
        </div>
        """, unsafe_allow_html=True)
        
        pregunta_ia = st.text_input("Escriba su consulta:", key=f"ia_q_{sec_idx}")
        if st.button("Consultar Asistente", key=f"ia_btn_{sec_idx}"):
            if pregunta_ia.strip():
                st.info(f"Asistente ILEPSA: En relación con su consulta sobre '{pregunta_ia}', recuerde que las normativas internas y el marco del Acuerdo Ministerial MDT-2025-006 priorizan siempre el respeto, la equidad y el cumplimiento legal estricto.")
            else:
                st.warning("Ingrese un texto para consultar.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # PANTALLA FINAL - CERTIFICADO
    # ---------------------------------------------------------
    else:
        st.balloons()
        st.markdown('<div class="page-container">', unsafe_allow_html=True)
        st.markdown("""
        <div class="exam-card" style="text-align: center; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);">
            <h2>CERTIFICADO OFICIAL DE APROBACIÓN</h2>
            <p>COMPAÑÍA ILEPSA</p>
            <p>Se certifica que el colaborador con Cédula N° {cedula} ha completado y aprobado satisfactoriamente las 100 secciones del Programa de Formación Integral bajo el marco del Acuerdo Ministerial MDT-2025-006.</p>
            <hr style="margin: 20px 0;">
            <p>Calificación Final / Aciertos: {correctas} / {total}</p>
            <p style="color: #059669; font-weight: bold;">ESTADO: APROBADO CON ÉXITO</p>
        </div>
        """.format(cedula=st.session_state.cedula, correctas=st.session_state.respuestas_correctas, total=total_secciones), unsafe_allow_html=True)
        
        if st.button("Finalizar y Salir del Sistema"):
            st.session_state.iniciado = False
            st.session_state.cedula = ""
            st.session_state.seccion_actual = 0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
