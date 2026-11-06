import streamlit as st
import time
from datetime import date
from supabase import create_client

# Configuración de página
st.set_page_config(
    page_title="Capacitación MDT - ILEPSA",
    page_icon="🏢",
    layout="wide"
)

# Conexión a base de datos en Supabase
@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# Encabezado corporativo
try:
    st.image("logo_ilepsa.png", width=200)
except:
    pass

st.title("Plataforma de Capacitación Obligatoria MDT-2025-006")
st.subheader("INDUSTRIA LICORERA EMBOTELLADORA DE PICHINCHA S.A. ILEPSA")
st.markdown("---")

# Manejo de estado de sesión
if "cedula" not in st.session_state:
    st.session_state.cedula = None
if "tiempo_inicio" not in st.session_state:
    st.session_state.tiempo_inicio = None

# Pantalla de Login
if st.session_state.cedula is None:
    st.markdown("### Inicio de Sesión de Trabajadores")
    with st.form("form_login"):
        cedula_input = st.text_input("Ingrese su Cédula / Documento de Identidad:")
        btn_ingresar = st.form_submit_button("Ingresar a la Plataforma")
        
        if btn_ingresar:
            if cedula_input.strip() == "":
                st.error("Por favor ingrese una cédula válida.")
            else:
                # Buscar trabajador en la base de datos
                res = supabase.table("usuarios").select("*").eq("cedula", cedula_input.strip()).execute()
                if res.data:
                    st.session_state.cedula = cedula_input.strip()
                    st.session_state.usuario_data = res.data[0]
                    st.session_state.tiempo_inicio = time.time()
                    st.success(f"Bienvenido/a {res.data[0]['nombres']}")
                    st.rerun()
                else:
                    st.error("Cédula no registrada. Por favor solicite su registro al Departamento de RRHH / Administración.")

else:
    # Pantalla principal del trabajador
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**Trabajador:** {st.session_state.usuario_data['nombres']}")
        st.write(f"**Empresa:** {st.session_state.usuario_data['empresa']}")
    with col2:
        if st.button("Cerrar Sesión / Guardar Progreso"):
            # Guardar tiempo acumulado en la sesión
            tiempo_fin = time.time()
            minutos = round((tiempo_fin - st.session_state.tiempo_inicio) / 60, 2)
            
            # Limitar a máximo 30 minutos por sesión diaria
            if minutos > 30:
                minutos = 30.0
                
            if minutos > 0.5: # Guardar solo si estuvo más de 30 segundos
                supabase.table("registro_tiempos").insert({
                    "cedula": st.session_state.cedula,
                    "eje": st.session_state.usuario_data['eje_actual'],
                    "modulo": "1.1",
                    "minutos_acumulados": minutos,
                    "hora_inicio": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.session_state.tiempo_inicio)),
                    "hora_fin": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tiempo_fin))
                }).execute()
                st.info(f"Se registraron {minutos} minutos de capacitación en tu historial.")

            st.session_state.cedula = None
            st.rerun()

    st.markdown("---")
    st.markdown("### Eje 1: Derechos Laborales de Mujeres y Hombres")
    st.info("⏱️ Recuerda realizar un máximo de **30 minutos diarios** de lectura y actividades.")
    
    # Contenido del Módulo 1.1
    st.markdown("""
    #### Módulo 1.1: Marco Legal Nacional e Internacional
    * **Constitución de la República del Ecuador (Art. 33 y 329):** El trabajo es un derecho y un deber social. Se garantiza la igualdad de oportunidades y la no discriminación en el acceso y permanencia laboral.
    * **Convenios OIT 100 y 111:** Normativa internacional ratificada por Ecuador referente a la igualdad de remuneración y la eliminación de todo tipo de discriminación laboral.
    """)
