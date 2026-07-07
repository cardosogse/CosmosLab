import streamlit as st
from database import (inicializar_db, validar_y_bloquear_token, obtener_datos_usuario, 
                      liberar_token, registrar_nuevo_usuario, forzar_cancelacion_licencia, eliminar_registro_token)
from assets import inyectar_css
from modulos.modulo1 import mostrar_modulo1, mezclar_memorama
from modulos.modulo2 import mostrar_modulo2

# ========================================================
# 🛠️ CAJAS VACÍAS TEMPORALES PARA IR MONTANDO POR CAPAS
# ========================================================
def mostrar_modulo3_temporal():
    st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>🧬 Módulo 3: Reactores de Enlace Bioquímico</h2>", unsafe_allow_html=True)
    st.info("🚧 **Estación en construcción.** Esta pieza de LEGO se activará en la siguiente actualización sin romper el sistema.")

def mostrar_modulo4_temporal():
    st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>🌡️ Módulo 4: Glucómica e Isomerismo</h2>", unsafe_allow_html=True)
    st.info("🚧 **Estación en construcción.** Esta pieza de LEGO se activará en la siguiente actualización sin romper el sistema.")

def mostrar_evaluacion_temporal():
    st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>🏆 Evaluación Final de la Bitácora</h2>", unsafe_allow_html=True)
    st.info("🚧 **Estación en construcción.** El examen final se habilitará automáticamente al terminar los módulos anteriores.")

# ========================================================
# GESTIÓN DEL ESTADO GLOBAL
# ========================================================
def inicializar_estado():
    if "auth" not in st.session_state: st.session_state["auth"] = False
    if "token_actual" not in st.session_state: st.session_state["token_actual"] = ""
    if "vidas" not in st.session_state: st.session_state["vidas"] = 3
    if "errores_quiz" not in st.session_state: st.session_state["errores_quiz"] = 0
    if "advertencia_ph" not in st.session_state: st.session_state["advertencia_ph"] = False
    if "puntos_acumulados" not in st.session_state: st.session_state["puntos_acumulados"] = 0
    if "racha_consecutiva" not in st.session_state: st.session_state["racha_consecutiva"] = 0
    if "licencia_extendida" not in st.session_state: st.session_state["licencia_extendida"] = False
    if "memo_tablero" not in st.session_state: st.session_state["memo_tablero"] = mezclar_memorama()
    if "memo_reveladas" not in st.session_state: st.session_state["memo_reveladas"] = []
    if "memo_resueltas" not in st.session_state: st.session_state["memo_resueltas"] = []
    if "memo_completado" not in st.session_state: st.session_state["memo_completado"] = False

def main():
    inyectar_css()
    inicializar_db()
    inicializar_estado()

    if not st.session_state["auth"]:
        st.markdown("<h1 class='main-title'>Chonps<span class='main-title-suffix'>Lab</span> Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-title'>Plataforma de Simulación Bioquímica - Nodo Synapsis</p>", unsafe_allow_html=True)
        st.markdown("<div class='bio-panel'><span style='color:#00e5ff; font-weight:700; font-size:1.25rem;'>Acceso Restringido</span><p style='color:#cfd8dc; margin-top:10px;'>Ingresa tu token de suscripción activo para desplegar el entorno de simulación.</p></div>", unsafe_allow_html=True)
        
        pwd = st.text_input("Token de Licencia:", type="password")
        if st.button("Autenticar Terminal", use_container_width=True):
            token_limpio = pwd.strip().upper()
            es_valido, mensaje = validar_y_bloquear_token(token_limpio)
            if es_valido:
                st.session_state["auth"] = True
                st.session_state["token_actual"] = token_limpio
                pts, comp = obtener_datos_usuario(token_limpio)
                st.session_state["puntos_acumulados"] = pts
                if comp == 1:
                    st.session_state["memo_completado"] = True
                    st.session_state["memo_resueltas"] = [1, 2, 3, 4, 5]
                st.rerun()
            else:
                st.error(f"Error: {mensaje}")
        
        with st.expander("⚙️ Panel de Administración (Gestor de Licencias y Tokens)"):
            c_admin1, c_admin2 = st.columns(2)
            with c_admin1:
                nuevo_token = st.text_input("Nuevo Token:").strip().upper()
                dias = st.number_input("Días de vigencia:", min_value=1, value=30)
                if st.button("Crear Suscripción", type="primary", use_container_width=True):
                    if nuevo_token: st.info(registrar_nuevo_usuario(nuevo_token, dias))
            with c_admin2:
                token_bloqueado = st.text_input("Token Objetivo:").strip().upper()
                c_b1, c_b2, c_b3 = st.columns(3)
                with c_b1:
                    if st.button("🔓 Desbloquear"): liberar_token(token_bloqueado); st.success("Liberado.")
                with c_b2:
                    if st.button("❌ Cancelar"): forzar_cancelacion_licencia(token_bloqueado); liberar_token(token_bloqueado); st.error("Cancelado.")
                with c_b3:
                    if st.button("🗑️ Eliminar"): eliminar_registro_token(token_bloqueado); st.error("Borrado.")
    else:
        with st.sidebar:
            st.markdown(f"**Usuario:** `{st.session_state['token_actual']}`")
            st.markdown(f"**Marcador:** `🪙 {st.session_state['puntos_acumulados']} PTS`")
            if st.button("🚪 Cerrar Sesión Segura", use_container_width=True):
                liberar_token(st.session_state["token_actual"])
                st.session_state["auth"] = False
                st.rerun()

        _, c_vid = st.columns([3, 1])
        with c_vid:
            st.markdown(f"<div class='monitor-box'><span style='color:#90a4ae; font-size:12px;'>ESTABILIDAD CELULAR</span><br><b style='font-size:20px; color:#f44336;'>{st.session_state.vidas} / 3 💔</b></div>", unsafe_allow_html=True)

        if st.session_state.vidas <= 0:
            st.error("🚨 COLAPSO METABÓLICO: Lisis celular detectada por acumulación de fallos.")
            if st.button("Reiniciar Simulador"):
                st.session_state.vidas = 3
                st.rerun()
            return

        tabs = st.tabs(["🏛️ Módulo 1", "⚡ Módulo 2", "🧬 Módulo 3", "🌡️ Módulo 4", "🏆 Evaluación"])

        with tabs[0]:
            mostrar_modulo1()
            
        with tabs[1]:
            mostrar_modulo2()
            
        with tabs[2]:
            mostrar_modulo3_temporal()
            
        with tabs[3]:
            mostrar_modulo4_temporal()
            
        with tabs[4]:
            mostrar_evaluacion_temporal()

if __name__ == "__main__":
    main()
