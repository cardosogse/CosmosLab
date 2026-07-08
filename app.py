import streamlit as st
import pandas as pd
from database import (
    inicializar_db, validar_token, liberar_token, obtener_datos_usuario,
    generar_token, listar_todos_los_tokens, revocar_eliminar_token, forzar_liberacion_sesion
)
from assets import cargar_estilos, mezclar_memorama
# Importación directa de estaciones sin pasar por intermediarios corruptos
from modulos.m1_dia1 import mostrar_dia1
from modulos.m1_dia2 import mostrar_dia2
from modulos.m1_dia3 import mostrar_dia3
from modulos.m1_dia4 import mostrar_dia4
from modulos.modulo2 import mostrar_modulo2

st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
inicializar_db()

st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Entorno Virtual de Simulación Bioquímica para Ciencias Biológicas</p>", unsafe_allow_html=True)

st.sidebar.title("🛠️ Consola del Sistema")
modo_acceso = st.sidebar.radio("Selecciona tu Terminal:", ["Portal del Estudiante", "Consola del Administrador"])

if "auth" not in st.session_state: st.session_state["auth"] = False
if "token_actual" not in st.session_state: st.session_state["token_actual"] = ""
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "errores_quiz" not in st.session_state: st.session_state["errores_quiz"] = 0
if "advertencia_ph" not in st.session_state: st.session_state["advertencia_ph"] = False
if "puntos_acumulados" not in st.session_state: st.session_state["puntos_acumulados"] = 0
if "racha_consecutiva" not in st.session_state: st.session_state["racha_consecutiva"] = 0
if "licencia_extendida" not in st.session_state: st.session_state["licencia_extendida"] = False
if "memo_reveladas" not in st.session_state: st.session_state["memo_reveladas"] = []
if "memo_resueltas" not in st.session_state: st.session_state["memo_resueltas"] = []
if "memo_completado" not in st.session_state: st.session_state["memo_completado"] = False
if "memo_tablero" not in st.session_state: st.session_state["memo_tablero"] = mezclar_memorama()

if modo_acceso == "Consola del Administrador":
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.subheader("🔑 Autenticación de Seguridad del Administrador")
    clave_admin = st.text_input("Introduce la Clave Maestra de Infraestructura:", type="password")
    
    if clave_admin == "UNAM2026":
        st.success("Acceso verificado a los servicios centrales de SQLite.")
        tab_generar, tab_control = st.tabs(["🆕 Generar Nuevos Tokens", "📊 Monitor de Alumnos en Tiempo Real"])
        
        with tab_generar:
            vigencia = st.number_input("Días de vigencia del token:", min_value=1, max_value=365, value=30)
            if st.button("Emitir Cupón de Acceso"):
                nuevo_tok = generar_token(vigencia)
                st.code(f"TOKEN EMITIDO: {nuevo_tok}", language="text")
                st.toast(f"Token {nuevo_tok} inyectado con éxito.")
                
        with tab_control:
            datos_raw = listar_todos_los_tokens()
            if datos_raw:
                df = pd.DataFrame(datos_raw, columns=["Token", "Activo", "Días Restantes", "Puntos", "Vidas", "Módulo Máx"])
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.markdown("#### Operaciones Críticas sobre la Base de Datos")
                col_tok_sel, col_btn_lib, col_btn_del = st.columns([2, 1, 1])
                with col_tok_sel:
                    token_seleccionado = st.selectbox("Selecciona un Token para Operar:", df["Token"].tolist())
                with col_btn_lib:
                    if st.button("🔓 Forzar Cierre", use_container_width=True):
                        forzar_liberacion_sesion(token_seleccionado)
                        st.success("Sesión liberada.")
                        st.rerun()
                with col_btn_del:
                    if st.button("🚨 Revocar Licencia", use_container_width=True):
                        revocar_eliminar_token(token_seleccionado)
                        st.warning("Token destruido.")
                        st.rerun()
            else: st.info("Base de datos vacía.")
    elif clave_admin != "": st.error("Clave incorrecta.")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    if not st.session_state["auth"]:
        st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
        st.subheader("🔒 Acceso a Estaciones de Trabajo")
        token_input = st.text_input("Introduce tu Token de Suscripción Autorizado:", type="password")
        
        if st.button("Conectar e Inicializar Simuladores", use_container_width=True):
            if token_input.strip():
                es_valido, mensaje = validar_token(token_input)
                if es_valido:
                    datos = obtener_datos_usuario(token_input.strip().upper())
                    st.session_state["auth"] = True
                    st.session_state['token_actual'] = token_input.strip().upper()
                    st.session_state['puntos_acumulados'] = datos[0]
                    st.session_state['vidas'] = datos[1]
                    if datos[2] >= 2: st.session_state["memo_completado"] = True
                    st.rerun()
                else: st.error(f"Fallo de conexión: {mensaje}")
            else: st.warning("Digita un token.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        with st.sidebar:
            st.markdown(f"**Usuario:** `{st.session_state['token_actual']}`")
            st.markdown(f"**Marcador:** `🪙 {st.session_state['puntos_acumulados']} PTS`")
            st.markdown(f"**Estabilidad:** `💔 {st.session_state['vidas']} / 3`")
            if st.button("🚪 Cerrar Sesión Segura", use_container_width=True):
                liberar_token(st.session_state['token_actual'])
                st.session_state.clear()
                st.rerun()
        
        if st.session_state['vidas'] <= 0:
            st.error("🚨 COLAPSO METABÓLICO: Lisis celular detectada por acumulación de fallos.")
            if st.button("Reiniciar Entorno Fisiológico"):
                st.session_state['vidas'] = 3
                st.rerun()
        else:
            # Enrutamiento directo integrado (Adiós modulo1.py corrupto)
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
            st.markdown("---")

            if "Día 1" in estacion_actual:
                mostrar_dia1()
            elif "Día 2" in estacion_actual:
                mostrar_dia2()
            elif "Día 3" in estacion_actual:
                mostrar_dia3()
            else:
                mostrar_dia4()import streamlit as st
import pandas as pd
from database import (
    inicializar_db, validar_token, liberar_token, obtener_datos_usuario,
    generar_token, listar_todos_los_tokens, revocar_eliminar_token, forzar_liberacion_sesion
)
from assets import cargar_estilos, mezclar_memorama
from modulos.modulo1 import mostrar_modulo1
from modulos.modulo2 import mostrar_modulo2

st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
inicializar_db()

st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Entorno Virtual de Simulación Bioquímica para Ciencias Biológicas</p>", unsafe_allow_html=True)

st.sidebar.title("🛠️ Consola del Sistema")
modo_acceso = st.sidebar.radio("Selecciona tu Terminal:", ["Portal del Estudiante", "Consola del Administrador"])

if "auth" not in st.session_state: st.session_state["auth"] = False
if "token_actual" not in st.session_state: st.session_state["token_actual"] = ""
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "errores_quiz" not in st.session_state: st.session_state["errores_quiz"] = 0
if "advertencia_ph" not in st.session_state: st.session_state["advertencia_ph"] = False
if "puntos_acumulados" not in st.session_state: st.session_state["puntos_acumulados"] = 0
if "racha_consecutiva" not in st.session_state: st.session_state["racha_consecutiva"] = 0
if "licencia_extendida" not in st.session_state: st.session_state["licencia_extendida"] = False
if "memo_reveladas" not in st.session_state: st.session_state["memo_reveladas"] = []
if "memo_resueltas" not in st.session_state: st.session_state["memo_resueltas"] = []
if "memo_completado" not in st.session_state: st.session_state["memo_completado"] = False
if "memo_tablero" not in st.session_state: st.session_state["memo_tablero"] = mezclar_memorama()

if modo_acceso == "Consola del Administrador":
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.subheader("🔑 Autenticación de Seguridad del Administrador")
    clave_admin = st.text_input("Introduce la Clave Maestra de Infraestructura:", type="password")
    
    if clave_admin == "UNAM2026":
        st.success("Acceso verificado a los servicios centrales de SQLite.")
        tab_generar, tab_control = st.tabs(["🆕 Generar Nuevos Tokens", "📊 Monitor de Alumnos en Tiempo Real"])
        
        with tab_generar:
            vigencia = st.number_input("Días de vigencia del token:", min_value=1, max_value=365, value=30)
            if st.button("Emitir Cupón de Acceso"):
                nuevo_tok = generar_token(vigencia)
                st.code(f"TOKEN EMITIDO: {nuevo_tok}", language="text")
                st.toast(f"Token {nuevo_tok} inyectado con éxito.")
                
        with tab_control:
            datos_raw = listar_todos_los_tokens()
            if datos_raw:
                df = pd.DataFrame(datos_raw, columns=["Token", "Activo", "Días Restantes", "Puntos", "Vidas", "Módulo Máx"])
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.markdown("#### Operaciones Críticas sobre la Base de Datos")
                col_tok_sel, col_btn_lib, col_btn_del = st.columns([2, 1, 1])
                with col_tok_sel:
                    token_seleccionado = st.selectbox("Selecciona un Token para Operar:", df["Token"].tolist())
                with col_btn_lib:
                    if st.button("🔓 Forzar Cierre", use_container_width=True):
                        forzar_liberacion_sesion(token_seleccionado)
                        st.success("Sesión liberada.")
                        st.rerun()
                with col_btn_del:
                    if st.button("🚨 Revocar Licencia", use_container_width=True):
                        revocar_eliminar_token(token_seleccionado)
                        st.warning("Token destruido.")
                        st.rerun()
            else: st.info("Base de datos vacía.")
    elif clave_admin != "": st.error("Clave incorrecta.")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    if not st.session_state["auth"]:
        st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
        st.subheader("🔒 Acceso a Estaciones de Trabajo")
        token_input = st.text_input("Introduce tu Token de Suscripción Autorizado:", type="password")
        
        if st.button("Conectar e Inicializar Simuladores", use_container_width=True):
            if token_input.strip():
                es_valido, mensaje = validar_token(token_input)
                if es_valido:
                    datos = obtener_datos_usuario(token_input.strip().upper())
                    st.session_state["auth"] = True
                    st.session_state['token_actual'] = token_input.strip().upper()
                    st.session_state['puntos_acumulados'] = datos[0]
                    st.session_state['vidas'] = datos[1]
                    if datos[2] >= 2: st.session_state["memo_completado"] = True
                    st.rerun()
                else: st.error(f"Fallo de conexión: {mensaje}")
            else: st.warning("Digita un token.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        with st.sidebar:
            st.markdown(f"**Usuario:** `{st.session_state['token_actual']}`")
            st.markdown(f"**Marcador:** `🪙 {st.session_state['puntos_acumulados']} PTS`")
            st.markdown(f"**Estabilidad:** `💔 {st.session_state['vidas']} / 3`")
            if st.button("🚪 Cerrar Sesión Segura", use_container_width=True):
                liberar_token(st.session_state['token_actual'])
                st.session_state.clear()
                st.rerun()
        
        if st.session_state['vidas'] <= 0:
            st.error("🚨 COLAPSO METABÓLICO: Lisis celular detectada por acumulación de fallos.")
            if st.button("Reiniciar Entorno Fisiológico"):
                st.session_state['vidas'] = 3
                st.rerun()
        else:
            mostrar_modulo1()
