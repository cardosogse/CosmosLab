import streamlit as st
from database import (inicializar_db, validar_y_bloquear_token, obtener_datos_usuario, 
                      liberar_token, registrar_nuevo_usuario, forzar_cancelacion_licencia, eliminar_registro_token)
from assets import inyectar_css
from modulos.modulo1 import mostrar_modulo1, mezclar_memorama
from modulos.modulo2 import mostrar_modulo2

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
        pwd = st.text_input("Token de Licencia:", type="password")
        if st.button("Autenticar Terminal", use_container_width=True):
            es_valido, mensaje = validar_y_bloquear_token(pwd.strip().upper())
            if es_valido:
                st.session_state["auth"] = True
                st.session_state["token_actual"] = pwd.strip().upper()
                pts, comp = obtener_datos_usuario(pwd.strip().upper())
                st.session_state["puntos_acumulados"] = pts
                if comp == 1:
                    st.session_state["memo_completado"] = True
                    st.session_state["memo_resueltas"] = [1, 2, 3, 4, 5]
                st.rerun()
            else:
                st.error(f"Error: {mensaje}")
    else:
        with st.sidebar:
            st.markdown(f"**Usuario:** `{st.session_state['token_actual']}`")
            st.markdown(f"**Puntos:** `🪙 {st.session_state['puntos_acumulados']}`")
            if st.button("🚪 Cerrar Sesión", use_container_width=True):
                liberar_token(st.session_state["token_actual"])
                st.session_state["auth"] = False
                st.rerun()

        st.markdown(f"<div class='monitor-box'><span style='color:#f44336; font-size:20px;'>VIDAS: {st.session_state.vidas} / 3 💔</span></div>", unsafe_allow_html=True)

        if st.session_state.vidas <= 0:
            st.error("🚨 COLAPSO METABÓLICO DETECTADO.")
            return

        tabs = st.tabs(["🏛️ Módulo 1", "⚡ Módulo 2", "🧬 Módulo 3", "🌡️ Módulo 4", "🏆 Evaluación"])

        with tabs[0]:
            mostrar_modulo1()

        with tabs[1]:
            mostrar_modulo2()

if __name__ == "__main__":
    main()

