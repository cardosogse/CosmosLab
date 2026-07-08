import streamlit as st
import time
from database import sincronizar_progreso_db, otorgar_tiempo_extra_db
from assets import obtener_svg_atomo, mezclar_memorama

def mostrar_dia1():
    st.subheader("Día 1: Niveles de Organización y Separación de Fases")
    st.write("Las interacciones macromoleculares generadas *in vitro* constituyen las bases del diagnóstico clínico veterinario.")
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🔬 Simulador de Centrifugación Macromolecular")
    muestra = st.selectbox("Selecciona la Muestra de Fluido:", ["Plasma Sanguíneo", "Sangre Entera (Muestra anticoagulada)"])
    
    if st.button("Ejecutar Fuerzas G (Centrifugar)"):
        progreso = st.progress(0)
        for i in range(100):
            time.sleep(0.005)
            progreso.progress(i + 1)
            
        if muestra == "Plasma Sanguíneo":
            st.success("🔬 Diagnóstico: Mezcla Homogénea (Solución Coloidal)")
            st.info("Bajo el rigor de *Harper*, el plasma mantiene una fase uniforme debido a que las proteínas (albúmina/globulinas) permanecen dispersas sin precipitar por fuerzas estándar.")
        else:
            st.warning("🩸 Diagnóstico: Mezcla Heterogénea en Suspensión")
            st.info("La fuerza centrífuga vence el flujo uniforme precipitando los elementos celulares densos (eritrocitos) al fondo, dejando el plasma libre en la superficie.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🎛️ Deslizador de Teorías Cuánticas y Modelos Atómicos")
    modelo = st.select_slider("Línea de Evolución Atómica:", options=["Dalton (1810)", "Thomson (1897)", "Rutherford (1911)", "Bohr (1913)", "Schrödinger (1926)"])
    
    col_txt, col_svg = st.columns([3, 1])
    with col_txt:
        if "Dalton" in modelo: st.markdown("<div class='card-dalton'><b>Dalton:</b> Esfera sólida sin cargas. Explica las proporciones estequiométricas.</div>", unsafe_allow_html=True)
        elif "Thomson" in modelo: st.markdown("<div class='card-thomson'><b>Thomson:</b> Descubre el electrón. Introduce la naturaleza eléctrica.</div>", unsafe_allow_html=True)
        elif "Rutherford" in modelo: st.markdown("<div class='card-rutherford'><b>Rutherford:</b> Núcleo denso positivo y espacio periférico vacío.</div>", unsafe_allow_html=True)
        elif "Bohr" in modelo: st.markdown("<div class='card-bohr'><b>Bohr:</b> Órbitas circulares planas fijas con niveles de energía cuantizados.</div>", unsafe_allow_html=True)
        else: st.markdown("<div class='card-schrodinger'><b>Schrödinger:</b> Orbitales de densidad probabilística 3D. *Lehninger* demuestra que dictan las geometrías de las biomoléculas.</div>", unsafe_allow_html=True)
    with col_svg:
        st.components.v1.html(f"<div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px; background-color:rgba(255,255,255,0.02); border-radius:8px;'>{obtener_svg_atomo(modelo)}</div>", height=120, scrolling=False)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🧠 Desafío de Consolidación: Memorama Atómico")
    
    if len(st.session_state["memo_reveladas"]) == 2:
        idx1, idx2 = st.session_state["memo_reveladas"]
        val1, id_par1 = st.session_state["memo_tablero"][idx1]
        val2, id_par2 = st.session_state["memo_tablero"][idx2]
        
        if id_par1 == id_par2:
            if id_par1 not in st.session_state["memo_resueltas"]:
                st.session_state["memo_resueltas"].append(id_par1)
                if not st.session_state["memo_completado"]:
                    st.session_state["racha_consecutiva"] += 1
                    puntos_ganados = 100
                    if st.session_state["racha_consecutiva"] >= 2 and not st.session_state["licencia_extendida"]:
                        puntos_ganados += 300
                        st.session_state["licencia_extendida"] = True
                        otorgar_tiempo_extra_db(st.session_state["token_actual"], dias=7)
                        st.toast("🚀 ¡RACHA CUÁNTICA! +7 días de licencia extra.", icon="🎁")
                    st.session_state["puntos_acumulados"] += puntos_ganados
                    sincronizar_progreso_db(st.session_state["token_actual"], st.session_state["puntos_acumulados"], 1)
            st.toast("⚡ ¡Afinidad molecular correcta!", icon="✅")
        else:
            st.session_state["racha_consecutiva"] = 0
            st.toast("❌ No interactúan.", icon="⚠️")
        st.session_state["memo_reveladas"] = []

    if len(st.session_state["memo_resueltas"]) == 5 and not st.session_state["memo_completado"]:
        st.session_state["memo_completado"] = True
        sincronizar_progreso_db(st.session_state["token_actual"], st.session_state["puntos_acumulados"], 1)

    cols_memo = st.columns(5)
    for i in range(10):
        col_idx = i % 5
        with cols_memo[col_idx]:
            val_tarjeta, id_par = st.session_state["memo_tablero"][i]
            if id_par in st.session_state["memo_resueltas"]:
                st.button(f"✅ {val_tarjeta}", key=f"b_memo_{i}", disabled=True, use_container_width=True)
            elif i in st.session_state["memo_reveladas"]:
                st.button(f"👀 {val_tarjeta}", key=f"b_memo_{i}", disabled=True, use_container_width=True)
            else:
                if st.button("⚛️ Revelar", key=f"b_memo_{i}", use_container_width=True):
                    st.session_state["memo_reveladas"].append(i)
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
