import streamlit as st
import time
from database import sincronizar_progreso_db, otorgar_tiempo_extra_db
from assets import obtener_svg_atomo, mezclar_memorama

def mostrar_dia1():
    st.subheader("Día 1: Niveles de Organización y Separación de Fases")
    st.write("La bioquímica es una **ciencia aplicada**; los procesos e interacciones generados *in vitro* (tubo de ensayo) constituyen las bases del diagnóstico clínico y el desarrollo farmacéutico moderno.")
    
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
    st.markdown("""<span class='foco-parpadeante'>💡</span> <i>Deslice la línea del tiempo horizontal (barra azul cian) para descubrir la evolución del átomo.</i>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    modelo = st.select_slider(
        "Navegación Cronológica:",
        options=["Dalton (1810)", "Thomson (1897)", "Rutherford (1911)", "Bohr (1913)", "Schrödinger (1926)"],
        label_visibility="collapsed"
    )
    
    col_txt, col_svg = st.columns([3, 1])
    with col_txt:
        if "Dalton" in modelo: 
            st.markdown("<div class='card-dalton'><b>Dalton (1810):</b> Esfera sólida sin cargas. Explica las proporciones estequiométricas en las reacciones químicas elementales.</div>", unsafe_allow_html=True)
        elif "Thomson" in modelo: 
            st.markdown("<div class='card-thomson'><b>Thomson (1897):</b> Descubre el electrón. Introduce por primera vez la naturaleza eléctrica de la materia.</div>", unsafe_allow_html=True)
        elif "Rutherford" in modelo: 
            st.markdown("<div class='card-rutherford'><b>Rutherford (1911):</b> Demuestra que el átomo concentra su masa positiva en un núcleo central diminuto.</div>", unsafe_allow_html=True)
        elif "Bohr" in modelo: 
            st.markdown("<div class='card-bohr'><b>Bohr (1913):</b> Órbitas circulares planas fijas con niveles de energía cuantizados.</div>", unsafe_allow_html=True)
        else: 
            st.markdown("<div class='card-schrodinger'><b>Schrödinger (1926):</b> Orbitales de densidad probabilística 3D. *Lehninger* demuestra que dictan las geometrías de las biomoléculas.</div>", unsafe_allow_html=True)
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
                st.button(f"✅ {val_tarjeta}", key=f"btn_m1_d1_res_{i}", disabled=True, use_container_width=True)
            elif i in st.session_state["memo_reveladas"]:
                st.button(f"👀 {val_tarjeta}", key=f"btn_m1_d1_rev_{i}", disabled=True, use_container_width=True)
            else:
                if st.button("⚛️ Revelar", key=f"btn_m1_d1_act_{i}", use_container_width=True):
                    st.session_state["memo_reveladas"].append(i)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    c_reset, _ = st.columns([1, 3])
    with c_reset:
        if st.button("🔄 Reiniciar Memorama", use_container_width=True):
            st.session_state["memo_tablero"] = mezclar_memorama()
            st.session_state["memo_reveladas"] = []
            st.session_state["memo_resueltas"] = []
            if not st.session_state["memo_completado"]:
                st.session_state["racha_consecutiva"] = 0
            st.rerun()

    if st.session_state["memo_completado"]:
        st.markdown(f"<div class='card-success'>🏆 <b>¡Afinidad Atómica Consolidada!</b> Avance sellado permanentemente en la DB. Marcador: <b>{st.session_state['puntos_acumulados']} PTS</b>.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)import streamlit as st
import time
from database import sincronizar_progreso_db, otorgar_tiempo_extra_db
from assets import obtener_svg_atomo, mezclar_memorama

def mostrar_dia1():
    st.subheader("Día 1: Niveles de Organización y Separación de Fases")
    st.write("La bioquímica es una **ciencia aplicada**; los procesos e interacciones generados *in vitro* (tubo de ensayo) constituyen las bases del diagnóstico clínico y el desarrollo farmacéutico moderno.")
    
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
    st.markdown("""<span class='foco-parpadeante'>💡</span> <i>Deslice la línea del tiempo horizontal (barra azul cian) para descubrir la evolución del átomo.</i>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    modelo = st.select_slider(
        "Navegación Cronológica:",
        options=["Dalton (1810)", "Thomson (1897)", "Rutherford (1911)", "Bohr (1913)", "Schrödinger (1926)"],
        label_visibility="collapsed"
    )
    
    col_txt, col_svg = st.columns([3, 1])
    with col_txt:
        if "Dalton" in modelo: 
            st.markdown("<div class='card-dalton'><b>Dalton (1810):</b> Esfera sólida sin cargas. Explica las proporciones estequiométricas en las reacciones químicas elementales.</div>", unsafe_allow_html=True)
        elif "Thomson" in modelo: 
            st.markdown("<div class='card-thomson'><b>Thomson (1897):</b> Descubre el electrón. Introduce por primera vez la naturaleza eléctrica de la materia.</div>", unsafe_allow_html=True)
        elif "Rutherford" in modelo: 
            st.markdown("<div class='card-rutherford'><b>Rutherford (1911):</b> Demuestra que el átomo concentra su masa positiva en un núcleo central diminuto.</div>", unsafe_allow_html=True)
        elif "Bohr" in modelo: 
            st.markdown("<div class='card-bohr'><b>Bohr (1913):</b> Órbitas circulares planas fijas con niveles de energía cuantizados.</div>", unsafe_allow_html=True)
        else: 
            st.markdown("<div class='card-schrodinger'><b>Schrödinger (1926):</b> Orbitales de densidad probabilística 3D. *Lehninger* demuestra que dictan las geometrías de las biomoléculas.</div>", unsafe_allow_html=True)
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
            st.toast("❌ No interactúan.", icon="⚠️import streamlit as st
from database import descontar_vida_db, sincronizar_progreso_db

def mostrar_dia4():
    st.subheader("Día 4: Equilibrio Ácido-Base y Sistemas Amortiguadores Celulares")
    st.write("Evalúa los mecanismos biológicos del organismo para neutralizar los cambios críticos de pH producidos por desequilibrios metabólicos severos.")
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### Estructura de los Grupos Funcionales Secundarios")
    grupo = st.selectbox("Grupo Funcional a Inspeccionar:", ["Carbonilo (C=O)", "Metilo (CH3)", "Hidroxilo (-OH)", "Tiol / Disulfuro (-SH)", "Fosforilo (-PO3)"])
    if "Carbonilo" in grupo:
        st.warning("**Carbonilo:** Propio de aldehídos/cetonas. Centro neurálgico del metabolismo de glúcidos.")
    elif "Metilo" in grupo:
        st.warning("**Metilo:** Hidrofóbico, crítico en empaquetamiento estructural y marcas epigenéticas de metilación en el ADN.")
    elif "Tiol" in grupo:
        st.warning("**Tiol/Disulfuro:** Puentes covalentes cruzados de cisteína. Brindan rigidez mecánica a pezuñas y cuernos por la queratina.")
    else:
        st.warning("Grupo funcional característico de biomoléculas celulares.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🌡️ Cámara de Perfusión y Desnaturalización Proteica")
    st.write("Selecciona una cámara de experimentación celular y sométela a una agresión química inyectando un ácido fuerte:")
    
    solucion = st.radio("Cámara de Perfusión Sanguínea:", ["Plasma con Amortiguador Bicarbonato (pH 7.4)", "Agua Destilada Pura (pH 7.0)"])
    
    if st.button("Inyectar 10 mL de HCl", use_container_width=True):
        token = st.session_state['token_actual']
        if "Agua" in solucion:
            if not st.session_state.advertencia_ph:
                st.markdown("<div class='card-hint'>💡 <b>ALERTA DE SEGURIDAD:</b> El agua carece de sistemas amortiguadores. Presiona una vez más si deseas inyectar y desnaturalizar las proteínas de la muestra.</div>", unsafe_allow_html=True)
                st.session_state.advertencia_ph = True
            else:
                st.markdown("<div class='card-error'>🚨 <b>CHOQUE DE ACIDOSIS:</b> pH cayó a 2.0. Proteínas desnaturalizadas. <b>-1 Vida en la BD.</b></div>", unsafe_allow_html=True)
                descontar_vida_db(token)
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.session_state.advertencia_ph = False
                st.rerun()
        else:
            st.markdown("<div class='card-success'>🛡️ <b>TAMPÓN EXITOSO:</b> El bicarbonato absorbió los protones (H+), derivándolos a ácido carbónico disociable en CO2 exhalable vía pulmonar.</div>", unsafe_allow_html=True)
            st.session_state.advertance_ph = False
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🚑 Cuestionario de Certificación Fisiológica")
    Q1 = st.radio("1. ¿Por qué la evolución orgánica seleccionó la D-Glucosa sobre la L-Glucosa?", ["A) Desvía la luz a la derecha.", "B) Modelo estereoquímico llave-cerradura en los sitios activos enzimáticos."], index=None)
    Q2 = st.radio("2. Glucosa y Galactosa difieren únicamente en la orientación espacial del carbono asimétrico 4 (C-4), son:", ["A) Isótopos", "B) Epímeros"], index=None)
    
    if st.button("Firmar y Evaluar Módulo", use_container_width=True):
        token = st.session_state['token_actual']
        errores = 0
        if Q1 and "B)" not in Q1: errores += 1
        if Q2 and "B)" not in Q2: errores += 1
        
        if not Q1 or not Q2: 
            st.warning("Examen incompleto.")
        elif errores == 0:
            st.balloons()
            st.success("🏆 ¡Felicidades! Récord perfecto. Progreso bloqueado anti-F5 en SQLite.")
            sincronizar_progreso_db(token, st.session_state["puntos_acumulados"] + 200, 2)
            st.session_state["puntos_acumulados"] += 200
            st.rerun()
        else:
            st.session_state.errores_quiz += 1
            if st.session_state.errores_quiz == 1:
                st.markdown(f"<div class='card-hint'>💡 Tienes {errores} error(es). Recuerda que la variación en un único centro quiral define un epímero. Corrige sin penalización.</div>", unsafe_allow_html=True)
            else:
                descontar_vida_db(token)
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.error("❌ Fallo Clínico. Se ha descontado 1 Vida.")
                st.session_state.errores_quiz = 0
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)import streamlit as st
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
