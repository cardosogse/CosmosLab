import streamlit as st
import time
import random
from database import sincronizar_progreso_db

def mostrar_dia1():
    st.subheader("Día 1: Niveles de Organización y Separación de Fases")
    st.write("La bioquímica es una **ciencia aplicada**; los procesos e interacciones generados *in vitro* (tubo de ensayo) constituyen las bases del diagnóstico clínico y el desarrollo farmacéutico moderno.")
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🔬 Simulador de Centrifugación Macromolecular")
    st.write("Introduce una muestra de fluido biológico animal en el rotor de la centrifugadora:")
    
    muestra = st.selectbox("Selecciona la Muestra de Estudio:", ["Plasma Sanguíneo", "Sangre Entera (Muestra anticoagulada)"])
    
    if st.button("Ejecutar Fuerzas G (Centrifugar)"):
        progreso = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progreso.progress(i + 1)
            
        if muestra == "Plasma Sanguíneo":
            st.success("🔬 Diagnóstico: Mezcla Homogénea (Solución Coloidal)")
            st.info("Bajo el rigor de *Harper*, el plasma mantiene una única fase uniforme debido a que las proteínas plasmáticas solubles (albúmina/globulinas) y electrolitos permanecen dispersos molecularmente sin precipitar por la fuerza centrífuga estándar.")
        else:
            st.warning("🩸 Diagnóstico: Mezcla Heterogénea en Suspensión")
            st.info("La fuerza centrífuga ha vencido el flujo circulatorio uniforme y precipita los elementos celulares densos (eritrocitos y leucocitos) al fondo del tubo, dejando el plasma ámbar en la superficie superior de forma macroscópica.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🎛️ Deslizador de Teorías Cuánticas y Modelos Atómicos")
    modelo = st.select_slider(
        "Línea de Evolución Atómica:",
        options=["Dalton (1810)", "Thomson (1897)", "Rutherford (1911)", "Bohr (1913)", "Schrödinger (1926)"]
    )
    
    if modelo == "Dalton (1810)":
        st.info("**Esfera Sólida:** Considera el átomo como una unidad indivisible. Explica las leyes de las proporciones estequiométricas en las reacciones químicas elementales.")
    elif modelo == "Thomson (1897)":
        st.info("**Budín de Pasas:** Descubre la existencia del electrón. Introduce por primera vez la naturaleza eléctrica de la materia.")
    elif modelo == "Rutherford (1911)":
        st.info("**Modelo Nuclear:** Demuestra que el átomo concentra su masa positiva en un núcleo central diminuto, estando mayormente vacío.")
    elif modelo == "Bohr (1913)":
        st.info("**Órbitas Cuantizadas:** Introduce niveles fijos de energía. Explica cómo los electrones saltan de órbita emitiendo fotones sin colapsar.")
    elif modelo == "Schrödinger (1926)":
        st.info("**Modelo de Probabilidad 3D:** Describe orbitales moleculares gobernados por ecuaciones mecánicos-cuánticas. *Lehninger* demuestra que estas orientaciones espaciales dictan las geometrías tridimensionales exactas indispensables para los enlaces estables de las biomoléculas.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🎮 Reto Evaluatorio: Memorama Cuántico")
    st.write("Empareja de forma correcta los conceptos y autores para certificar tu bitácora.")
    
    conceptos_maestros = {
        "Schrödinger": "Geometrías 3D y Probabilidad",
        "Rutherford": "Descubrimiento del Núcleo Central",
        "Plasma": "Mezcla Homogénea Coloidal"
    }
    
    if 'memo_tarjetas' not in st.session_state:
        items = list(conceptos_maestros.keys()) + list(conceptos_maestros.values())
        random.seed(42)
        random.shuffle(items)
        st.session_state['memo_tarjetas'] = items
        st.session_state['memo_abiertas'] = []
        st.session_state['memo_resueltas'] = []
        
    tarjetas = st.session_state['memo_tarjetas']
    
    cols = st.columns(3)
    for index, elemento in enumerate(tarjetas):
        col_idx = index % 3
        with cols[col_idx]:
            if elemento in st.session_state['memo_resueltas']:
                st.button(f"✅ {elemento}", key=f"memo_{index}", disabled=True)
            elif index in st.session_state['memo_abiertas']:
                st.button(f"👁️ {elemento}", key=f"memo_{index}")
            else:
                if st.button("❓ Voltear", key=f"memo_{index}"):
                    if len(st.session_state['memo_abiertas']) < 2:
                        st.session_state['memo_abiertas'].append(index)
                        st.rerun()
                        
    if len(st.session_state['memo_abiertas']) == 2:
        idx1, idx2 = st.session_state['memo_abiertas']
        val1, val2 = tarjetas[idx1], tarjetas[idx2]
        
        es_par = False
        if val1 in conceptos_maestros and conceptos_maestros[val1] == val2: es_par = True
        if val2 in conceptos_maestros and conceptos_maestros[val2] == val1: es_par = True
        
        if es_par:
            st.session_state['memo_resueltas'].extend([val1, val2])
            st.toast("¡Par correcto encontrado! 🎉")
            st.session_state['memo_abiertas'] = []
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("No coinciden. Intenta de nuevo.")
            if st.button("Volver a ocultar tarjetas"):
                st.session_state['memo_abiertas'] = []
                st.rerun()

    if len(st.session_state['memo_resueltas']) == 6:
        st.success("🎯 ¡Felicidades! Has emparejado la totalidad de los conceptos cuánticos.")
        
        if st.session_state.get('dia_completado', 0) >= 1:
            st.info("Bitácora ya aprobada previamente. Acceso libre al Día 2 habilitado.")
        else:
            if st.button("Firmar Bitácora y Guardar en MainLab"):
                token = st.session_state['token_activo']
                sincronizar_progreso_db(token, 100, 1)
                st.session_state['puntos'] += 100
                st.session_state['dia_completado'] = 1
                st.balloons()
                st.success("Éxito. Progreso sincronizado. Estación del Día 2 desbloqueada.")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
