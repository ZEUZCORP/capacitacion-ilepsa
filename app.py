import streamlit as st
from contenidos import SECCIONES
import random
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Plataforma de Capacitación y Cumplimiento Normativo",
    page_icon="🛡️",
    layout="wide"
)

# Inicialización de estados de sesión
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "cedula" not in st.session_state:
    st.session_state.cedula = ""
if "empresa" not in st.session_state:
    st.session_state.empresa = ""
if "logueado" not in st.session_state:
    st.session_state.logueado = False
if "seccion_actual" not in st.session_state:
    st.session_state.seccion_actual = 1
if "respuestas_usuario" not in st.session_state:
    st.session_state.respuestas_usuario = {}
if "secciones_completadas" not in st.session_state:
    st.session_state.secciones_completadas = set()

TOTAL_SECCIONES = len(SECCIONES)

# ----------------- PANTALLA DE ACCESO / LOGIN -----------------
if not st.session_state.logueado:
    st.title("🛡️ Sistema de Gestión y Capacitación Integral Corporativa")
    st.markdown("### Programa de Formación Obligatorio (40 Horas Académicas)")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("Por favor, ingrese sus datos institucionales para registrar su avance en el sistema de cumplimiento normativo.")
        
        with st.form("form_login"):
            nombre_input = st.text_input("Nombre y Apellido Completo:")
            cedula_input = st.text_input("Número de Cédula / Identificación:")
            empresa_input = st.text_input("Nombre de la Empresa u Organización:", value="Corporación / Empresa")
            
            submitted = st.form_submit_button("Ingresar a la Plataforma")
            
            if submitted:
                if nombre_input.strip() and cedula_input.strip():
                    st.session_state.usuario = nombre_input.strip()
                    st.session_state.cedula = cedula_input.strip()
                    st.session_state.empresa = empresa_input.strip()
                    st.session_state.logueado = True
                    st.rerun()
                else:
                    st.error("Por favor, complete su nombre y número de identificación para continuar.")
    with col2:
        st.markdown("#### 📋 Estructura del Programa:")
        st.markdown(f"- **Módulos Totales:** {TOTAL_SECCIONES} Secciones.")
        st.markdown("- **Ejes:** Derechos Laborales, Seguridad, Calidad, y **Módulo Adicional Obligatorio** (Igualdad de Género, No Violencia, Trabajo de Igual Valor).")
        st.markdown("- **Certificación:** Válida al completar el 100% de las evaluaciones.")

else:
    # ----------------- PLATAFORMA PRINCIPAL -----------------
    
    # Barra lateral de navegación y progreso
    st.sidebar.title("Panel de Control")
    st.sidebar.markdown(f"**Colaborador(a):** {st.session_state.usuario}")
    st.sidebar.markdown(f"**Cédula:** {st.session_state.cedula}")
    st.sidebar.markdown(f"**Organización:** {st.session_state.empresa}")
    st.sidebar.markdown("---")
    
    # Cálculo de progreso
    completadas = len(st.session_state.secciones_completadas)
    progreso = completadas / TOTAL_SECCIONES
    
    st.sidebar.markdown(f"### Progreso General: {completadas} / {TOTAL_SECCIONES}")
    st.sidebar.progress(progreso)
    
    menu = st.sidebar.radio(
        "Navegación:",
        ["📚 Módulo de Estudio y Evaluaciones", "🏆 Certificado Oficial", "🚪 Cerrar Sesión"]
    )
    
    if menu == "🚪 Cerrar Sesión":
        st.session_state.logueado = False
        st.session_state.usuario = ""
        st.session_state.cedula = ""
        st.rerun()

    # ----------------- VISTA DE ESTUDIO Y EVALUACIONES -----------------
    if menu == "📚 Módulo de Estudio y Evaluaciones":
        st.title("📖 Programa de Capacitación y Cumplimiento Normativo")
        st.markdown("Lea detenidamente el contenido de la sección y responda la evaluación para registrar su avance en el centro de trabajo.")
        st.markdown("---")
        
        # Selector rápido de sección
        ids_secciones = [s["id"] for s in SECCIONES]
        seleccion_idx = st.selectbox(
            "Seleccione la Sección a cursar:",
            options=ids_secciones,
            index=ids_secciones.index(st.session_state.seccion_actual),
            format_func=lambda x: f"Sección {x}: {SECCIONES[x-1]['titulo']}"
        )
        st.session_state.seccion_actual = seleccion_idx
        
        seccion_actual_data = SECCIONES[st.session_state.seccion_actual - 1]
        
        # Mostrar metadatos de la sección
        st.markdown(f"### `{seccion_actual_data['eje']}`")
        st.markdown(f"## {seccion_actual_data['titulo']}")
        
        # Contenido principal
        st.markdown(seccion_actual_data["contenido"])
        st.markdown("---")
        
        # Sección de Pregunta y Evaluación
        st.markdown("### ✍️ Evaluación de Comprensión")
        st.markdown(f"**Pregunta:** {seccion_actual_data['pregunta']}")
        
        # Opciones de respuesta
        opciones = seccion_actual_data["opciones"]
        respuesta_key = f"resp_{seccion_actual_data['id']}"
        
        seleccion_usuario = st.radio(
            "Seleccione la respuesta correcta:",
            options=opciones,
            key=respuesta_key,
            index=None if respuesta_key not in st.session_state.respuestas_usuario else opciones.index(st.session_state.respuestas_usuario.get(respuesta_key))
        )
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            enviar_resp = st.button("Verificar Respuesta")
            
        if enviar_resp:
            if seleccion_usuario is not None:
                st.session_state.respuestas_usuario[respuesta_key] = seleccion_usuario
                if seleccion_usuario == seccion_actual_data["correcta"]:
                    st.success("¡Respuesta Correcta! Has demostrado comprensión clave de este estándar corporativo.")
                    st.session_state.secciones_completadas.add(seccion_actual_data["id"])
                    st.rerun()
                else:
                    st.error("Respuesta incorrecta. Revise nuevamente el contenido de la sección e intente otra opción.")
            else:
                st.warning("Por favor, seleccione una opción antes de verificar.")
                
        # Controles de navegación inferior
        st.markdown("---")
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.session_state.seccion_actual > 1:
                if st.button("⬅️ Sección Anterior"):
                    st.session_state.seccion_actual -= 1
                    st.rerun()
        with col_nav2:
            if st.session_state.seccion_actual < TOTAL_SECCIONES:
                if st.button("Siguiente Sección ➡️"):
                    st.session_state.seccion_actual += 1
                    st.rerun()

    # ----------------- VISTA DE CERTIFICADO OFICIAL -----------------
    elif menu == "🏆 Certificado Oficial":
        st.title("🏆 Certificado de Aprobación del Programa")
        st.markdown("---")
        
        if len(st.session_state.secciones_completadas) == TOTAL_SECCIONES:
            st.success("¡Felicitaciones! Has completado exitosamente las 150 secciones del programa de capacitación y cumplimiento normativo.")
            
            # Plantilla visual del Certificado
            st.markdown(
                f"""
                <div style="border: 5px solid #2e7d32; padding: 40px; border-radius: 15px; background-color: #f9fbf9; text-align: center; color: #333;">
                    <h1 style="color: #1b5e20; font-family: serif;">CERTIFICADO DE APROBACIÓN</h1>
                    <p style="font-size: 18px; color: #555;">Este reconocimiento se otorga a:</p>
                    <h2 style="color: #0d47a1; text-decoration: underline;">{st.session_state.usuario}</h2>
                    <p style="font-size: 16px;"><b>Identificación (Cédula):</b> {st.session_state.cedula} | <b>Organización:</b> {st.session_state.empresa}</p>
                    <hr style="width: 50%; margin: 20px auto; border: 1px solid #c8e6c9;">
                    <p style="font-size: 16px; line-height: 1.6;">
                        Por haber cursado, superado y aprobado satisfactoriamente las <b>150 secciones especializadas</b> (40 horas académicas auditadas) 
                        en materia de Derechos Laborales, Seguridad, Prevención de Riesgos, Igualdad de Género, No Discriminación y Trabajo de Igual Valor en todo el centro de trabajo.
                    </p>
                    <p style="font-size: 14px; color: #666; margin-top: 30px;">Fecha de Emisión: {datetime.now().strftime('%d/%m/%Y')}</p>
                    <br>
                    <div style="display: inline-block; border-top: 2px solid #333; padding-top: 5px; width: 250px;">
                        <b>Gerencia General / Dirección</b><br>
                        <span>Representación Legal Autorizada</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🖨️ Imprimir / Guardar Certificado"):
                st.info("Utilice la función de su navegador (Ctrl+P / Cmd+P) para exportar este certificado en formato PDF o imprimirlo físicamente.")
        else:
            st.warning(f"Aún tienes secciones pendientes. Has completado **{len(st.session_state.secciones_completadas)} de {TOTAL_SECCIONES}** secciones.")
            st.info("Para desbloquear y visualizar tu certificado oficial, debes completar el 100% de las evaluaciones en el 'Módulo de Estudio'.")
