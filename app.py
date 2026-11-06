import streamlit as st
import streamlit.components.v1 as components
import time
from contenidos import SECCIONES

st.set_page_config(
    page_title="Plataforma ILEPSA",
    page_icon="🏢",
    layout="centered"
)

# Diccionario de nombres por cédula
NOMBRES_COLABORADORES = {
    "9999999999": "Super Administrador ILEPSA",
    "1712345678": "Juan Carlos Pérez",
    "1787654321": "María Fernanda Andrade",
}

# Inicializar memoria de sesión
if "paso" not in st.session_state:
    st.session_state.paso = "login"
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

# Estilos corporativos limpios y elegantes
st.markdown("""
    <style>
    .card-principal {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 5px solid #0284c7;
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

# ---------------------------------------------------------
# 1. PANTALLA DE LOGIN (MINIMALISTA)
# ---------------------------------------------------------
if st.session_state.paso == "login":
    st.markdown("""
    <div class="card-principal" style="text-align: center;">
        <h2 style="color: #0f172a; margin-top:0;">ACCESO COLABORADORES ILEPSA</h2>
        <p style="color: #64748b; margin-bottom: 0;">Ingrese su número de documento para continuar</p>
    </div>
    """, unsafe_allow_html=True)
    
    cedula_input = st.text_input("Cédula de Identidad:", max_chars=10, type="password")
    
    if st.button("Ingresar al Sistema", type="primary", use_container_width=True):
        cedula_limpia = cedula_input.strip()
        if len(cedula_limpia) >= 10:
            st.session_state.cedula = cedula_limpia
            st.session_state.nombre_usuario = NOMBRES_COLABORADORES.get(cedula_limpia, f"Colaborador C.I. {cedula_limpia}")
            
            if cedula_limpia in st.session_state.progreso_usuarios:
                st.session_state.seccion_actual = st.session_state.progreso_usuarios[cedula_limpia]
            else:
                st.session_state.seccion_actual = 0
                
            st.session_state.paso = "instrucciones"
            st.rerun()
        else:
            st.error("Ingrese un número de cédula válido de 10 dígitos.")

# ---------------------------------------------------------
# 2. MENSAJE OBLIGATORIO Y DE DIRECTRICES
# ---------------------------------------------------------
elif st.session_state.paso == "instrucciones":
    st.markdown(f"""
    <div class="card-principal">
        <h3 style="color: #0f172a; margin-top:0;">¡Bienvenido(a), {st.session_state.nombre_usuario}!</h3>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 15px 0;">
        <p style="font-size: 15px; color: #334155; line-height: 1.6;">
            Este programa de formación corporativa es de <b>carácter obligatorio</b> para todo el personal de la compañía. Su cumplimiento y aprobación forman parte de las directrices institucionales vigentes.
        </p>
        <p style="font-size: 15px; color: #334155; line-height: 1.6;">
            <b>Instrucciones importantes:</b>
        </p>
        <ul style="color: #334155; font-size: 15px;">
            <li>Debe completar las secciones diarias establecidas en su cronograma.</li>
            <li>Cada sección cuenta con una lectura teórica y una evaluación obligatoria al finalizar.</li>
            <li>Su avance se guarda de forma automática; si sale, podrá retomar exactamente donde se quedó.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Comenzar Capacitación ➔", type="primary", use_container_width=True):
        st.session_state.paso = "evaluacion"
        st.rerun()

# ---------------------------------------------------------
# 3. PANTALLA DE CAPACITACIÓN (ORDENADA Y LIMPIA)
# ---------------------------------------------------------
elif st.session_state.paso == "evaluacion":
    # Forzar scroll automático al inicio de la página
    components.html(
        """
        <script>
            window.parent.scrollTo({top: 0, behavior: 'instant'});
        </script>
        """,
        height=0,
    )
    
    total_secciones = len(SECCIONES)
    sec_idx = st.session_state.seccion_actual
    
    # Encabezado fijo limpio
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
    
    col_s1, col_s2 = st.columns([5, 1])
    with col_s2:
        if st.button("Salir"):
            st.session_state.paso = "login"
            st.rerun()
            
    progreso = sec_idx / total_secciones
    st.progress(progreso, text=f"Progreso actual: Sección {sec_idx + 1} de {total_secciones}")
    
    if sec_idx < total_secciones:
        seccion = SECCIONES[sec_idx]
        
        # Contenido teórico limpio sin etiquetas rotas
        st.markdown(f"""
        <div class="card-principal">
            <span style="color: #0284c7; font-weight: bold; font-size: 14px;">{seccion['eje']}</span>
            <h2 style="margin-top: 5px; color: #0f172a;">{seccion['titulo']}</h2>
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 15px 0;">
            <div style="font-size: 16px; line-height: 1.6; color: #334155;">
                {seccion['contenido']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Evaluación de la sección
        st.markdown(f"""
        <div class="pregunta-box">
            <h4 style="margin-top:0; color: #0f172a;">Evaluación Obligatoria</h4>
            <p style="font-size: 16px; font-weight: 600; color: #1e293b;">{seccion['pregunta']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form(key=f"form_seccion_{sec_idx}"):
            respuesta = st.radio("Seleccione la respuesta correcta:", seccion['opciones'])
            
            submitted = st.form_submit_button("Siguiente Sección ➔", type="primary")
            if submitted:
                if respuesta == seccion['correcta']:
                    st.session_state.respuestas_correctas += 1
                    st.session_state.seccion_actual += 1
                    st.session_state.progreso_usuarios[st.session_state.cedula] = st.session_state.seccion_actual
                    st.success("¡Respuesta correcta! Cargando la siguiente sección...")
                    time.sleep(0.3)
                    st.rerun()
                else:
                    st.error("Respuesta incorrecta. Revise detenidamente la lectura teórica superior e intente de nuevo.")
    else:
        st.session_state.paso = "certificado"
        st.rerun()

# ---------------------------------------------------------
# 4. CERTIFICADO FINAL
# ---------------------------------------------------------
elif st.session_state.paso == "certificado":
    st.balloons()
    st.markdown(f"""
    <div class="card-principal" style="text-align: center;">
        <h2 style="color: #0f172a;">📜 CERTIFICADO OFICIAL DE APROBACIÓN</h2>
        <h4 style="color: #0284c7;">COMPAÑÍA ILEPSA S.A.</h4>
        <p>Se otorga el presente certificado a:</p>
        <h3 style="color: #0f172a; text-decoration: underline;">{st.session_state.nombre_usuario}</h3>
        <p>Con Cédula N° <b>{st.session_state.cedula}</b> por haber completado y aprobado con éxito las 100 secciones del programa de formación obligatoria.</p>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;">
        <p><b>Calificación Final:</b> {st.session_state.respuestas_correctas} / {len(SECCIONES)} aciertos.</p>
        <p style="color: #059669; font-weight: bold;">ESTADO: APROBADO CON ÉXITO</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Finalizar y Salir"):
        st.session_state.paso = "login"
        st.session_state.cedula = ""
        st.session_state.nombre_usuario = ""
        st.session_state.seccion_actual = 0
        st.rerun()
