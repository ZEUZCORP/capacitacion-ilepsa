import streamlit as st
from datetime import datetime
from contenidos import SECCIONES

# Configuración inicial de la página con diseño ampliado
st.set_page_config(
    page_title="Programa de Formación Integral y Obligatoria",
    page_icon="🎓",
    layout="centered"
)

# Inicializar variables de sesión
if "iniciado" not in st.session_state:
    st.session_state.iniciado = False
if "cedula" not in st.session_state:
    st.session_state.cedula = ""
if "seccion_actual" not in st.session_state:
    st.session_state.seccion_actual = 0
if "respuestas_correctas" not in st.session_state:
    st.session_state.respuestas_correctas = 0
if "chat_ia" not in st.session_state:
    st.session_state.chat_ia = []

# Base de datos simulada de sesiones activas y registros en tiempo real
if "registro_usuarios" not in st.session_state:
    st.session_state.registro_usuarios = {
        "1712345678": {"nombre": "Colaborador Ejemplo 1", "progreso": 45, "estado": "En progreso", "tiempo_min": 28, "ultimo_acceso": "Hace 5 min"},
        "1798765432": {"nombre": "Colaborador Ejemplo 2", "progreso": 100, "estado": "Certificado Emitido", "tiempo_min": 65, "ultimo_acceso": "Hace 2 min"},
        "0911223344": {"nombre": "Colaborador Ejemplo 3", "progreso": 12, "estado": "En progreso", "tiempo_min": 14, "ultimo_acceso": "Hace 12 min"}
    }

# Estilo visual interactivo, moderno y con animaciones CSS suaves
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.6s ease-out forwards;
    }
    .main-header {
        font-size: 28px;
        font-weight: 800;
        color: #1b365d;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 16px;
        color: #5c768d;
        text-align: center;
        margin-bottom: 25px;
    }
    .hero-card {
        background: linear-gradient(135deg, #1b365d 0%, #2c5282 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(27, 54, 93, 0.2);
        margin-bottom: 25px;
    }
    .info-box {
        background-color: #f8fafc;
        border-left: 5px solid #2b6cb0;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .admin-box {
        background-color: #eef2f7;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #319795;
        margin-bottom: 20px;
    }
    .ia-box {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border: 2px dashed #cbd5e0;
        padding: 20px;
        border-radius: 12px;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PANTALLA DE INICIO / PORTADA INTERACTIVA
# ---------------------------------------------------------
if not st.session_state.iniciado:
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Portada Interactiva y Visualmente Atractiva
    st.markdown("""
    <div class="hero-card">
        <h1 style="color: white; margin-top: 0; font-size: 26px;">🎓 Programa de Formación Integral y Obligatoria</h1>
        <p style="font-size: 16px; opacity: 0.9;">Capacitación general y corporativa orientada a la excelencia en el lugar de trabajo.</p>
        <hr style="border-color: rgba(255,255,255,0.2); margin: 15px 0;">
        <p style="font-size: 14px; margin-bottom: 0;">🛡️ Desarrollado en estricto cumplimiento con el <b>Acuerdo Ministerial MDT-2025-006</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box fade-in">
        <h3>📌 Indicaciones Importantes para el Personal:</h3>
        <ul>
            <li><b>Estructura Completa:</b> El programa consta de <b>100 secciones formativas</b> divididas en cuatro ejes fundamentales (Derechos Laborales, Género, Erradicación de Violencia y Trabajo de Igual Valor).</li>
            <li><b>Dedicación Diaria:</b> Se recomienda un tiempo mínimo de estudio de <b>30 minutos diarios</b> para un correcto aprendizaje y retención.</li>
            <li><b>Aprobación y Certificado:</b> Al culminar y aprobar las evaluaciones de todas las secciones, se desbloqueará de forma inmediata tu <b>certificado oficial de aprobación</b>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🔑 Acceso al Sistema")
    cedula_input = st.text_input("Ingrese su número de Cédula de Identidad:", max_chars=10, placeholder="Ej. 1712345678 (O admin: 9999999999)")
    
    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        iniciar_btn = st.button("Iniciar Capacitación", type="primary")
        
    if iniciar_btn:
        cedula_limpia = cedula_input.strip()
        if len(cedula_limpia) >= 10:
            st.session_state.iniciado = True
            st.session_state.cedula = cedula_limpia
            st.session_state.tiempo_inicio = datetime.now()
            
            # Registrar usuario en vivo si no es admin
            if cedula_limpia != "9999999999":
                if cedula_limpia not in st.session_state.registro_usuarios:
                    st.session_state.registro_usuarios[cedula_limpia] = {
                        "nombre": f"Colaborador Cédula {cedula_limpia}",
                        "progreso": 0,
                        "estado": "Iniciado",
                        "tiempo_min": 1,
                        "ultimo_acceso": "Justo ahora"
                    }
            st.rerun()
        else:
            st.error("⚠️ Por favor, ingrese un número de cédula válido de 10 dígitos.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PANEL DE SUPERADMINISTRADOR (CÉDULA: 9999999999)
# ---------------------------------------------------------
elif st.session_state.cedula == "9999999999":
    st.markdown('<div class="main-header">📊 Panel de Monitoreo y Control Gerencial</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Consola de Auditoría en Vivo - Acuerdo Ministerial MDT-2025-006</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="admin-box fade-in">
        <h4>Panel de Control Administrativo</h4>
        <p>Desde este entorno exclusivo, el superadministrador tiene visibilidad en tiempo real sobre la conectividad, tiempos de dedicación diarios, avance de secciones de los colaboradores y el registro de certificados emitidos en la plataforma.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("👥 Usuarios Registrados", len(st.session_state.registro_usuarios))
    col_m2.metric("📜 Certificados Emitidos", sum(1 for u in st.session_state.registro_usuarios.values() if u["progreso"] == 100))
    col_m3.metric("⏱️ Tiempo Promedio", "35 minutos")
    
    st.divider()
    st.subheader("🔍 Monitoreo de Colaboradores Conectados")
    
    for ced, datos in st.session_state.registro_usuarios.items():
        with st.expander(f"Cédula: {ced} | {datos['nombre']} — [Progreso: {datos['progreso']}%]"):
            st.write(f"**Estado del Colaborador:** {datos['estado']}")
            st.write(f"**Tiempo de Sesión Invertido:** {datos['tiempo_min']} minutos")
            st.write(f"**Última Actividad Registrada:** {datos['ultimo_acceso']}")
            st.progress(datos['progreso'] / 100.0, text=f"Avance actual: {datos['progreso']}%")
            
    st.divider()
    if st.button("Cerrar Sesión de Administrador", type="primary"):
        st.session_state.iniciado = False
        st.session_state.cedula = ""
        st.rerun()

# ---------------------------------------------------------
# DESARROLLO DE LAS 100 SECCIONES Y CONSULTAS CON IA
# ---------------------------------------------------------
else:
    total_secciones = len(SECCIONES)
    sec_idx = st.session_state.seccion_actual
    
    # Actualizar datos en vivo del usuario actual
    if st.session_state.cedula in st.session_state.registro_usuarios:
        progreso_pct = int((sec_idx / total_secciones) * 100)
        st.session_state.registro_usuarios[st.session_state.cedula]["progreso"] = progreso_pct
        st.session_state.registro_usuarios[st.session_state.cedula]["estado"] = "En progreso"
        st.session_state.registro_usuarios[st.session_state.cedula]["ultimo_acceso"] = "Activo ahora"
    
    # Barra de progreso general animada
    progreso_val = (sec_idx / total_secciones)
    st.progress(progreso_val, text=f"Progreso General: Sección {sec_idx + 1} de {total_secciones} ({int(progreso_val*100)}%)")
    
    if sec_idx < total_secciones:
        seccion = SECCIONES[sec_idx]
        
        st.markdown(f"### 🏷️ {seccion['eje']}")
        st.markdown(f"## 📌 {seccion['titulo']}")
        
        # Contenido de lectura en tarjeta limpia
        st.markdown(f"""
        <div class="info-box fade-in">
            {seccion['contenido']}
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Evaluación Interactiva de la Sección
        st.markdown("#### 📝 Evaluación de Aprendizaje")
        respuesta_usuario = st.radio(seccion['pregunta'], seccion['opciones'], key=f"p_{sec_idx}")
        
        col_env, col_esp = st.columns([1, 4])
        with col_env:
            if st.button("Enviar Respuesta", type="primary"):
                if respuesta_usuario == seccion['correcta']:
                    st.success("¡Respuesta correcta! Avanzando a la siguiente sección...")
                    st.session_state.respuestas_correctas += 1
                    st.session_state.seccion_actual += 1
                    st.rerun()
                else:
                    st.error("Respuesta incorrecta. Lee detenidamente el contenido y vuelve a intentarlo.")
                    
        # ---------------------------------------------------------
        # CUADRO INTERACTIVO DE LA IA (PREGUNTAS Y RESPUESTAS)
        # ---------------------------------------------------------
        st.markdown("""
        <div class="ia-box">
            <h4>🤖 Asistente Virtual de Capacitación (IA)</h4>
            <p style="font-size: 14px; color: #4a5568;">¿Tienes alguna duda sobre esta sección o sobre tus derechos laborales? Pregúntale a nuestro asistente integrado.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Interfaz de chat interactiva integrada
        pregunta_ia = st.text_input("Escribe tu pregunta sobre el contenido o la ley:", key=f"input_ia_{sec_idx}")
        if st.button("Consultar con la IA", key=f"btn_ia_{sec_idx}"):
            if pregunta_ia.strip():
                # Simulación de respuesta inteligente contextual basada en el eje activo
                if "Derechos" in seccion['eje']:
                    resp_ia = f"Respecto a tu consulta sobre '{pregunta_ia}', recuerda que la Constitución y el Código del Trabajo garantizan la irrenunciabilidad de derechos y la intangibilidad del sueldo en todo momento."
                elif "Género" in seccion['eje']:
                    resp_ia = f"Analizando tu pregunta sobre '{pregunta_ia}', la organización promueve activamente la igualdad de oportunidades, la eliminación de sesgos inconscientes y la paridad en el liderazgo."
                elif "Violencia" in seccion['eje']:
                    resp_ia = f"Sobre tu duda referente a '{pregunta_ia}', la empresa mantiene cero tolerancia al acoso laboral, garantizando absoluta confidencialidad en los canales de denuncia y protección contra represalias."
                else:
                    resp_ia = f"En relación con tu pregunta sobre '{pregunta_ia}', la ley exige transparencia salarial estricta y bandas de remuneración basadas en la valoración objetiva de puestos de trabajo."
                
                st.session_state.chat_ia.append({"pregunta": pregunta_ia, "respuesta": resp_ia})
                st.rerun()
            else:
                st.warning("Por favor, escribe una pregunta válida antes de consultar.")
                
        # Historial de preguntas interactivas recientes en esta sesión
        if st.session_state.chat_ia:
            with st.expander("💬 Historial de consultas a la IA en esta sesión"):
                for chat in reversed(st.session_state.chat_ia[-3:]):
                    st.markdown(f"**Tú:** {chat['pregunta']}")
                    st.markdown(f"**Asistente IA:** {chat['respuesta']}")
                    st.markdown("---")
    
    # ---------------------------------------------------------
    # PANTALLA FINAL Y EMISIÓN DE CERTIFICADO OFICIAL
    # ---------------------------------------------------------
    else:
        # Actualizar estado a certificado emitido en tiempo real
        if st.session_state.cedula in st.session_state.registro_usuarios:
            st.session_state.registro_usuarios[st.session_state.cedula]["progreso"] = 100
            st.session_state.registro_usuarios[st.session_state.cedula]["estado"] = "Certificado Emitido"
        
        st.balloons()
        st.markdown('<div class="main-header">🎉 ¡Felicitaciones! Has Culminado con Éxito las 100 Secciones</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="hero-card fade-in" style="text-align: center;">
            <h2>📜 Certificado Oficial de Aprobación</h2>
            <p>Se certifica formalmente que el colaborador con Cédula N° <b>{st.session_state.cedula}</b> ha completado satisfactoriamente las <b>100 secciones formativas</b> del Programa Integral bajo el marco normativo del <b>Acuerdo Ministerial MDT-2025-006</b>.</p>
            <hr style="border-color: rgba(255,255,255,0.2); margin: 20px 0;">
            <p><b>Evaluaciones Superadas con Éxito:</b> {st.session_state.respuestas_correctas} / {total_secciones}</p>
            <p style="font-size: 13px; opacity: 0.8;">Estado: Validado y Registrado en el Sistema</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Finalizar y Salir del Sistema", type="primary"):
            st.session_state.iniciado = False
            st.session_state.seccion_actual = 0
            st.session_state.respuestas_correctas = 0
            st.session_state.chat_ia = []
            st.rerun()
