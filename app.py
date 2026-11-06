import streamlit as st
import time

st.set_page_config(
    page_title="Plataforma ILEPSA - Ingreso",
    page_icon="🏢",
    layout="centered"
)

# Base de datos simulada de nombres corporativos asociados a la cédula
NOMBRES_COLABORADORES = {
    "9999999999": "Super Administrador ILEPSA",
    "1712345678": "Juan Carlos Pérez",
    "1787654321": "María Fernanda Andrade",
}

# Estilo formal corporativo
st.markdown("""
    <style>
    .card-login {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 5px solid #0284c7;
        padding: 35px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="card-login" style="text-align: center;">
        <h2 style="color: #0f172a; margin-top:0;">COMPAÑÍA ILEPSA S.A.</h2>
        <h4 style="color: #0284c7;">Sistema Oficial de Capacitación Obligatoria</h4>
        <p style="color: #64748b;">Acuerdo Ministerial MDT-2025-006</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

cedula_input = st.text_input("Ingrese su Cédula de Identidad para iniciar:", max_chars=10, type="password")

if st.button("Iniciar Sesión", type="primary", use_container_width=True):
    cedula_limpia = cedula_input.strip()
    if len(cedula_limpia) >= 10:
        # Guardar en session_state global
        st.session_state.cedula = cedula_limpia
        st.session_state.nombre_usuario = NOMBRES_COLABORADORES.get(cedula_limpia, f"Colaborador C.I. {cedula_limpia}")
        
        with st.spinner("Validando credenciales en el sistema ILEPSA..."):
            time.sleep(1)
            
        # Redirección nativa de Streamlit a la página dentro de /pages/
        st.switch_page("pages/capacitacion.py")
    else:
        st.error("Por favor ingrese un número de cédula válido de 10 dígitos.")
