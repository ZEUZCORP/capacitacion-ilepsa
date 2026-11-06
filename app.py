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

# Conexión limpia y segura usando st.secrets como lo configuramos
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
if "seccion_actual" not in st.session_state:
    st.session_state.seccion_actual = 0
if "respuestas_correctas" not in st.session_state:
    st.session_state.respuestas_correctas = 0

# Estilos CSS con animación de transición de página limpia
st.markdown("""
    <style>
    @keyframes fadeInSlide {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .nueva-pagina {
        animation: fadeInSlide 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
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

# Script para forzar el scroll al inicio absoluto en cada cambio de vista
components.html(
    """
    <script>
        const parentDoc = window.parent.document;
        parentDoc.querySelectorAll('section.main').forEach(el => el.scrollTo({top: 0, behavior: 'instant'}));
        window.parent.scrollTo({top: 0, behavior: 'instant'});
    </script>
    """,
    height=0,
)

# =========================================================
# FASE 1: LOGIN (Consulta directa a la tabla 'usuarios')
# =========================================================
if st.session_state.paso == "login":
    st.markdown("""
    <div class="nueva-pagina card-principal" style="text-align: center;">
        <h2 style="color: #0f172a; margin-top:0;">ACCESO COLABORADORES ILEPSA</h2>
        <p style="color: #64748b; margin-bottom: 0;">Ingrese su número de cédula para continuar</p>
    </div>
    """, unsafe_allow_html=True)
    
    cedula_input = st.text_input("Cédula de Identidad:", max_chars=10, type="password")
    
    if st.button("Ingresar al Sistema", type="primary", use_container_width=True):
        cedula_limpia = cedula_input.strip()
        if len(cedula_limpia) >= 10:
            try:
                # Consulta real a Supabase trayendo el campo 'nombres' desde la tabla 'usuarios'
                response = supabase.table("usuarios").select("nombres").eq("cedula", cedula_limpia).execute()
                
                if response.data and len(response.data) > 0:
                    st.session_state.cedula = cedula_limpia
                    st.session_state.nombre_usuario = response.data[0]["nombres"]
                    
                    # Traqueo y registro de horas en la tabla 'registro_tiempos'
                    try:
                        supabase.table("registro_tiempos").insert({
                            "cedula": cedula_limpia,
                            "fecha_ingreso": datetime.now().isoformat()
                        }).execute()
                    except Exception:
                        pass
                    
                    st.session_state.paso = "instrucciones"
                    st.rerun()
                else:
                    st.error("Cédula no registrada en la base de datos de ILEPSA.")
            except Exception as e:
                st.error(f"Error de conexión con Supabase: {e}")
        else:
            st.error("Ingrese un número de cédula válido de 10 dígitos.")

# =========================================================
# FASE 2: INSTRUCCIONES Y MARCO LEGAL (Bienvenida)
# =========================================================
elif st.session_state.paso == "instrucciones":
    st.markdown(f"""
    <div class="nueva-pagina card-principal">
        <h3 style="color: #0f172a; margin-top:0;">¡Bienvenido(a), {st.session_state.nombre_usuario}!</h3>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 15px 0;">
        <p style="font-size: 15px; color: #334155; line-height: 1.6;">
            En cumplimiento con la normativa legal vigente y el <b>Acuerdo Ministerial MDT-2025-006</b>, este programa de formación integral es de <b>carácter obligatorio</b> para todo el personal de la Compañía ILEPSA S.A.
        </p>
        <p style="font-size: 15px; color: #334155; line-height: 1.6;">
            <b>¿De qué se trata?</b> El programa está diseñado para promover un entorno laboral seguro, equitativo, inclusivo y estrictamente libre de violencia y discriminación en el ámbito de trabajo.
        </p>
        <p style="font-size: 15px; color: #334155; line-height: 1.6;">
            <b>Directrices importantes:</b>
        </p>
        <ul style="color: #334155; font-size: 15px;">
            <li>Debe completar obligatoriamente las secciones establecidas en el cronograma.</li>
            <li>Cada sección consta de contenido teórico y una evaluación interactiva de validación.</li>
            <li>Su avance se registra de manera centralizada en el sistema de la empresa.</li>
            <li><b>Al completar el 100% de las secciones, el sistema le habilitará de forma automática su certificado oficial de aprobación.</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Comenzar Capacitación ➔", type="primary", use_container_width=True):
        st.session_state.paso = "evaluacion"
        st.session_state.seccion_actual = 0
        st.rerun()

# =========================================================
# FASE 3: MÓDULO DE CAPACITACIÓN (SECCIÓN POR SECCIÓN RECREADA)
# =========================================================
elif st.session_state.paso == "evaluacion":
    total_secciones = len(SECCIONES)
    sec_idx = st.session_state.seccion_actual

    if sec_idx < total_secciones:
        seccion = SECCIONES[sec_idx]
        
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
        
        # CONTENEDOR RECREADO COMO UNA PÁGINA TOTALMENTE NUEVA
        st.markdown(f"""
        <div class="nueva-pagina card-principal">
            <span style="color: #0284c7; font-weight: bold; font-size: 14px;">{seccion['eje']}</span>
            <h2 style="margin-top: 5px; color: #0f172a;">{seccion['titulo']}</h2>
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 15px 0;">
            <div style="font-size: 16px; line-height: 1.6; color: #334155;">
                {seccion['contenido']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="nueva-pagina pregunta-box">
            <h4 style="margin-top:0; color: #0f172a;">Evaluación Obligatoria</h4>
            <p style="font-size: 16px; font-weight: 600; color: #1e293b;">{seccion['pregunta']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        respuesta = st.radio(
            "Seleccione la respuesta correcta para continuar:", 
            seccion['opciones'], 
            key=f"radio_seccion_aislada_{sec_idx}"
        )
        
        if st.button("Siguiente Sección ➔", type="primary", key=f"btn_siguiente_pagina_{sec_idx}", use_container_width=True):
            if respuesta == seccion['correcta']:
                st.session_state.respuestas_correctas += 1
                st.session_state.seccion_actual += 1
                
                with st.spinner(f"Cargando la siguiente página ({st.session_state.seccion_actual + 1}/{total_secciones})..."):
                    time.sleep(0.3)
                st.rerun()
            else:
                st.error("Respuesta incorrecta. Debe revisar detenidamente la teoría de esta página para poder avanzar.")
    else:
        st.session_state.paso = "certificado"
        st.rerun()

# =========================================================
# FASE 4: CERTIFICADO FINAL
# =========================================================
elif st.session_state.paso == "certificado":
    st.balloons()
    st.markdown(f"""
    <div class="nueva-pagina card-principal" style="text-align: center;">
        <h2 style="color: #0f172a;">📜 CERTIFICADO OFICIAL DE APROBACIÓN</h2>
        <h4 style="color: #0284c7;">COMPAÑÍA ILEPSA S.A.</h4>
        <p>Se otorga el presente certificado oficial bajo el marco del <b>Acuerdo Ministerial MDT-2025-006</b> a:</p>
        <h3 style="color: #0f172a; text-decoration: underline;">{st.session_state.nombre_usuario}</h3>
        <p>Con Cédula N° <b>{st.session_state.cedula}</b> por haber completado y aprobado satisfactoriamente las 100 secciones del programa.</p>
        <hr style="margin: 20px 0;">
        <p><b>Calificación Final:</b> {st.session_state.respuestas_correctas} / {len(SECCIONES)} aciertos.</p>
        <p style="color: #059669; font-weight: bold; font-size: 18px;">ESTADO: APROBADO CON ÉXITO</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("¡Felicitaciones! Su aprobación ha sido registrada con éxito en la base de datos de ILEPSA.")
    
    if st.button("Finalizar y Salir"):
        st.session_state.paso = "login"
        st.session_state.cedula = ""
        st.session_state.nombre_usuario = ""
        st.session_state.seccion_actual = 0
        st.rerun()
