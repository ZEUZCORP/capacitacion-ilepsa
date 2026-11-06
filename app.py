import streamlit as st
import streamlit.components.v1 as components
import time
import random
from datetime import datetime
from supabase import create_client, Client
from contenidos import SECCIONES

st.set_page_config(
    page_title="Plataforma ILEPSA",
    page_icon="🏢",
    layout="centered"
)

@st.cache_resource
def init_supabase() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_supabase()

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

COLORES_SECCION = [
    {"borde": "#0284c7", "fondo_etiqueta": "#e0f2fe", "texto_etiqueta": "#0369a1"},
    {"borde": "#7c3aed", "fondo_etiqueta": "#ede9fe", "texto_etiqueta": "#6d28d9"},
    {"borde": "#059669", "fondo_etiqueta": "#d1fae5", "texto_etiqueta": "#047857"},
    {"borde": "#d97706", "fondo_etiqueta": "#fef3c7", "texto_etiqueta": "#b45309"},
    {"borde": "#dc2626", "fondo_etiqueta": "#fee2e2", "texto_etiqueta": "#b91c1c"}
]

# Revisar si ya acertó en la sección actual para bloquear dinámicamente las opciones con CSS
sec_actual_idx = st.session_state.get("seccion_actual", 0)
bloqueo_css = ""
if st.session_state.get(f"estado_msg_{sec_actual_idx}", "") == "exito":
    bloqueo_css = """
    div.stRadio div[role="radiogroup"] {
        opacity: 0.45 !important;
        pointer-events: none !important;
    }
    """

st.markdown("""
    <style>
    @keyframes fadeInPage {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .pagina-nueva-transicion {
        animation: fadeInPage 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .card-principal {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
        position: relative;
    }
    .badge-seccion-derecha {
        position: absolute;
        top: 20px;
        right: 25px;
        padding: 5px 14px;
        border-radius: 15px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .header-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 12px 18px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 15px;
    }
    .contenido-texto {
        font-size: 18.5px;
        line-height: 1.8;
        color: #334155;
        text-align: justify;
    }
    .pregunta-box {
        background-color: #f8fafc;
        border-left: 4px solid #0f172a;
        padding: 22px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    .stRadio > label {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        margin-bottom: 12px !important;
    }
    div.stRadio div[role="radiogroup"] label p {
        font-size: 17.5px !important;
        color: #1e293b !important;
        line-height: 1.5 !important;
    }
    div.stRadio div[role="radiogroup"] label {
        font-size: 17.5px !important;
        padding-top: 6px !important;
        padding-bottom: 6px !important;
    }
    """ + bloqueo_css + """
    </style>
""", unsafe_allow_html=True)

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
    <div class="pagina-nueva-transicion card-principal" style="text-align: center; border-top: 5px solid #0284c7; max-width: 550px; margin: 40px auto;">
        <h3 style="color: #0f172a; margin-top:0;">ACCESO COLABORADORES ILEPSA</h3>
        <p style="color: #64748b; font-size: 15px; margin-bottom: 0;">Ingrese su número de cédula para acceder a la capacitación virtual programada por la compañía.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        cedula_input = st.text_input("Cédula de Identidad:", max_chars=10, type="password")
        if st.button("Ingresar al Sistema", type="primary", use_container_width=True):
            cedula_limpia = cedula_input.strip()
            if len(cedula_limpia) >= 10 or cedula_limpia == "1":
                try:
                    response = supabase.table("usuarios").select("nombres, seccion_actual, sub_paso").eq("cedula", cedula_limpia).execute()
                    
                    if response.data and len(response.data) > 0:
                        user_data = response.data[0]
                        st.session_state.cedula = cedula_limpia
                        st.session_state.nombre_usuario = user_data["nombres"]
                        st.session_state.seccion_actual = user_data.get("seccion_actual", 0) or 0
                        st.session_state.sub_paso = user_data.get("sub_paso", "teoria") or "teoria"
                        
                        try:
                            supabase.table("registro_tiempos").insert({
                                "cedula": cedula_limpia,
                                "fecha_ingreso": datetime.now().isoformat()
                            }).execute()
                        except Exception:
                            pass

                        if "Administrador" in st.session_state.nombre_usuario or cedula_limpia in ["9999999999", "1"]:
                            st.session_state.es_admin = True
                            st.session_state.paso = "admin_dashboard"
                        else:
                            st.session_state.es_admin = False
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
        <p style="color: #64748b; font-size: 15px;"><b>Administrador en sesión:</b> {st.session_state.nombre_usuario}</p>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 12px 0;">
        <p style="font-size: 15px; color: #334155;">
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
                    nombre_reg = "Colaborador / Admin"
                    sec_progreso = "N/A"
                
                datos_tabla.append({
                    "Colaborador": nombre_reg,
                    "Cédula": cedula_reg,
                    "Sección Actual": f"{sec_progreso} / {len(SECCIONES)}" if isinstance(sec_progreso, int) else sec_progreso,
                    "Fecha y Hora de Ingreso": fecha_reg
                })
            st.dataframe(datos_tabla, use_container_width=True)
        else:
            st.info("Aún no se registran ingresos en la tabla registro_tiempos.")
    except Exception as e:
        st.error(f"Error al consultar los registros: {e}")
        
    if st.button("Cerrar Sesión de Administrador", type="primary", use_container_width=True):
        st.session_state.paso = "login"
        st.session_state.cedula = ""
        st.session_state.nombre_usuario = ""
        st.session_state.es_admin = False
        st.rerun()

# =========================================================
# FASE 3: INSTRUCCIONES / BIENVENIDA
# =========================================================
elif st.session_state.paso == "instrucciones":
    st.markdown(f"""
    <div class="pagina-nueva-transicion card-principal" style="border-top: 5px solid #0284c7;">
        <h3 style="color: #0f172a; margin-top:0;">¡Bienvenido(a), {st.session_state.nombre_usuario}!</h3>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 12px 0;">
        <p style="font-size: 16px; color: #334155; line-height: 1.6;">
            En cumplimiento con el <b>Artículo 3 del Acuerdo Ministerial MDT-2025-006</b>, los empleadores del sector privado y público deben llevar a cabo procesos de capacitación con una duración mínima de <b>cuarenta (40) horas anuales</b> dirigidos a todos los trabajadores.
        </p>
        <p style="font-size: 16px; color: #334155; line-height: 1.6;">
            Este programa aborda los temas obligatorios normativos: <b>a) Derechos laborales de mujeres y hombres; b) Igualdad de género; c) Erradicación de violencia y no discriminación en el centro de trabajo; y d) Establecimiento de trabajo de igual valor.</b>
        </p>
        <p style="font-size: 15px; color: #0284c7; background-color: #e0f2fe; padding: 12px; border-radius: 6px; margin-top: 15px; font-weight: 500;">
            💡 <b>Nota:</b> Su progreso se guardará automáticamente para cuando inicie sesión nuevamente.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Continuar mi Capacitación ➔", type="primary", use_container_width=True):
        st.session_state.paso = "evaluacion"
        st.rerun()

# =========================================================
# FASE 4: MÓDULO DE CAPACITACIÓN
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
        
        if st.session_state.sub_paso == "teoria":
            st.markdown(f"""
            <div class="pagina-nueva-transicion card-principal" style="border-top: 5px solid {estilo_color['borde']};">
                <div class="badge-seccion-derecha" style="background-color: {estilo_color['fondo_etiqueta']}; color: {estilo_color['texto_etiqueta']};">
                    LECTURA {sec_idx + 1} / {total_secciones}
                </div>
                <span style="color: {estilo_color['borde']}; font-weight: bold; font-size: 14.5px; text-transform: uppercase;">
                    {seccion['eje']}
                </span>
                <h3 style="margin-top: 8px; margin-bottom: 12px; color: #0f172a; font-size: 23px;">{seccion['titulo']}</h3>
                <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 14px 0;">
                <div class="contenido-texto">
                    {seccion['contenido']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Continuar al Cuestionario de esta Sección ➔", type="primary", key=f"btn_ir_cuestionario_{sec_idx}", use_container_width=True):
                st.session_state.sub_paso = "cuestionario"
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

        elif st.session_state.sub_paso == "cuestionario":
            st.markdown(f"""
            <div class="pagina-nueva-transicion card-principal" style="border-top: 5px solid {estilo_color['borde']};">
                <div class="badge-seccion-derecha" style="background-color: {estilo_color['fondo_etiqueta']}; color: {estilo_color['texto_etiqueta']};">
                    EVALUACIÓN {sec_idx + 1} / {total_secciones}
                </div>
                <span style="color: {estilo_color['borde']}; font-weight: bold; font-size: 14.5px; text-transform: uppercase;">
                    Cuestionario de Validación
                </span>
                <h3 style="margin-top: 8px; margin-bottom: 12px; color: #0f172a; font-size: 23px;">{seccion['titulo']}</h3>
                <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 14px 0;">
                <p style="font-size: 16px; color: #475569; margin-bottom: 15px;">
                    Responda la siguiente pregunta correspondiente al contenido que acaba de estudiar:
                </p>
                <div class="pregunta-box" style="border-left: 4px solid {estilo_color['borde']};">
                    <p style="font-size: 18px; font-weight: 600; color: #1e293b; margin: 0;">{seccion['pregunta']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            key_estado_msg = f"estado_msg_{sec_idx}"
            if key_estado_msg not in st.session_state:
                st.session_state[key_estado_msg] = ""

            col_lbl1, col_lbl2 = st.columns([2, 3])
            with col_lbl1:
                st.markdown("<p style='font-size: 20px; font-weight: 700; color: #0f172a; margin-top: 10px;'>Seleccione su respuesta:</p>", unsafe_allow_html=True)
            with col_lbl2:
                msg = st.session_state[key_estado_msg]
                if msg == "error":
                    st.markdown("<p style='color: #dc2626; font-weight: 700; font-size: 13.5px; background-color: #fee2e2; padding: 8px 12px; border-radius: 6px; border: 1px solid #fca5a5; margin: 0;'>❌ Respuesta incorrecta. Debe revisar nuevamente la teoría.</p>", unsafe_allow_html=True)
                elif msg == "exito":
                    st.markdown("<p style='color: #059669; font-weight: 700; font-size: 13.5px; background-color: #d1fae5; padding: 8px 12px; border-radius: 6px; border: 1px solid #a7f3d0; margin: 0;'>✔ ¡Respuesta correcta!</p>", unsafe_allow_html=True)

            key_opciones_mix = f"opciones_mix_{sec_idx}"
            if key_opciones_mix not in st.session_state:
                lista_opciones = list(seccion['opciones'])
                random.shuffle(lista_opciones)
                st.session_state[key_opciones_mix] = lista_opciones

            respuesta = st.radio(
                "", 
                st.session_state[key_opciones_mix], 
                key=f"radio_cuestionario_{sec_idx}"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("⬅ Volver a leer la Teoría", use_container_width=True):
                    st.session_state[key_estado_msg] = ""
                    st.session_state.sub_paso = "teoria"
                    try:
                        supabase.table("usuarios").update({
                            "sub_paso": "teoria"
                        }).eq("cedula", st.session_state.cedula).execute()
                    except Exception:
                        pass
                    st.rerun()
            with col_btn2:
                if st.session_state[key_estado_msg] == "exito":
                    if st.button(f"Continuar Sección {sec_idx + 1} de Capacitación ➔", type="primary", key=f"btn_continuar_sec_{sec_idx}", use_container_width=True):
                        st.session_state[key_estado_msg] = ""
                        st.session_state.respuestas_correctas += 1
                        st.session_state.seccion_actual += 1
                        st.session_state.sub_paso = "teoria"
                        
                        if key_opciones_mix in st.session_state:
                            del st.session_state[key_opciones_mix]
                        
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
                        st.rerun()
                else:
                    btn_siguiente = st.button("Enviar Respuesta y Siguiente ➔", type="primary", key=f"btn_enviar_{sec_idx}", use_container_width=True)
                    if btn_siguiente:
                        if respuesta == seccion['correcta']:
                            st.session_state[key_estado_msg] = "exito"
                            st.rerun()
                        else:
                            st.session_state[key_estado_msg] = "error"
                            st.rerun()
    else:
        st.session_state.paso = "certificado"
        st.rerun()

# =========================================================
# FASE 5: CERTIFICADO OFICIAL CORPORATIVO
# =========================================================
elif st.session_state.paso == "certificado":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="font-size: 28px;">🎓 ✨</span>
        <h3 style="color: #059669; margin: 5px 0; font-size: 22px;">¡CAPACITACIÓN APROBADA CON ÉXITO!</h3>
        <p style="color: #64748b; font-size: 15px;">Su certificado oficial de cumplimiento ha sido emitido satisfactoriamente.</p>
    </div>
    """, unsafe_allow_html=True)
    
    html_certificado = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Lora:ital,wght@0,400;0,600;1,400&family=Open+Sans:wght@400;600&display=swap');
      
      body {{
          font-family: 'Open Sans', sans-serif;
          background-color: #e2e8f0;
          margin: 0;
          padding: 20px;
          display: flex;
          justify-content: center;
          align-items: center;
      }}
      .diploma-marco {{
          background: #fffdf9;
          border: 12px double #1e3a8a;
          width: 900px;
          padding: 50px 70px;
          text-align: center;
          box-sizing: border-box;
          box-shadow: 0 15px 35px rgba(0,0,0,0.15);
          position: relative;
          margin: 0 auto;
      }}
      .institucion-sup {{
          font-family: 'Cinzel', serif;
          font-size: 16px;
          letter-spacing: 5px;
          color: #475569;
          text-transform: uppercase;
          font-weight: 700;
          margin-bottom: 10px;
      }}
      h1 {{
          font-family: 'Cinzel', serif;
          color: #1e3a8a;
          font-size: 36px;
          margin: 0 0 8px 0;
          letter-spacing: 2px;
      }}
      .normativa {{
          font-family: 'Open Sans', sans-serif;
          color: #0284c7;
          font-size: 13px;
          text-transform: uppercase;
          letter-spacing: 2px;
          margin-bottom: 35px;
          font-weight: 600;
      }}
      .otorga-texto {{
          font-family: 'Lora', serif;
          font-size: 17px;
          color: #334155;
          font-style: italic;
          margin-bottom: 5px;
      }}
      .nombre-colaborador {{
          font-family: 'Lora', serif;
          color: #0f172a;
          font-size: 34px;
          font-weight: bold;
          border-bottom: 2px solid #cbd5e1;
          display: inline-block;
          padding-bottom: 6px;
          margin: 10px 0 15px 0;
      }}
      .cedula-texto {{
          font-family: 'Open Sans', sans-serif;
          font-size: 15px;
          color: #475569;
          margin-bottom: 30px;
      }}
      .cuerpo-texto {{
          font-family: 'Lora', serif;
          font-size: 15.5px;
          color: #334155;
          line-height: 1.8;
          max-width: 740px;
          margin: 0 auto 50px auto;
          text-align: justify;
      }}
      .firmas-area {{
          display: flex;
          justify-content: center;
          margin-top: 20px;
      }}
      .firma-caja {{
          text-align: center;
          width: 300px;
      }}
      .linea-firma {{
          border-top: 1px solid #1e3a8a;
          margin-bottom: 8px;
      }}
      .cargo-titulo {{
          font-family: 'Open Sans', sans-serif;
          font-weight: 700;
          color: #0f172a;
          font-size: 15px;
      }}
      .empresa-sub {{
          font-family: 'Open Sans', sans-serif;
          font-size: 13px;
          color: #64748b;
      }}
      
      @media print {{
          body {{ background: transparent; padding: 0; }}
          .diploma-marco {{ box-shadow: none; border: 10px double #1e3a8a; width: 100%; }}
      }}
    </style>
    </head>
    <body>
      <div class="diploma-marco">
        <div class="institucion-sup">COMPAÑÍA ILEPSA S.A.</div>
        <h1>CERTIFICADO DE APROBACIÓN</h1>
        <div class="normativa">Acuerdo Ministerial MDT-2025-006 • Capacitación de 40 Horas</div>
        
        <div class="otorga-texto">Se otorga el presente reconocimiento oficial a:</div>
        <div class="nombre-colaborador">{st.session_state.nombre_usuario}</div>
        <div class="cedula-texto">Cédula de Identidad N° <b>{st.session_state.cedula}</b></div>
        
        <div class="cuerpo-texto">
          Por haber cumplido y aprobado satisfactoriamente el programa de formación corporativa en cumplimiento del <b>Artículo 3 del Acuerdo Ministerial MDT-2025-006</b>, abordando los ejes de derechos laborales de mujeres y hombres, igualdad de género, erradicación de violencia y no discriminación en el centro de trabajo, y trabajo de igual valor, con una intensidad de <b>40 horas académicas</b>.
        </div>
        
        <div class="firmas-area">
          <div class="firma-caja">
            <div class="linea-firma"></div>
            <div class="cargo-titulo">Gerencia General</div>
            <div class="empresa-sub">ILEPSA S.A.</div>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    
    components.html(html_certificado, height=620, scrolling=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🖨️ Imprimir y Guardar Certificado in PDF", type="primary", use_container_width=True):
        components.html("<script>window.parent.print();</script>", height=0)
    
    if st.button("Finalizar y Salir del Sistema"):
        st.session_state.paso = "login"
        st.session_state.cedula = ""
        st.session_state.nombre_usuario = ""
        st.session_state.es_admin = False
        st.session_state.seccion_actual = 0
        st.session_state.sub_paso = "teoria"
        st.rerun()
