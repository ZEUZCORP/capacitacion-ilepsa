import streamlit as st
import streamlit.components.v1 as components
import time
from contenidos import SECCIONES

st.set_page_config(
    page_title="Plataforma de Capacitación - ILEPSA",
    page_icon="🏢",
    layout="centered"
)

# Base de datos simulada de nombres de colaboradores asociados a su cédula
# Puedes actualizar o ampliar este diccionario con los nombres reales de ILEPSA
NOMBRES_COLABORADORES = {
    "9999999999": "Super Administrador ILEPSA",
    # Ejemplos de cédulas (puedes agregar más aquí):
    "1712345678": "Juan Carlos Pérez",
    "1787654321": "María Fernanda Andrade",
}

# Inicializar estados de sesión
if "paso" not in st.session_state:
    st.session_state.paso = "login"  # login, cargando, capacitacion, certificado
if "cedula" not in st.session_state:
    st.session_state.cedula = ""
if "nombre_usuario" not in st.session_state:
    st.session_state.nombre_usuario = ""
if "seccion_actual" not in st.session_state:
    st.session_state.seccion_actual = 0
if "respuestas_correctas" not in st.session_state:
    st.session_state.respuestas_correctas = 0
if "progreso_usuarios" not in st.session_state:
    st.session_state.progreso_usuarios = {}

# Estilos CSS con animación de volteo de página de libro (Page Flip 3D)
st.markdown("""
    <style>
    @keyframes flipPage3D {
        0% {
            opacity: 0;
            transform: perspective(1200px) rotateY(-18deg) translateX(-40px);
            filter: blur(4px);
        }
        50% {
            opacity: 0.6;
            filter: blur(1px);
        }
        100% {
            opacity: 1;
            transform: perspective(1200px) rotateY(0deg) translateX(0px);
            filter: blur(0px);
        }
    }

    .hoja-libro-animada {
        animation: flipPage3D 0.65s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 8px solid #0284c7;
        padding: 35px;
        border-radius: 12px;
        box-shadow: 12px 12px 30px rgba(0,0,0,0.08);
        margin-bottom: 30px;
    }

    .welcome-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 40px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        margin-bottom: 25px;
    }

    .header-info-box {
        background: linear-gradient(90deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 15px 20px;
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        margin-bottom: 20px;
    }

    .question-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #0284c7;
        padding: 22px;
        border-radius: 8px;
        margin-top: 25px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FASE 1: INGRESO DE CÉDULA ÚNICAMENTE
# ---------------------------------------------------------
if st.session_state.paso == "login":
    st.markdown("""
    <div class="welcome-card">
        <h1 style="color: #ffffff; margin-top: 0; font-size: 28px;">PROGRAMA DE FORMACIÓN INTEGRAL</h1>
        <h3 style="color: #38bdf8; margin-bottom: 10px;">COMPAÑÍA ILEPSA S.A.</h3>
        <p style="opacity: 0.9; font-size: 15px;">Cumplimiento Normativo — Acuerdo Ministerial MDT-2025-006</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hoja-libro-animada">
        <h4 style="margin-top:0; color: #0f172a;">📋 Acceso al Sistema de Capacitación</h4>
        <p style="color: #475569; font-size: 14px;">Ingrese su número de Cédula de Identidad para iniciar la sesión y recuperar su progreso guardado automáticamente.</p>
    </div>
    """, unsafe_allow_html=True)
    
    cedula_input = st.text_input("Ingrese su Cédula de Identidad:", max_chars=10, type="password")
    
    if st.button("Ingresar al Sistema", type="primary"):
        cedula_limpia = cedula_input.strip()
        
        if len(cedula_limpia) >= 10:
            st.session_state.cedula = cedula_limpia
            # Buscar el nombre correspondiente o asignar uno genérico si es nuevo colaborador
            if cedula_limpia in NOMBRES_COLABORADORES:
                st.session_state.nombre_usuario = NOMBRES_COLABORADORES[cedula_limpia]
            else:
                st.session_state.nombre_usuario = f"Colaborador ILEPSA (C.I. {cedula_limpia})"
                
            st.session_state.paso = "cargando"
            st.rerun()
        else:
            st.error("Por favor ingrese un número de cédula válido de 10 dígitos.")

# ---------------------------------------------------------
# FASE 2: PANTALLA DE BIENVENIDA Y CARGA DE PÁGINA
# ---------------------------------------------------------
elif st.session_state.paso == "cargando":
    st.markdown(f"""
    <div class="welcome-card">
        <h1 style="color: #38bdf8; margin-bottom: 10px;">¡BIENVENIDO(A) A ILEPSA!</h1>
        <h2 style="color: #ffffff; margin-top: 0;">{st.session_state.nombre_usuario}</h2>
        <p style="font-size: 15px; color: #cbd5e1;">Cédula de Identidad: N° {st.session_state.cedula}</p>
        <p style="font-size: 14px; color: #94a3b8; margin-top: 20px;">Abriendo libro digital de capacitación y recuperando registro de avance...</p>
    </div>
    """, unsafe_allow_html=True)
    
    barra_carga = st.progress(0, text="Cargando libro digital...")
    for porcentaje in range(1, 101):
        time.sleep(0.02)
        if porcentaje == 30:
            barra_carga.progress(porcentaje, text="Validando perfil de colaborador en ILEPSA S.A. ...")
        elif porcentaje == 70:
            barra_carga.progress(porcentaje, text="Recuperando la última sección completada...")
        elif porcentaje == 100:
            barra_carga.progress(porcentaje, text="¡Página lista! Trasladando a la sección de lectura...")

    time.sleep(0.4)
    
    if st.session_state.cedula in st.session_state.progreso_usuarios:
        st.session_state.seccion_actual = st.session_state.progreso_usuarios[st.session_state.cedula]
    else:
        st.session_state.seccion_actual = 0
        
    st.session_state.paso = "capacitacion"
    st.rerun()

# ---------------------------------------------------------
# FASE 3: DESARROLLO DE LA CAPACITACIÓN (TRANSICIÓN TIPO LIBRO)
# ---------------------------------------------------------
elif st.session_state.paso == "capacitacion":
    total_secciones = len(SECCIONES)
    sec_idx = st.session_state.seccion_actual
    
    # Inyección de JavaScript que obliga a la ventana principal a subir completamente al inicio
    components.html(
        """
        <script>
            window.parent.scrollTo({top: 0, behavior: 'instant'});
        </script>
        """,
        height=0,
    )
    
    # Barra superior mostrando claramente la empresa, el NOMBRE y la CÉDULA
    st.markdown(f"""
    <div class="header-info-box">
        <table style="width:100%; border:none; margin:0;">
            <tr>
                <td style="border:none; font-size:14px;">🏢 <b>Empresa:</b> ILEPSA S.A.</td>
                <td style="border:none; font-size:14px;">👤 <b>Colaborador:</b> {st.session_state.nombre_usuario}</td>
                <td style="border:none; font-size:14px;">🪪 <b>Cédula:</b> {st.session_state.cedula}</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    col_sal1, col_sal2 = st.columns([4, 1])
    with col_sal2:
        if st.button("Guardar y Salir"):
            st.session_state.paso = "login"
            st.session_state.cedula = ""
            st.session_state.nombre_usuario = ""
            st.rerun()
            
    st.divider()
    
    progreso_val = sec_idx / total_secciones
    st.progress(progreso_val, text=f"Progreso General: Sección {sec_idx + 1} de {total_secciones} ({int(progreso_val*100)}%)")
    
    if sec_idx < total_secciones:
        seccion = SECCIONES[sec_idx]
        
        # El atributo key fuerza a Streamlit a destruir la vista anterior y animar la nueva hoja
        st.markdown(f'<div class="hoja-libro-animada" key="pagina_libro_{sec_idx}_{time.time()}">', unsafe_allow_html=True)
        
        st.markdown(f"### 📖 {seccion['eje']}")
        st.markdown(f"## {seccion['titulo']}")
        
        # Texto de Lectura Obligatoria
        st.markdown(seccion['contenido'])
        
        st.divider()
        
        # Bloque de Evaluación en la parte inferior de la página
        st.markdown(f"""
        <div class="question-box">
            <h4 style="margin-top:0;">📝 Evaluación Obligatoria de la Sección {sec_idx + 1}</h4>
            <p style="font-size:16px;"><b>{seccion['pregunta']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        respuesta_usuario = st.radio("Seleccione su respuesta para avanzar de página:", seccion['opciones'], key=f"radio_choice_{sec_idx}")
        
        col_b1, col_b2 = st.columns([1, 3])
        with col_b1:
            if st.button("Pasar de Página ➔", type="primary"):
                if respuesta_usuario == seccion['correcta']:
                    st.success("¡Respuesta correcta! Volteando hoja del libro...")
                    st.session_state.respuestas_correctas += 1
                    st.session_state.seccion_actual += 1
                    st.session_state.progreso_usuarios[st.session_state.cedula] = st.session_state.seccion_actual
                    time.sleep(0.5)  # Pausa deliberada para ver el paso de página
                    st.rerun()
                else:
                    st.error("Respuesta incorrecta. Vuelva a leer el texto superior antes de intentar de nuevo.")
                    
        st.markdown("""
        <div style="background-color: #f1f5f9; border: 1px dashed #94a3b8; padding: 15px; border-radius: 8px; margin-top: 25px;">
            <h5 style="margin:0 0 5px 0;">🤖 Asistente Virtual ILEPSA</h5>
            <p style="font-size: 13px; color: #475569; margin-bottom:10px;">¿Tiene dudas sobre este tema? Escriba su consulta a continuación:</p>
        </div>
        """, unsafe_allow_html=True)
        
        pregunta_ia = st.text_input("Escriba su consulta:", key=f"ia_input_sec_{sec_idx}")
        if st.button("Consultar Asistente", key=f"ia_btn_sec_{sec_idx}"):
            if pregunta_ia.strip():
                st.info(f"Asistente ILEPSA: Respecto a '{pregunta_ia}', el marco legal del MDT-2025-006 garantiza el cumplimiento estricto de los derechos de los colaboradores.")
            else:
                st.warning("Ingrese una consulta válida.")

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.session_state.paso = "certificado"
        st.rerun()

# ---------------------------------------------------------
# FASE 4: CERTIFICADO OFICIAL FINAL
# ---------------------------------------------------------
elif st.session_state.paso == "certificado":
    st.balloons()
    st.markdown('<div class="hoja-libro-animada" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown(f"""
        <h2>📜 CERTIFICADO OFICIAL DE APROBACIÓN</h2>
        <h3>COMPAÑÍA ILEPSA S.A.</h3>
        <p>Se certifica que el colaborador(a):</p>
        <h3 style="color:#0284c7;">{st.session_state.nombre_usuario}</h3>
        <p>Con Cédula de Identidad N° <b>{st.session_state.cedula}</b> ha completado y aprobado satisfactoriamente las <b>100 secciones</b> del Programa de Formación Integral bajo el marco del <b>Acuerdo Ministerial MDT-2025-006</b>.</p>
        <hr style="margin: 20px 0;">
        <p><b>Aciertos Totales:</b> {st.session_state.respuestas_correctas} / {len(SECCIONES)}</p>
        <p style="color: #059669; font-weight: bold; font-size: 18px;">ESTADO: CERTIFICADO EMITIDO Y REGISTRADO</p>
    """, unsafe_allow_html=True)
    
    if st.button("Finalizar y Salir del Sistema"):
        st.session_state.paso = "login"
        st.session_state.cedula = ""
        st.session_state.nombre_usuario = ""
        st.session_state.seccion_actual = 0
        st.session_state.respuestas_correctas = 0
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
