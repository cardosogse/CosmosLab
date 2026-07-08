import streamlit as st
import pandas as pd

try:
    from database import (
        inicializar_db, validar_token, liberar_token, obtener_datos_usuario,
        generar_token, listar_todos_los_tokens, revocar_eliminar_token, forzar_liberacion_sesion,
        obtener_password_admin, actualizar_password_admin
    )
    from assets import cargar_estilos, mezclar_memorama
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
    from modulos.modulo2 import mostrar_modulo2

except Exception as e:
    st.set_page_config(page_title="MainLab - Diagnóstico", layout=\"wide\", page_icon="🚨")
    st.error("🚨 MONITOR DE CONTROL: ERROR DE COMPILACIÓN DETECTADO EN LOS MÓDULOS")
    st.markdown("---")
    st.markdown(f"**Tipo de Fallo detectado:** `{type(e).__name__}`")
    if hasattr(e, 'filename') and e.filename:
        st.error(f"📁 **Archivo roto real:** `{e.filename}`")
    if hasattr(e, 'lineno') and e.lineno:
        st.warning(f"🔢 **Línea exacta del conflicto:** Renglón `{e.lineno}`")
    if hasattr(e, 'text') and e.text:
        st.code(f"Código conflictivo:\n{e.text}")
    st.stop()

# Configuración estructural de Streamlit
st.set_page_config(page_title="MainLab Pro - Entorno Químico", layout="wide", page_icon="🔬")
inicializar_db()
cargar_estilos()

# Inicialización segura de st.session_state
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'token_actual' not in st.session_state: st.session_state['token_actual'] = None
if 'identificador_usuario' not in st.session_state: st.session_state['identificador_usuario'] = ""
if 'modulo_actual' not in st.session_state: st.session_state['modulo_actual'] = 1
if 'puntos_acumulados' not in st.session_state: st.session_state['puntos_acumulados'] = 0
if 'vidas' not in st.session_state: st.session_state['vidas'] = 3
if 'errores_quiz' not in st.session_state: st.session_state['errores_quiz'] = 0
if 'modo_acceso_index' not in st.session_state: st.session_state['modo_acceso_index'] = 0

# Título de Infraestructura Centralizada
st.markdown("<h1 class='main-title'>🔬 MainLab Academic</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8a99ad; margin-bottom:30px;'>Ecosistema Avanzado para la Simulación y Evaluación en Ciencias Biológicas</p>", unsafe_allow_html=True)

# Configuración de navegación lateral reactiva
modo_acceso = st.sidebar.radio(
    "Navegación del Entorno:",
    options=["🎓 Portal del Estudiante", "💻 Consola del Administrador"],
    index=st.session_state['modo_acceso_index']
)

# Sincronizar el estado del radio por si el usuario hace clic directamente
if modo_acceso == "🎓 Portal del Estudiante":
    st.session_state['modo_acceso_index'] = 0
else:
    st.session_state['modo_acceso_index'] = 1

# ==========================================
# INTERFAZ 1: PORTAL DEL ESTUDIANTE
# ==========================================
if modo_acceso == "🎓 Portal del Estudiante":
    if not st.session_state['auth']:
        st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#ffffff; margin-top:0; text-align:center;'>🔑 Control de Acceso Cuántico</h3>", unsafe_allow_html=True)
        
        token_input = st.text_input("Introduce tu Token de Acceso o Clave Maestra:", type="password", placeholder="SYNAPSIS-PRO-XXXX")
        password_maestra = obtener_password_admin()
        
        if st.button("Validar Credenciales en Red", use_container_width=True):
            if token_input == "":
                st.warning("Por favor, ingrese un token válido.")
            elif token_input == password_maestra:
                st.success("🔓 ¡ACCESO DE ADMINISTRADOR AUTENTICADO CON ÉXITO!")
                st.session_state['auth'] = True
                st.session_state['modo_acceso_index'] = 1  # Cambia automáticamente a la consola
                st.rerun()
            else:
                es_valido, usuario, modulo, pts, vds = validar_token(token_input)
                if es_valido:
                    st.session_state['auth'] = True
                    st.session_state['token_actual'] = token_input
                    st.session_state['identificador_usuario'] = usuario
                    st.session_state['modulo_actual'] = modulo
                    st.session_state['puntos_acumulados'] = pts
                    st.session_state['vidas'] = vds
                    st.success(f"🔬 Conexión establecida. Bienvenido, Operador {usuario}.")
                    st.rerun()
                else:
                    st.error("🚨 Token inválido, revocado o expirado en la base de datos central.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # Barra lateral informativa del Alumno
    with st.sidebar:
        st.markdown("### 👨‍🔬 Operador Activo")
        st.write(f"**Usuario:** `{st.session_state['identificador_usuario']}`")
        st.write(f"**Token:** `{st.session_state['token_actual']}`")
        st.metric("Puntuación Acumulada", f"{st.session_state['puntos_acumulados']} PTS")
        st.markdown(f"**Estabilidad de Entorno:** `💔 {st.session_state['vidas']} / 3 Vidas`")
        st.markdown("---")
        if st.button("🚪 Cerrar Sesión Segura", use_container_width=True):
            if st.session_state['token_actual']:
                liberar_token(st.session_state['token_actual'])
            st.session_state.clear()
            st.rerun()

    # Procesar lógica de vidas agotadas
    if st.session_state['vidas'] <= 0:
        st.error("🚨 COLAPSO METABÓLICO: Lisis celular detectada por acumulación de fallos.")
        if st.button("Reiniciar Entorno Fisiológico (Recargar Vidas)"):
            st.session_state['vidas'] = 3
            st.rerun()
    else:
        # Enrutamiento de unidades académicas
        if st.session_state['modulo_actual'] == 1:
            st.markdown("<h2 style='color:#ffffff; margin-top:0;'>Unidad 1: Fundamentos de Química Biológica</h2>", unsafe_allow_html=True)
            
            estacion_actual = st.radio(
                "Cronograma de Trabajo:",
                options=[
                    "📅 Estación: Día 1 (Fases y Modelos)",
                    "📅 Estación: Día 2 (Estructura y Bioelementos)",
                    "📅 Estación: Día 3 (Fusión e Interacciones)",
                    "📅 Estación: Día 4 (Homeostasis y pH)"
                ],
                horizontal=True,
                label_visibility="collapsed"
            )

            if "Día 1" in estacion_actual:
                mostrar_dia1()
            elif "Día 2" in estacion_actual:
                mostrar_dia2()
            elif "Día 3" in estacion_actual:
                mostrar_dia3()
            else:
                mostrar_dia4()
        else:
            mostrar_modulo2()

# ==========================================
# INTERFAZ 2: CONSOLA DEL ADMINISTRADOR
# ==========================================
else:
    st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>💻 Panel de Control de Infraestructura</h2>", unsafe_allow_html=True)
    
    pass_maestra = obtener_password_admin()
    if 'admin_auth' not in st.session_state: st.session_state['admin_auth'] = False
    
    if not st.session_state['admin_auth'] and not st.session_state['auth']:
        input_pass = st.text_input("Contraseña del Sistema:", type="password")
        if st.button("Desbloquear Consola"):
            if input_pass == pass_maestra:
                st.session_state['admin_auth'] = True
                st.rerun()
            else:
                st.error("Acceso denegado.")
        st.stop()

    st.session_state['admin_auth'] = True

    # Pestañas de administración de base de datos
    tab1, tab2, tab3 = st.tabs(["🎫 Emisión de Cupones", "📊 Monitor de Sesiones", "⚙️ Seguridad"])
    
    with tab1:
        st.markdown("### Generador de Licencias Únicas")
        c1, c2 = st.columns(2)
        with c1:
            u_id = st.text_input("Identificador / Matrícula del Alumno:", placeholder="JuanPerez_2026")
            dias_val = st.number_value = st.slider("Días de vigencia del Token:", 1, 90, 30)
        with c2:
            st.write("")
            st.write("")
            if st.button("Fabricar Token Autorizado", use_container_width=True):
                if u_id:
                    nuevo_tok = generar_token(dias_val, u_id)
                    st.success(f"Token Creado: `{nuevo_tok}` asignado a {u_id}")
                else:
                    st.warning("Introduzca un identificador.")
                    
    with tab2:
        st.markdown("### Estado de la Capa de Persistencia (SQLite)")
        tokens_db = listar_todos_los_tokens()
        if tokens_db:
            df = pd.DataFrame(tokens_db, columns=["Token de Acceso", "Estado de Sesión", "Vigencia Remanente", "Puntos", "Vidas", "Progreso Actual"])
            st.dataframe(df, use_container_width=True)
            
            st.markdown("### Acciones Quirúrgicas de Rescate")
            c_tok = st.selectbox("Seleccionar Token Objetivo:", df["Token de Acceso"].tolist())
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Forzar Liberación de Sesión (Anti-Bloqueo)", use_container_width=True):
                    forzar_liberacion_sesion(c_tok)
                    st.success("Sesión restaurada a estado Libre.")
                    st.rerun()
            with col_b2:
                if st.button("Revocar y Eliminar Token del Registro", use_container_width=True):
                    revocar_eliminar_token(c_tok)
                    st.error("Token eliminado.")
                    st.rerun()
        else:
            st.info("No hay tokens registrados en la base de datos.")
            
    with tab3:
        st.markdown("### Configuración de Seguridad Global")
        nueva_pass = st.text_input("Actualizar Contraseña Maestra de Administrador:", type="password", placeholder="Mínimo 6 caracteres")
        if st.button("Sobrescribir Credencial"):
            if len(nueva_pass) >= 4:
                actualizar_password_admin(nueva_pass)
                st.success("Contraseña del sistema actualizada con éxito.")
            else:
                st.error("Contraseña demasiado corta.")
                
    if st.sidebar.button("🚪 Salir de Consola", use_container_width=True):
        st.session_state.clear()
        st.rerun()
        
