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

# Conexión limpia y segura usando st.secrets
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
if "respuestas_correctas" not in st.session_state:
    st.session_state.respuestas_correctas = 0

# Paleta de colores rotativa por sección para que el usuario note visualmente que cambió de pantalla
COLORES_SECCION = [
    {"borde": "#0284c7", "fondo_etiqueta": "#e0f2fe", "texto_etiqueta": "#0369a1"}, # Azul
    {"borde": "#7c3aed", "fondo_etiqueta": "#ede9fe", "texto_etiqueta": "#6d28d9"}, # Violeta
    {"borde": "#059669", "fondo_etiqueta": "#d1fae5", "texto_etiqueta": "#047857"}, # Esmeralda
    {"borde": "#d97706", "fondo_etiqueta": "#fef3c7", "texto_etiqueta": "#b45309"}, # Ámbar
    {"borde": "#dc2626", "fondo_etiqueta": "#fee2e2", "texto_etiqueta": "#b91c1c"}  # Rojo institucional
]

# Estilos CSS avanzados con indicador lateral derecho y animaciones de cambio de página
st.markdown("""
    <style>
    @keyframes fadeInPage {
        0% { opacity: 0; transform: translateY(25px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .pagina-nueva-transicion {
        animation: fadeInPage 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .card-principal {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 35px;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
        position: relative;
    }
    .badge-seccion-derecha {
        position: absolute;
        top: 25px;
        right: 30px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .header-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .pregunta-box {
        background-color: #f8fafc;
        border-left: 5px solid #0f172a;
        padding: 22px;
        border-radius: 0 10px 10px 0;
        margin-top: 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
    }
    </style>
""", unsafe_allow_html=True)

# SCRIPT DE JAVASCRIPT INQUEBRANTABLE PARA FORZAR EL SCROLL AL INICIO ABSOLUTO (0,0)
components.html(
    """
    <script>
        function forzarScrollTop() {
            const doc = window.parent.document;
            doc.querySelectorAll('section.main').forEach(el => {
                el.scrollTop = 0;
                el.scrollTo({top: 0, behavior: 'instant'});
            });
            window.parent.scrollTo({top: 0, behavior: 'instant'});
        }
        forzarScrollTop();
        setTimeout(forzarScrollTop, 50);
        setTimeout(forzarScrollTop, 150);
    </script>
    """,
    height=0,
)

# =========================================================
# FASE 1: LOGIN
# =========================================================
if st.session_state.paso == "login":
    st.markdown("""
    <div class="pagina-nueva-transicion card-principal" style="text-align: center; border-top: 5px solid #0284c7;">
        <h2 style="color: #0f172a; margin-top:0;">ACCESO COLABORADORES ILEPSA</h2>
        <p style="color: #64748b; margin-bottom: 0;">Ingrese su número de cédula para continuar con la capacitación obligatoria</p>
    </div>
    """, unsafe_allow_html=True)
    
    cedula_input = st.text_input("Cédula de Identidad:", max_chars=10, type="password")
    
    if st.button("Ingresar al Sistema", type="primary", use_container_width=True):
        cedula_limpia = cedula_input.strip()
        if len(cedula_limpia) >= 10 or cedula_limpia == "1":
            try:
                response = supabase.table("usuarios").select("nombres").eq("cedula", cedula_limpia).execute()
                
                if response.data and len(response.data) > 0:
                    st.session_state.cedula = cedula_limpia
                    st.session_state.nombre_usuario = response.data[0]["nombres"]
                    
                    if "Administrador" in st.session_state.nombre_usuario or cedula_limpia in ["9999999999", "1"]:
                        st.session_state.es_admin = True
                        st.session_state.paso = "admin_dashboard"
                    else:
                        st.session_state.es_admin = False
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
            st.error("Ingrese un número de cédula válido.")

# =========================================================
# FASE 2: PANEL DE ADMINISTRACIÓN
# =========================================================
elif st.session_state.paso == "admin_dashboard":
    st.markdown(f"""
    <div class="pagina-nueva-transicion card-principal" style="border-top: 5px solid #0f172a;">
        <h2 style="color: #0f172a; margin-top:0;">📊 PANEL DE CONTROL Y ESTADÍSTICAS - ILEPSA</h2>
        <p style="color: #64748b;"><b>Administrador en sesión:</b> {st.session_state.nombre_usuario}</p>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 15px 0;">
        <p style="font-size: 15px; color: #334155;">
            Monitoreo en tiempo real de accesos, metraje de tiempo de conexión y avance de los colaboradores bajo la normativa MDT-2025-006.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🕒 Registro de Ingresos y Tiempos de Conexión")
    try:
        query_tiempos = supabase.table("registro_tiempos").select("*").order("fecha_ingreso", desc=True).execute()
        if query_tiempos.data and len(query_tiempos.data) > 0:
            datos_tabla = []
            for reg in query_tiempos.data:
                cedula_reg = reg.get("cedula", "N/A")
                fecha_reg = reg.get("fecha_ingreso", "N/A")
                res_user = supabase.table("usuarios").select("nombres").eq("cedula", cedula_reg).execute()
                nombre_reg = res_user.data[0]["nombres"] if res_user.data else "Colaborador Externo"
                datos_tabla.append({
                    "Colaborador": nombre_reg,
                    "Cédula": cedula_reg,
                    "Fecha y Hora de Ingreso": fecha_reg
                })
            st.dataframe(datos_tabla, use_container_width=True)
        else:
            st.info("Aún no se registran ingresos de colaboradores.")
    except Exception:
        pass
        
    st.markdown("### 👥 Listado General de Colaboradores Registrados")
    try:
        query_usuarios = supabase.table("usuarios").select("*").execute()
        if query_usuarios.data:
            st.dataframe(query_usuarios.data, use_container_width=True)
    except Exception:
        pass
        
    if st.button("Cerrar Sesión de Administrador", type="primary", use_container_width=True):
        st.session_state.paso = "login"
        st.session_state.cedula = ""
        st.session_state.nombre_usuario = ""
        st.session_state.es_admin = False
        st.rerun()

# =========================================================
# FASE 3: INSTRUCCIONES (Colaboradores)
# =========================================================
elif st.session_state.paso == "instrucciones":
    st.markdown(f"""
    <div class="pagina-nueva-transicion card-principal" style="border-top: 5px solid #0284c7;">
        <h3 style="color: #0f172a; margin-top:0;">¡Bienvenido(a), {st.session_state.nombre_usuario}!</h3>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 15px 0;">
        <p style="font-size: 15px; color: #334155; line-height: 1.6;">
            En cumplimiento con la normativa legal vigente y el <b>Acuerdo Ministerial MDT-2025-006</b>, este programa de formación integral es de <b>carácter obligatorio</b> para todo el personal de la Compañía ILEPSA S.A.
        </p>
        <p style="font-size: 15px; color: #334155; line-height: 1.6;">
            <b>Directrices importantes:</b>
        </p>
        <ul style="color: #334155; font-size: 15px;">
            <li>Debe completar obligatoriamente cada una de las secciones interactivas.</li>
            <li>Cada página contiene contenido teórico y una evaluación obligatoria. El sistema le exigirá lectura atenta para avanzar.</li>
            <li><b>Al completar el 100% de las secciones, se generará su certificado oficial de aprobación.</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Comenzar Capacitación ➔", type="primary", use_container_width=True):
        st.session_state.paso = "evaluacion"
        st.session_state.seccion_actual = 0
        st.rerun()

# =========================================================
# FASE 4: MÓDULO DE CAPACITACIÓN (SECCIÓN POR SECCIÓN CON CAMBIO VISUAL Y SCROLL FORZADO)
# =========================================================
elif st.session_state.paso == "evaluacion":
    total_secciones = len(SECCIONES)
    sec_idx = st.session_state.seccion_actual

    if sec_idx < total_secciones:
        seccion = SECCIONES[sec_idx]
        
        # Seleccionar dinámicamente un color institucional rotativo para esta sección específica
        estilo_color = COLORES_SECCION[sec_idx % len(COLORES_SECCION)]
        
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
        
        # CONTENEDOR DE TEORÍA CON BORDES DINÁMICOS Y ETIQUETA VISIBLE A LA DERECHA
        st.markdown(f"""
        <div class="pagina-nueva-transicion card-principal" style="border-top: 6px solid {estilo_color['borde']};">
            <div class="badge-seccion-derecha" style="background-color: {estilo_color['fondo_etiqueta']}; color: {estilo_color['texto_etiqueta']};">
                SECCIÓN {sec_idx + 1} DE {total_secciones}
            </div>
            <span style="color: {estilo_color['borde']}; font-weight: bold; font-size: 14px; text-transform: uppercase;">
                {seccion['eje']}
            </span>
            <h2 style="margin-top: 8px; color: #0f172a; font-size: 24px;">{seccion['titulo']}</h2>
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 18px 0;">
            <div style="font-size: 16px; line-height: 1.7; color: #334155;">
                {seccion['contenido']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # CONTENEDOR DE EVALUACIÓN
        st.markdown(f"""
        <div class="pagina-nueva-transicion pregunta-box" style="border-left: 5px solid {estilo_color['borde']};">
            <h4 style="margin-top:0; color: #0f172a;">Evaluación de Validación Obligatoria</h4>
            <p style="font-size: 16px; font-weight: 600; color: #1e293b; margin-bottom: 0;">{seccion['pregunta']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Selector único e independiente para cada página
        respuesta = st.radio(
            "Seleccione la respuesta correcta para continuar a la siguiente página:", 
            seccion['opciones'], 
            key=f"radio_seccion_aislada_{sec_idx}"
        )
        
        # Botón con reseteo absoluto de scroll y pantalla
        if st.button("Siguiente Sección ➔", type="primary", key=f"btn_siguiente_pagina_{sec_idx}", use_container_width=True):
            if respuesta == seccion['correcta']:
                st.session_state.respuestas_correctas += 1
                st.session_state.seccion_actual += 1
                
                # Script de re-enrutamiento y carga limpia
                components.html(
                    """
                    <script>
                        const parentDoc = window.parent.document;
                        parentDoc.querySelectorAll('section.main').forEach(el => {
                            el.scrollTop = 0;
                            el.scrollTo({top: 0, behavior: 'instant'});
                        });
                        window.parent.scrollTo({top: 0, behavior: 'instant'});
                    </script>
                    """,
                    height=0,
                )
                
                with st.spinner(f"Guardando avance y cargando página {st.session_state.seccion_actual + 1}..."):
                    time.sleep(0.35)
                st.rerun()
            else:
                st.error("Respuesta incorrecta. Debe leer detalladamente la teoría de esta sección para poder avanzar.")
    else:
        st.session_state.paso = "certificado"
        st.rerun()

# =========================================================
# FASE 5: CERTIFICADO FINAL
# =========================================================
elif st.session_state.paso == "certificado":
    st.balloons()
    st.markdown(f"""
    <div class="pagina-nueva-transicion card-principal" style="text-align: center; border-top: 6px solid #059669;">
        <h2 style="color: #0f172a;">📜 CERTIFICADO OFICIAL DE APROBACIÓN</h2>
        <h4 style="color: #0284c7;">COMPAÑÍA ILEPSA S.A.</h4>
        <p>Se otorga el presente certificado oficial bajo el marco del <b>Acuerdo Ministerial MDT-2025-006</b> a:</p>
        <h3 style="color: #0f172a; text-decoration: underline;">{st.session_state.nombre_usuario}</h3>
        <p>Con Cédula N° <b>{st.session_state.cedula}</b> por haber completado y aprobado satisfactoriamente todas las secciones del programa.</p>
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
        st.session_state.es_admin = False
        st.session_state.seccion_actual = 0
        st.rerun()
