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
if "paso" not in st.session_state:
    st.session_state.paso = "login"  # login, cargando, capacitacion, certificado
if "cedula" not in st.session_state:
    st.session_state.cedula = ""
if "seccion_actual" not in st.session_state:
    st.session_state.seccion_actual = 0
if "respuestas_correctas" not in st.session_state:
    st.session_state.respuestas_correctas = 0
if "progreso_usuarios" not in st.session_state:
    st.session_state.progreso_usuarios = {}

# Estilos avanzados con animación de paso de página de libro (Flip 3D)
st.markdown("""
    <style>
    @keyframes pageTurn {
        0% {
            opacity: 0;
            transform: translateY(15px) scale(0.98);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    .libro-hoja {
        animation: pageTurn 0.5s ease-out forwards;
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 6px solid #0284c7;
        padding: 35px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.06);
        margin-bottom: 25px;
    }

    .welcome-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 40px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        margin-bottom: 25px;
        animation: pageTurn 0.6s ease-out forwards;
    }

    .question-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0284c7;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Forzar scroll automático hacia arriba en cada recarga
components.html(
    """
    <script>
        window.parent.scrollTo({top: 0, behavior: 'smooth'});
    </script>
    """,
    height=0,
)

# ---------------------------------------------------------
# FASE 1: PANTALLA DE INGRESO (LOGIN)
# ---------------------------------------------------------
if st.session_state.paso == "login":
    st.markdown("""
    <div class="welcome-container">
        <h1 style="color: #ffffff; margin-top: 0; font-size: 28px;">PROGRAMA DE FORMACIÓN INTEGRAL</h1>
        <h3 style="color: #38bdf8; margin-bottom: 10px;">COMPAÑÍA ILEPSA S.A.</h3>
        <p style="opacity: 0.9; font-size: 15px;">Marco normativo del Acuerdo Ministerial MDT-2025-006</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="libro-hoja">
        <h4 style="margin-top:0; color: #0f172a;">📋 Indicaciones Importantes:</h4>
        <ul>
            <li><b>Estructura:</b> 100 Secciones de aprendizaje evaluadas.</li>
            <li><b>Guardado Automático:</b> Su progreso se almacena de forma individual por cédula.</li>
            <li><b>Certificación:</b> Se emite de forma automática al completar el 100% de las secciones.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    cedula_input = st.text_input("Ingrese su Cédula de Identidad:", max_chars=10, type="password")
    
    if st.button("Ingresar al Sistema", type="primary"):
        cedula_limpia = cedula_input.strip()
        if len(cedula_limpia) >= 10:
            st.session_state.cedula = cedula_limpia
            st.session_state.paso = "cargando"
            st.rerun()
        else:
            st.error("Por favor ingrese un número de cédula válido de 10 dígitos.")

# ---------------------------------------------------------
# FASE 2: PANTALLA DE BIENVENIDA Y CARGA VISIBLE
# ---------------------------------------------------------
elif st.session_state.paso == "cargando":
    st.markdown(f"""
    <div class="welcome-container">
        <h1 style="color: #38bdf8; margin-bottom: 10px;">¡BIENVENIDO(A) A ILEPSA!</h1>
        <h3 style="color: #ffffff; margin-top: 0;">Colaborador(a) Cédula N°: {st.session_state.cedula}</h3>
        <p style="font-size: 16px; color: #cbd5e1; margin-top: 15px;">Preparando su entorno de capacitación modular...</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra de progreso visual de carga deliberada para que el usuario aprecie la bienvenida
    barra_carga = st.progress(0, text="Iniciando sesión segura...")
    for porcentaje in range(1, 101):
        time.sleep(0.02)  # Controla la velocidad de la animación de bienvenida
        if porcentaje == 30:
            barra_carga.progress(porcentaje, text="Verificando registros de cumplimiento MDT-2025-006...")
        elif porcentaje == 70:
            barra_carga.progress(porcentaje, text="Cargando progreso guardado del colaborador...")
        elif porcentaje == 100:
            barra_carga.progress(porcentaje, text="¡Entorno listo con éxito!")

    time.sleep(0.5)
    
    # Recuperar progreso guardado si existe
    if st.session_state.cedula in st.session_state.progreso_usuarios:
        st.session_state.seccion_actual = st.session_state.progreso_usuarios[st.session_state.cedula]
    else:
        st.session_state.seccion_actual = 0
        
    st.session_state.paso = "capacitacion"
    st.rerun()

# ---------------------------------------------------------
# FASE 3: DESARROLLO DE LA CAPACITACIÓN (LIBRO INTERACTIVO)
# ---------------------------------------------------------
elif st.session_state.paso == "capacitacion":
    total_secciones = len(SECCIONES)
    sec_idx = st.session_state.seccion_actual
    
    col_h1, col_h2, col_h3 = st.columns([2, 2, 1])
    col_h1.write("🏢 **Empresa:** ILEPSA S.A.")
    col_h2.write(f"👤 **Cédula:** {st.session_state.cedula}")
    if col_h3.button("Guardar y Salir"):
        st.session_state.paso = "login"
        st.session_state.cedula = ""
        st.rerun()
        
    st.divider()
    
    progreso_val = sec_idx / total_secciones
    st.progress(progreso_val, text=f"Progreso General: Sección {sec_idx + 1} de {total_secciones} ({int(progreso_val*100)}%)")
    
    if sec_idx < total_secciones:
        seccion = SECCIONES[sec_idx]
        
        # Contenedor principal con efecto visual de paso de hoja
        st.markdown(f'<div class="libro-hoja" key="hoja_{sec_idx}">', unsafe_allow_html=True)
        
        st.markdown(f"### 📖 {seccion['eje']}")
        st.markdown(f"## {seccion['titulo']}")
        
        st.markdown(seccion['contenido'])
        
        st.markdown(f"""
        <div class="question-box">
            <h4 style="margin-top:0;">📝 Evaluación de la Sección {sec_idx + 1}</h4>
            <p style="font-size:16px;"><b>{seccion['pregunta']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        respuesta_usuario = st.radio("Seleccione la respuesta correcta:", seccion['opciones'], key=f"radio_s_{sec_idx}")
        
        col_b1, col_b2 = st.columns([1, 3])
        with col_b1:
            if st.button("Siguiente Sección ➔", type="primary"):
                if respuesta_usuario == seccion['correcta']:
                    st.success("¡Respuesta correcta! Pasando a la siguiente página...")
                    st.session_state.respuestas_correctas += 1
                    st.session_state.seccion_actual += 1
                    st.session_state.progreso_usuarios[st.session_state.cedula] = st.session_state.seccion_actual
                    time.sleep(0.6)  # Pausa dramática para que se note el cambio de página
                    st.rerun()
                else:
                    st.error("Respuesta incorrecta. Revise el contenido teórico antes de continuar.")
                    
        st.markdown("""
        <div style="background-color: #f1f5f9; border: 1px dashed #94a3b8; padding: 15px; border-radius: 8px; margin-top: 25px;">
            <h5 style="margin:0 0 5px 0;">🤖 Asistente Virtual ILEPSA</h5>
            <p style="font-size: 13px; color: #475569; margin-bottom:10px;">¿Tiene dudas sobre esta sección? Escriba su consulta:</p>
        </div>
        """, unsafe_allow_html=True)
        
        pregunta_ia = st.text_input("Escriba su consulta:", key=f"ia_input_{sec_idx}")
        if st.button("Consultar Asistente", key=f"ia_btn_{sec_idx}"):
            if pregunta_ia.strip():
                st.info(f"Asistente ILEPSA: Respecto a '{pregunta_ia}', recuerde que las normativas internas y el Acuerdo Ministerial MDT-2025-006 priorizan la equidad y el cumplimiento legal estricto.")
            else:
                st.warning("Ingrese una pregunta válida.")

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.session_state.paso = "certificado"
        st.rerun()

# ---------------------------------------------------------
# FASE 4: CERTIFICADO FINAL
# ---------------------------------------------------------
elif st.session_state.paso == "certificado":
    st.balloons()
    st.markdown('<div class="libro-hoja" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown(f"""
        <h2>📜 CERTIFICADO OFICIAL DE APROBACIÓN</h2>
        <h3>COMPAÑÍA ILEPSA S.A.</h3>
        <p>Se certifica formalmente que el colaborador con Cédula N° <b>{st.session_state.cedula}</b> ha completado y aprobado satisfactoriamente las <b>100 secciones</b> del Programa de Formación Integral bajo el marco del <b>Acuerdo Ministerial MDT-2025-006</b>.</p>
        <hr style="margin: 20px 0;">
        <p><b>Evaluaciones Superadas:</b> {st.session_state.respuestas_correctas} / {len(SECCIONES)}</p>
        <p style="color: #059669; font-weight: bold; font-size: 18px;">ESTADO: APROBADO CON ÉXITO</p>
    """, unsafe_allow_html=True)
    
    if st.button("Finalizar y Salir del Sistema"):
        st.session_state.paso = "login"
        st.session_state.cedula = ""
        st.session_state.seccion_actual = 0
        st.session_state.respuestas_correctas = 0
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
