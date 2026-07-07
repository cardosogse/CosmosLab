import streamlit as st
import pandas as pd
from database import (
    inicializar_db, validar_token, liberar_token, obtener_datos_usuario,
    generar_token, listar_todos_los_tokens, revocar_eliminar_token, forzar_liberacion_sesion
)
from assets import cargar_estilos
from modulos.modulo1 import mostrar_modulo1

# Configuración del servidor y chasis responsivo
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
inicializar_db()

# Identidad visual corporativa limpia
st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Entorno Virtual de Simulación Bioquímica para Ciencias Biológicas</p>", unsafe_allow_html=True)

# CONTROLADOR DE VISTAS PRINCIPALES: SIDEBAR DE ACCESOS
st.sidebar.title("🛠️ Consola del Sistema")
modo_acceso = st.sidebar.radio("Selecciona tu Terminal:", ["Portal del Estudiante", "Consola del Administrador"])

# ========================================================
# VISTA A: CONSOLA DEL ADMINISTRADOR (RECUPERADA Y MEJORADA)
# ========================================================
if modo_acceso == "Consola del Administrador":
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.subheader("🔑 Autenticación de Seguridad del Administrador")
    clave_admin = st.text_input("Introduce la Clave Maestra de Infraestructura:", type="password")
    
    # CLAVE DE SEGURIDAD CONFIGURABLE (Cambia 'UNAM2026' por la que gustes)
    if clave_admin == "UNAM2026":
        st.success("Acceso concedido a la Consola de Infraestructura de MainLab.")
        st.markdown("---")
        
        tab_generar, tab_control = st.tabs(["🆕 Generar Nuevos Tokens", "📊 Monitor de Alumnos en Tiempo Real"])
        
        with tab_generar:
            st.write("Emite licencias de acceso temporal para los estudiantes del tronco común:")
            vigencia = st.number_input("Días de vigencia del token:", min_value=1, max_value=365, value=30)
            if st.button("Emitir Cupón de Acceso"):
                nuevo_tok = generar_token(vigencia)
                st.code(f"TOKEN EMITIDO: {nuevo_tok}", language="text")
                st.toast(f"Token {nuevo_tok} inyectado con éxito en la BD.")
                
        with tab_control:
            st.write("Control total de sesiones de alumnos y limpieza de base de datos:")
            datos_raw = listar_todos_los_tokens()
            
            if datos_raw:
                df = pd.DataFrame(datos_raw, columns=["Token", "En Uso (Activo)", "Días Restantes", "Puntos", "Vidas", "Día Máx Aprobado"])
                st.dataframe(df, use_container_width=True)
                
                st.markdown("#### Operaciones Críticas sobre la Base de Datos")
                col_tok_sel, col_btn_lib, col_btn_del = st.columns([2, 1, 1])
                
                with col_tok_sel:
                    token_seleccionado = st.selectbox("Selecciona un Token para Operar:", df["Token"].tolist())
                with col_btn_lib:
                    if st.button("🔓 Forzar Cierre de Sesión", help="Libera el estado 'En Uso' si el alumno dejó la pantalla congelada."):
                        forzar_liberacion_sesion(token_seleccionado)
                        st.success(f"Token {token_seleccionado} liberado.")
                        st.rerun()
                with col_btn_del:
                    if st.button("🚨 Revocar y Eliminar Cupón", help="Borra permanentemente al alumno de la base de datos."):
                        revocar_eliminar_token(token_seleccionado)
                        st.warning(f"Token {token_seleccionado} destruido.")
                        st.rerun()
            else:
                st.info("No existen tokens emitidos en la base de datos actual.")
    elif clave_admin != "":
        st.error("Clave de infraestructura incorrecta. Acceso denegado.")
    st.markdown("</div>", unsafe_allow_html=True)

# ========================================================
# VISTA B: TERMINAL DEL ESTUDIANTE (ENTORNO DE SIMULACIÓN)
# ========================================================
else:
    if 'token_activo' not in st.session_state:
        st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
        st.subheader("🔒 Acceso a Estaciones de Trabajo")
        token_input = st.text_input("Introduce tu Token de Suscripción Autorizado:", type="password")
        
        if st.button("Conectar e Inicializar Simuladores"):
            if token_input.strip():
                es_valido, mensaje = validar_token(token_input)
                if es_valido:
                    datos = obtener_datos_usuario(token_input)
                    st.session_state['token_activo'] = token_input.strip().upper()
                    st.session_state['puntos'] = datos[0]
                    st.session_state['vidas'] = datos[1]
                    st.session_state['dia_completado'] = datos[2]
                    st.success("Parámetros moleculares cargados con éxito.")
                    st.rerun()
                else:
                    st.error(f"Fallo de conexión: {mensaje}")
            else:
                st.warning("Por favor, digita un token de acceso.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        # Barra superior de salida segura del estudiante
        col_vacia, col_logout = st.columns([7, 1])
        with col_logout:
            if st.button("🚪 Cerrar Sesión Segura"):
                liberar_token(st.session_state['token_activo'])
                st.session_state.clear()
                st.rerun()
                
        st.markdown("---")
        # Invoca la bitácora de viaje modular
        mostrar_modulo1()
