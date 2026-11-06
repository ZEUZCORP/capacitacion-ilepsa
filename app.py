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
if "sub_paso" not in st.session_state:
    st.session_state.sub_paso = "teoria"
if "respuestas_correctas" not in st.session_state:
    st.session_state.respuestas_correctas = 0

# Paleta de colores rotativa por sección
COLORES_SECCION = [
    {"borde": "#0284c7", "fondo_etiqueta": "#e0f2fe", "texto_etiqueta": "#0369a1"},
    {"borde": "#7c3aed", "fondo_etiqueta": "#ede9fe", "texto_etiqueta": "#6d28d9"},
    {"borde": "#059669", "fondo_etiqueta": "#d1fae5", "texto_etiqueta": "#047857"},
    {"borde": "#d97706", "fondo_etiqueta": "#fef3c7", "texto_etiqueta": "#b45309"},
    {"borde": "#dc2626", "fondo_etiqueta": "#fee2e2", "texto_etiqueta": "#b91c1c"}
]

# Estilos CSS con tipografía compacta, elegante y estructurada
st.markdown("""
    <style>
    @keyframes fadeInPage {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .pagina-nueva-transicion {
        animation: fadeInPage 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .card-principal {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 25px 30px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
        position: relative;
    }
    .badge-seccion-derecha {
        position: absolute;
        top: 20px;
        right: 25px;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .header-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 10px 18px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .contenido-texto {
        font-size: 14.5px;
        line-height: 1.6;
        color: #334155;
    }
    .pregunta-box {
        background-color: #f8fafc;
        border-left: 4px solid #0f172a;
        padding: 20px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .certificado-container {
        background: #fff;
        border: 8px double #0f172a;
        padding: 40px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Script para forzar el scroll al inicio absoluto (0,0)
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
# FASE 1: LOGIN (Recupera progreso automático de Supabase)
# =========================================================
if st.session_state.paso == "login":
    st.markdown("""
    <div class="pagina-nueva-transicion card-principal" style="text-align: center; border-top: 5px solid #0284c7;">
        <h3 style="color: #0f172a; margin-top:0;">ACCESO COLABORADORES ILEPSA</h3>
        <p style="color: #64748b; font-size: 14px; margin-bottom: 0;">Ingrese su número de cédula para continuar con su capacitación guardada</p>
    </div>
    """, unsafe_allow_html=True)
    
    cedula_input = st.text_input("Cédula de Identidad:", max_chars=10, type="password")
    
    if st.button("Ingresar al Sistema", type="primary", use_container_width=True):
        cedula_limpia = cedula_input.strip()
        if len(cedula_limpia) >= 10 or cedula_limpia == "1":
            try:
                # Consultamos datos, incluyendo la sección y sub_paso guardados en Supabase
                response = supabase.table("usuarios").select("nombres, seccion_actual, sub_paso").eq("cedula", cedula_limpia).execute()
                
                if response.data and len(response.data) > 0:
                    user_data = response.data[0]
                    st.session_state.cedula = cedula_limpia
                    st.session_state.nombre_usuario = user_data["nombres"]
                    
                    # Recuperar progreso guardado en la base de datos (siempre que existan)
                    st.session_state.seccion_actual = user_data.get("seccion_actual", 0) or 0
                    st.session_state.sub_paso = user_data.get("sub_paso", "teoria") or "teoria"
                    
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
        <h3 style="color: #0f172a; margin-top:0;">📊 PANEL DE CONTROL Y ESTADÍSTICAS - ILEPSA</h3>
        <p style="color: #64748b; font-size: 14px;"><b>Administrador en sesión:</b> {st.session_state.nombre_usuario}</p>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 12px 0;">
        <p style="font-size: 14px; color: #334155;">
            Monitoreo en tiempo real de accesos, tiempos de conexión y avance guardado de los colaboradores bajo la normativa MDT-2025-006.
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
                res_user = supabase.table("usuarios").select("nombres, seccion_actual").eq("cedula", cedula_reg).execute()
                if res_user.data:
                    nombre_reg = res_user.data[0]["nombres"]
                    sec_progreso = res_user.data[0].get("seccion_actual", 0)
                else:
                    nombre_reg = "Colaborador Externo"
                    sec_progreso = 0
                
                datos_tabla.append({
                    "Colaborador": nombre_reg,
                    "Cédula": cedula_reg,
                    "Sección Actual": f"{sec_progreso} / {len(SECCIONES)}",
                    "Fecha y Hora de Ingreso": fecha_reg
                })
            st.dataframe(datos_tabla, use_container_width=True)
        else:
            st.info("Aún no se registran ingresos de colaboradores.")
    except Exception:
        pass
        
    st.markdown("### 👥 Listado General de Colaboradores Registrados")
    try:
        query_usuarios = supabase.table("usuarios").select("cedula, nombres, seccion_actual").execute()
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
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 12px 0;">
        <p style="font-size: 14.5px; color: #334155; line-height: 1.6;">
            En cumplimiento con la normativa legal vigente y el <b>Acuerdo Ministerial MDT-2025-006</b>, este programa de formación integral es de <b>carácter obligatorio</b> para todo el personal de la Compañía ILEPSA S.A. (Certificación de 40 horas).
        </p>
        <p style="font-size: 14.5px; color: #334155; line-height: 1.6; margin-bottom: 5px;">
            <b>Progreso Automático:</b> Su avance se guarda de forma permanente en el sistema. Si cierra sesión o ingresa otro día, continuará exactamente desde donde se quedó.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Continuar mi Capacitación ➔", type="primary", use_container_width=True):
        # Si ya completó todas las secciones, salta directo al certificado
        if st.session_state.seccion_actual >= len(SECCIONES):
            st.session_state.paso = "certificado"
        else:
            st.session_state.paso = "evaluacion"
        st.rerun()

# =========================================================
# FASE 4: MÓDULO DE CAPACITACIÓN (Con guardado automático en Supabase)
# =========================================================
elif st.session_state.paso == "evaluacion":
    total_secciones = len(SECCIONES)
    sec_idx = st.session_state.seccion_actual

    if sec_idx < total_secciones:
        seccion = SECCIONES[sec_idx]
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
            if st.button("Guardar y Salir"):
                st.session_state.paso = "login"
                st.rerun()
                
        progreso = sec_idx / total_secciones
        st.progress(progreso, text=f"Progreso actual: Sección {sec_idx + 1} de {total_secciones}")
        
        # -------------------------------------------------
        # PANTALLA 1: TEORÍA
        # -------------------------------------------------
        if st.session_state.sub_paso == "teoria":
            st.markdown(f"""
            <div class="pagina-nueva-transicion card-principal" style="border-top: 5px solid {estilo_color['borde']};">
                <div class="badge-seccion-derecha" style="background-color: {estilo_color['fondo_etiqueta']}; color: {estilo_color['texto_etiqueta']};">
                    LECTURA {sec_idx + 1} / {total_secciones}
                </div>
                <span style="color: {estilo_color['borde']}; font-weight: bold; font-size: 13px; text-transform: uppercase;">
                    {seccion['eje']}
                </span>
                <h3 style="margin-top: 6px; margin-bottom: 12px; color: #0f172a; font-size: 20px;">{seccion['titulo']}</h3>
                <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 12px 0;">
                <div class="contenido-texto">
                    {seccion['contenido']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Continuar al Cuestionario de esta Sección ➔", type="primary", key=f"btn_ir_cuestionario_{sec_idx}", use_container_width=True):
                st.session_state.sub_paso = "cuestionario"
                
                # GUARDADO AUTOMÁTICO EN SUPABASE DEL SUB-PASO
                try:
                    supabase.table("usuarios").update({
                        "seccion_actual": st.session_state.seccion_actual,
                        "sub_paso": "cuestionario"
                    }).eq("cedula", st.session_state.cedula).execute()
                except Exception:
                    pass

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
                st.rerun()

        # -------------------------------------------------
        # PANTALLA 2: CUESTIONARIO
        # -------------------------------------------------
        elif st.session_state.sub_paso == "cuestionario":
            st.markdown(f"""
            <div class="pagina-nueva-transicion card-principal" style="border-top: 5px solid {estilo_color['borde']};">
                <div class="badge-seccion-derecha" style="background-color: {estilo_color['fondo_etiqueta']}; color: {estilo_color['texto_etiqueta']};">
                    EVALUACIÓN {sec_idx + 1} / {total_secciones}
                </div>
                <span style="color: {estilo_color['borde']}; font-weight: bold; font-size: 13px; text-transform: uppercase;">
                    Cuestionario de Validación
                </span>
                <h3 style="margin-top: 6px; margin-bottom: 12px; color: #0f172a; font-size: 19px;">{seccion['titulo']}</h3>
                <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 12px 0;">
                <p style="font-size: 14px; color: #475569; margin-bottom: 15px;">
                    Responda la siguiente pregunta correspondiente al contenido que acaba de estudiar:
                </p>
                <div class="pregunta-box" style="border-left: 4px solid {estilo_color['borde']};">
                    <p style="font-size: 15px; font-weight: 600; color: #1e293b; margin: 0;">{seccion['pregunta']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            respuesta = st.radio(
                "Seleccione su respuesta:", 
                seccion['opciones'], 
                key=f"radio_cuestionario_{sec_idx}"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("⬅ Volver a leer la Teoría", use_container_width=True):
                    st.session_state.sub_paso = "teoria"
                    try:
                        supabase.table("usuarios").update({
                            "sub_paso": "teoria"
                        }).eq("cedula", st.session_state.cedula).execute()
                    except Exception:
                        pass
                    st.rerun()
            with col_btn2:
                btn_siguiente = st.button("Enviar Respuesta y Siguiente ➔", type="primary", key=f"btn_enviar_{sec_idx}", use_container_width=True)
            
            if btn_siguiente:
                if respuesta == seccion['correcta']:
                    st.session_state.respuestas_correctas += 1
                    st.session_state.seccion_actual += 1
                    st.session_state.sub_paso = "teoria"
                    
                    # GUARDADO AUTOMÁTICO EN SUPABASE DEL AVANCE DE SECCIÓN
                    try:
                        supabase.table("usuarios").update({
                            "seccion_actual": st.session_state.seccion_actual,
                            "sub_paso": "teoria"
                        }).eq("cedula", st.session_state.cedula).execute()
                    except Exception:
                        pass
                    
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
                    
                    with st.spinner(f"¡Respuesta correcta! Guardando avance y cargando siguiente sección..."):
                        time.sleep(0.3)
                    st.rerun()
                else:
                    st.error("Respuesta incorrecta. Debe revisar nuevamente la teoría de esta sección para poder avanzar.")
    else:
        st.session_state.paso = "certificado"
        st.rerun()

# =========================================================
# FASE 5: CERTIFICADO OFICIAL (40 HORAS - ACUERDO MDT-2025-006)
# =========================================================
elif st.session_state.paso == "certificado":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <span style="font-size: 24px;">✨ 🏆 ✨</span>
        <h3 style="color: #059669; margin: 5px 0; font-size: 20px;">¡CAPACITACIÓN APROBADA CON ÉXITO!</h3>
        <p style="color: #64748b; font-size: 13.5px;">Su aprobación ha sido procesada y registrada en el sistema de ILEPSA.</p>
    </div>
    """, unsafe_allow_html=True)
    
    html_certificado = f"""
    <div class="certificado-container">
        <h2 style="color: #0f172a; letter-spacing: 2px; margin-bottom: 5px; font-family: serif; font-size: 24px;">CERTIFICADO DE APROBACIÓN</h2>
        <p style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Acuerdo Ministerial MDT-2025-006</p>
        
        <p style="margin: 25px 0 10px 0; font-size: 15px; color: #334155;">Se otorga el presente reconocimiento a:</p>
        <h1 style="color: #0284c7; font-size: 28px; border-bottom: 2px solid #cbd5e1; display: inline-block; padding-bottom: 5px; margin: 10px 0; font-family: serif;">{st.session_state.nombre_usuario}</h1>
        <p style="font-size: 14px; color: #334155;">Con Cédula de Identidad N° <b>{st.session_state.cedula}</b></p>
        
        <p style="font-size: 14px; color: #334155; line-height: 1.6; max-width: 600px; margin: 20px auto;">
            Por haber completado y aprobado satisfactoriamente el programa de formación integral en prevención de riesgos laborales, equidad y no discriminación, con una intensidad de <b>40 horas académicas</b>, cumpliendo a cabalidad con las normativas vigentes de la compañía ILEPSA S.A.
        </p>
        
        <div style="margin-top: 40px; display: flex; justify-content: space-around;">
            <div style="text-align: center;">
                <div style="border-top: 1px solid #0f172a; width: 180px; margin: 0 auto 5px auto;"></div>
                <b style="color: #0f172a; font-size: 13px;">Gerencia General</b><br>
                <span style="color: #64748b; font-size: 11px;">ILEPSA S.A.</span>
            </div>
            <div style="text-align: center;">
                <div style="border-top: 1px solid #0f172a; width: 180px; margin: 0 auto 5px auto;"></div>
                <b style="color: #0f172a; font-size: 13px;">Dirección de Talento Humano</b><br>
                <span style="color: #64748b; font-size: 11px;">Validado y Registrado</span>
            </div>
        </div>
    </div>
    """
    
    st.markdown(html_certificado, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.download_button(
        label="📥 Descargar Certificado Oficial en HTML / Imprimir PDF",
        data=html_certificado,
        file_name=f"Certificado_ILEPSA_{st.session_state.cedula}.html",
        mime="text/html",
        use_container_width=True
    )
    
    if st.button("Finalizar y Salir del Sistema"):
        st.session_state.paso = "login"
        st.session_state.cedula = ""
        st.session_state.nombre_usuario = ""
        st.session_state.es_admin = False
        st.session_state.seccion_actual = 0
        st.session_state.sub_paso = "teoria"
        st.rerun()
