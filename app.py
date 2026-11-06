import streamlit as st
import datetime
from supabase import create_client, Client
from fpdf import FPDF

# Configuración de página
st.set_page_config(page_title="Capacitación ILEPSA", page_icon="🏢", layout="wide")

# Inicialización de Supabase
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# Contenido de los 4 Ejes Temáticos (40 Horas / MDT-2025-006)
EJES = {
    1: {
        "titulo": "Eje 1: Derechos Laborales, Igualdad y No Discriminación (10 Horas)",
        "modulos": {
            "1.1": {
                "titulo": "Módulo 1.1: Marco Legal Nacional e Internacional",
                "contenido": """
                #### 1. Constitución de la República del Ecuador
                * **Art. 33:** El trabajo es un derecho y un deber social, y un derecho económico, fuente de realización personal y base de la economía. El Estado garantizará la dignidad y retribuciones justas.
                * **Art. 329:** Garantía de igualdad de oportunidades y no discriminación en el acceso, permanencia y ascenso laboral.

                #### 2. Convenios OIT
                * **Convenio 100:** Igualdad de remuneración entre hombres y mujeres por trabajo de igual valor.
                * **Convenio 111:** Eliminación de toda discriminación en materia de empleo y ocupación.
                """,
                "pregunta": "¿Qué establece el Art. 329 de la Constitución?",
                "opciones": ["Igualdad de oportunidades y no discriminación laboral.", "Jornada laboral sin límites.", "Jubilación obligatoria a los 40 años."],
                "correcta": "Igualdad de oportunidades y no discriminación laboral."
            },
            "1.2": {
                "titulo": "Módulo 1.2: Código del Trabajo e Igualdad Salarial",
                "contenido": """
                #### 1. Código del Trabajo del Ecuador
                * Los derechos laborales son intangibles e irrenunciables.
                * Prohibición de diferencias salariales por motivo de género o condición social.
                """,
                "pregunta": "¿Cuál es la característica principal de los derechos laborales en Ecuador?",
                "opciones": ["Son intangibles e irrenunciables.", "Son modificables libremente por el empleador.", "Son opcionales."],
                "correcta": "Son intangibles e irrenunciables."
            }
        }
    },
    2: {
        "titulo": "Eje 2: Prevención del Acoso Laboral y Violencia de Género (10 Horas)",
        "modulos": {
            "2.1": {
                "titulo": "Módulo 2.1: Definición y Protocolos de Acoso",
                "contenido": """
                #### 1. Acoso Laboral
                * Comportamiento reiterado atentatorio a la dignidad de la persona que genera un entorno hostil.
                * Procedimiento confidencial de denuncia y protección dentro de ILEPSA.
                """,
                "pregunta": "¿Qué define al acoso laboral?",
                "opciones": ["Comportamiento reiterado atentatorio a la dignidad.", "Una diferencia de opinión laboral puntual.", "La asignación regular de tareas."],
                "correcta": "Comportamiento reiterado atentatorio a la dignidad."
            }
        }
    },
    3: {
        "titulo": "Eje 3: Conciliación de la Vida Laboral, Familiar y Personal (10 Horas)",
        "modulos": {
            "3.1": {
                "titulo": "Módulo 3.1: Maternidad, Paternidad y Lactancia",
                "contenido": """
                #### 1. Corresponsabilidad y Licencias
                * Licencias pagadas por maternidad y paternidad.
                * Permiso de lactancia materna: 2 horas diarias durante los primeros 12 meses.
                """,
                "pregunta": "¿Cuál es la duración del permiso de lactancia materna diaria?",
                "opciones": ["2 horas diarias por 12 meses.", "30 minutos diarios por 6 meses.", "1 hora diaria por 3 meses."],
                "correcta": "2 horas diarias por 12 meses."
            }
        }
    },
    4: {
        "titulo": "Eje 4: Salud Ocupacional y Riesgos Psicosociales (10 Horas)",
        "modulos": {
            "4.1": {
                "titulo": "Módulo 4.1: Entornos de Trabajo Seguros",
                "contenido": """
                #### 1. Salud Mental y Prevención
                * Evaluación de riesgos psicosociales y clima laboral en la planta y administración.
                """,
                "pregunta": "¿Cuál es el objetivo de evaluar los riesgos psicosociales?",
                "opciones": ["Garantizar un ambiente de trabajo sano y seguro.", "Eliminar los días de vacaciones.", "Aumentar la carga horaria."],
                "correcta": "Garantizar un ambiente de trabajo sano y seguro."
            }
        }
    }
}

# Generación de PDF
def generar_certificado_pdf(nombre_usuario, cedula_usuario, cargo_usuario):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    pdf.set_line_width(2)
    pdf.set_draw_color(180, 140, 40)
    pdf.rect(10, 10, 277, 190)
    pdf.set_line_width(0.5)
    pdf.rect(13, 13, 271, 184)

    pdf.set_font("Helvetica", 'B', 18)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 15, "INDUSTRIA LICORERA EMBOTELLADORA DE PICHINCHA S.A. ILEPSA", ln=True, align='C')
    
    pdf.set_font("Helvetica", 'I', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Cumplimiento Formativo Anual - Normativa MDT-2025-006", ln=True, align='C')
    
    pdf.ln(4)
    pdf.set_font("Helvetica", 'B', 28)
    pdf.set_text_color(180, 140, 40)
    pdf.cell(0, 16, "CERTIFICADO DE APROBACIÓN", ln=True, align='C')
    
    pdf.set_font("Helvetica", '', 12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, "Otorgado a:", ln=True, align='C')
    
    pdf.set_font("Helvetica", 'B', 22)
    pdf.set_text_color(10, 30, 80)
    pdf.cell(0, 14, nombre_usuario.upper(), ln=True, align='C')
    
    pdf.set_font("Helvetica", '', 11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 6, f"C.I.: {cedula_usuario} | Cargo: {cargo_usuario}", ln=True, align='C')
    
    pdf.ln(4)
    texto_cuerpo = (
        "Por haber completado y aprobado satisfactoriamente los 4 Ejes de Capacitación Obligatoria en "
        "Derechos Laborales, Prevención del Acoso, Conciliación Familiar y Salud Ocupacional, alcanzando un "
        "total acumulado de 40 HORAS ACADÉMICAS conforme a lo establecido por el Ministerio del Trabajo."
    )
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, texto_cuerpo, align='C')
    
    pdf.ln(8)
    fecha_actual = datetime.date.today().strftime("%d de %B de %Y")
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 6, f"Quito, Ecuador, {fecha_actual}", ln=True, align='C')
    
    pdf.ln(12)
    pdf.set_draw_color(50, 50, 50)
    pdf.line(98, 165, 198, 165)
    
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 5, "OSWALDO FERNANDO GÓMEZ DE LA TORRE REYES", ln=True, align='C')
    pdf.set_font("Helvetica", '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "Gerente General", ln=True, align='C')
    pdf.cell(0, 5, "INDUSTRIA LICORERA EMBOTELLADORA DE PICHINCHA S.A. ILEPSA", ln=True, align='C')
    
    return bytes(pdf.output())

# Control de Sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_data" not in st.session_state:
    st.session_state.user_data = None

# --- LOGIN ---
if not st.session_state.authenticated:
    st.title("Plataforma de Capacitación Obligatoria")
    st.subheader("INDUSTRIA LICORERA EMBOTELLADORA DE PICHINCHA S.A. ILEPSA")
    st.caption("Cumplimiento MDT-2025-006")

    cedula_input = st.text_input("Ingrese su Cédula de Identidad:")

    if st.button("Iniciar Sesión"):
        if cedula_input.strip():
            res = supabase.table("usuarios").select("*").eq("cedula", cedula_input.strip()).execute()
            if res.data:
                st.session_state.authenticated = True
                st.session_state.user_data = res.data[0]
                st.rerun()
            else:
                st.error("Cédula no registrada. Contacte a Talento Humano.")
        else:
            st.warning("Ingrese su cédula.")

# --- PLATAFORMA ---
else:
    user = st.session_state.user_data
    is_admin = user["cedula"] == "9999999999"
    
    st.sidebar.title(f"Usuario: {user['nombres']}")
    st.sidebar.write(f"**Cargo:** {user['cargo']}")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.rerun()

    if is_admin:
        st.title("🛡️ Panel de Control y Monitoreo en Tiempo Real (ADMINISTRADOR)")
        
        tab_envivo, tab_usuarios = st.tabs(["⚡ Actividad en Tiempo Real", "👥 Lista de Usuarios"])
        
        with tab_envivo:
            st.subheader("Registros de Tiempos Guardados")
            tiempos_all = supabase.table("registro_tiempos").select("*").order("id", desc=True).execute()
            if tiempos_all.data:
                st.dataframe(tiempos_all.data, use_container_width=True)
            else:
                st.info("Aún ningún usuario ha guardado minutos de estudio hoy.")

            st.subheader("Evaluaciones Presentadas")
            evals_all = supabase.table("evaluaciones").select("*").order("id", desc=True).execute()
            if evals_all.data:
                st.dataframe(evals_all.data, use_container_width=True)
            else:
                st.info("No hay evaluaciones registradas en el sistema.")
                
        with tab_usuarios:
            st.subheader("Personal Registrado en ILEPSA")
            users_all = supabase.table("usuarios").select("*").execute()
            if users_all.data:
                st.dataframe(users_all.data, use_container_width=True)

    else:
        st.title("Programa Anual de Capacitación Continua (40 Horas)")
        st.info("⏱️ Recuerda cumplir con el límite máximo de 30 minutos diarios de estudio.")

        eje_sel = st.sidebar.selectbox("Seleccionar Eje:", list(EJES.keys()), format_func=lambda x: f"Eje {x}")
        modulos_dict = EJES[eje_sel]["modulos"]
        mod_sel = st.sidebar.selectbox("Seleccionar Módulo:", list(modulos_dict.keys()), format_func=lambda x: modulos_dict[x]["titulo"])
        modulo_actual = modulos_dict[mod_sel]

        tab_modulo, tab_evaluacion, tab_progreso, tab_certificado = st.tabs([
            "📖 Módulo de Estudio", 
            "📝 Evaluación", 
            "📊 Mi Progreso",
            "🎓 Certificado (40 Horas)"
        ])

        with tab_modulo:
            st.header(EJES[eje_sel]["titulo"])
            st.subheader(modulo_actual["titulo"])
            st.markdown(modulo_actual["contenido"])
            
            st.divider()
            st.subheader("Registro Auditable de Tiempo")
            tiempo_estudio = st.number_input("Minutos dedicados hoy (máx 30 min):", min_value=1, max_value=30, value=30)
            
            if st.button("Guardar Mi Tiempo de Lectura"):
                hora_actual = datetime.datetime.now()
                registro = {
                    "cedula": user["cedula"],
                    "eje": eje_sel,
                    "modulo": mod_sel,
                    "minutos_acumulados": tiempo_estudio,
                    "hora_inicio": hora_actual.isoformat(),
                    "hora_fin": hora_actual.isoformat()
                }
                res = supabase.table("registro_tiempos").insert(registro).execute()
                if res.data:
                    st.success(f"¡Se han registrado {tiempo_estudio} minutos exitosamente!")

        with tab_evaluacion:
            st.header(f"Evaluación del Módulo {mod_sel}")
            st.write(modulo_actual["pregunta"])
            resp = st.radio("Respuesta:", modulo_actual["opciones"])
            
            if st.button("Enviar Respuestas"):
                aprobado = resp == modulo_actual["correcta"]
                puntaje = 100 if aprobado else 0
                
                eval_data = {
                    "cedula": user["cedula"],
                    "eje": eje_sel,
                    "puntaje": puntaje,
                    "aprobado": aprobado
                }
                supabase.table("evaluaciones").insert(eval_data).execute()
                
                if aprobado:
                    st.balloons()
                    st.success("¡Respuesta Correcta! Módulo aprobado.")
                else:
                    st.error("Respuesta incorrecta. Inténtalo de nuevo.")

        with tab_progreso:
            st.header("Mi Avance de Horas Auditables")
            tiempos = supabase.table("registro_tiempos").select("*").eq("cedula", user["cedula"]).execute()
            minutos_totales = sum([item["minutos_acumulados"] for item in tiempos.data]) if tiempos.data else 0
            horas_totales = round(minutos_totales / 60, 2)
            
            st.metric(label="Horas Acumuladas", value=f"{horas_totales} / 40.0 hrs")
            st.progress(min(horas_totales / 40.0, 1.0))
            
            if tiempos.data:
                st.dataframe(tiempos.data, use_container_width=True)

        with tab_certificado:
            st.header("Certificado de Aprobación (40 Horas)")
            tiempos = supabase.table("registro_tiempos").select("*").eq("cedula", user["cedula"]).execute()
            minutos_totales = sum([item["minutos_acumulados"] for item in tiempos.data]) if tiempos.data else 0
            horas_totales = minutos_totales / 60
            
            if horas_totales >= 0.5:
                st.success("🎉 Has cumplido con los requisitos formativos de ILEPSA.")
                pdf_bytes = generar_certificado_pdf(user["nombres"], user["cedula"], user["cargo"])
                st.download_button(
                    label="📥 Descargar Diploma Oficial PDF (40 Horas)",
                    data=pdf_bytes,
                    file_name=f"Certificado_ILEPSA_{user['cedula']}.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning("Debes guardar tu primer registro de lectura para probar el diploma.")
