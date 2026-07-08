import streamlit as st
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
            if not st.session_state["advertencia_ph"]:
                st.markdown("<div class='card-hint'>💡 <b>ALERTA DE SEGURIDAD:</b> El agua carece de sistemas amortiguadores. Presiona una vez más si deseas inyectar y desnaturalizar las proteínas de la muestra.</div>", unsafe_allow_html=True)
                st.session_state["advertencia_ph"] = True
            else:
                st.markdown("<div class='card-error'>🚨 <b>CHOQUE DE ACIDOSIS:</b> pH cayó a 2.0. Proteínas desnaturalizadas. <b>-1 Vida en la BD.</b></div>", unsafe_allow_html=True)
                descontar_vida_db(token)
                st.session_state["vidas"] = max(0, st.session_state["vidas"] - 1)
                st.session_state["advertencia_ph"] = False
                st.rerun()
        else:
            st.markdown("<div class='card-success'>🛡️ <b>TAMPÓN EXITOSO:</b> El bicarbonato absorbió los protones (H+), derivándolos a ácido carbónico disociable en CO2 exhalable vía pulmonar.</div>", unsafe_allow_html=True)
            st.session_state["advertencia_ph"] = False
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### ### 🚑 Cuestionario de Certificación Fisiológica")
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
            st.session_state["errores_quiz"] += 1
            if st.session_state["errores_quiz"] == 1:
                st.markdown(f"<div class='card-hint'>💡 Tienes {errores} error(es). Recuerda que la variación en un único centro quiral define un epímero. Corrige sin penalización.</div>", unsafe_allow_html=True)
            else:
                descontar_vida_db(token)
                st.session_state["vidas"] = max(0, st.session_state["vidas"] - 1)
                st.error("❌ Fallo Clínico. Se ha descontado 1 Vida.")
                st.session_state["errores_quiz"] = 0
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)import streamlit as st
from database import descontar_vida_db, sincronizar_progreso_db

def mostrar_dia4():
    st.subheader("Día 4: Equilibrio Ácido-Base y Sistemas Amortiguadores Celulares")
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🩸 Cámara de Perfusión: Monitoreo de Gases")
    solucion = st.radio("Medio Fisiológico:", ["Plasma con Amortiguador Bicarbonato (pH 7.4)", "Agua Destilada Pura (pH 7.0)"])
    
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
            st.session_state.advertencia_ph = False
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
        
        if not Q1 or not Q2: st.warning("Examen incompleto.")
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
from database import descontar_vida_db, restaurar_vida_db, sincronizar_progreso_db

def mostrar_dia4():
    st.subheader("Día 4: Equilibrio Ácido-Base y Sistemas Amortiguadores Celulares")
    st.write("Evalúa los mecanismos biológicos del organismo para neutralizar los cambios críticos de pH producidos por desequilibrios metabólicos severos.")
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🌡️ Cámara de Perfusión y Desnaturalización Proteica")
    st.write("Selecciona una cámara de experimentación celular y sométela a una agresión química inyectando un ácido fuerte:")
    
    sistema = st.radio("Cámara de Fluido Seleccionada:", ["Agua Destilada Pura", "Plasma Sanguíneo (Ecosistema Amortiguado)"])
    
    if st.button("Inyectar 10 mL de HCl (Ácido Clorhídrico)"):
        token = st.session_state['token_activo']
        
        if sistema == "Agua Destilada Pura":
            st.error("🚨 COLAPSO: El pH cayó drásticamente de 7.0 a 2.0")
            st.markdown("""
            **Fundamento de Fisiología (*Laguna*):** Al carecer de sistemas amortiguadores, el torrente libre de protones ($H^+$) destruyó los puentes de hidrógeno de las proteínas celulares, desnaturalizándolas de forma irreversible.
            """)
            descontar_vida_db(token)
            st.session_state['vidas'] = max(0, st.session_state['vidas'] - 1)
            st.rerun()
        else:
            st.success("🛡️ EFECTO TAMPÓN: El pH se estabilizó de manera exitosa en 7.4")
            st.markdown("""
            **Mecanismo Clínico (*Lehninger* + *Harper*):** Los iones bicarbonato ($\text{HCO}_3^-$) absorbieron el exceso de protones libres convirtiéndose en Ácido Carbónico ($\text{H}_2\text{CO}_3$). Al instante, la enzima *Anhidrasa Carbónica* lo deshidrató en agua y gas $\text{CO}_2$ exhalado por los pulmones (Efecto Bohr).
            """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🚑 Reto Clínico de Rescate de Estabilidad")
    st.write("Responde la pregunta basada en las patologías descritas en el *Harper* para restaurar tu salud o certificar el Módulo.")
    
    pregunta = "¿Qué respuesta compensatoria fisiológica despliega un animal para mitigar una acidosis láctica masiva producida por sobrecarga de granos o cetoacidosis metabólica?"
    opciones = [
        "Bradipnea (Disminución de la frecuencia respiratoria para retener CO2)",
        "Hiperventilación activa (Aumento del ritmo respiratorio para expulsar CO2 en forma de gas)",
        "Inactivación completa de la enzima anhidrasa carbónica renal"
    ]
    
    seleccion = st.radio(pregunta, opciones)
    
    if st.button("Validar Respuesta de Rescate"):
        token = st.session_state['token_activo']
        if seleccion == opciones[1]:
            st.success("¡Respuesta Correcta! El pulmón elimina el ácido volátil estabilizando el sistema biológico celular.")
            
            if st.session_state['vidas'] < 3:
                restaurar_vida_db(token)
                st.session_state['vidas'] = min(3, st.session_state['vidas'] + 1)
                st.toast("¡Estabilidad Celular restaurada (+1 Vida)! ❤️")
                
            if st.session_state.get('dia_completado', 0) < 4:
                sincronizar_progreso_db(token, 200, 4)
                st.session_state['puntos'] += 200
                st.session_state['dia_completado'] = 4
                st.balloons()
            st.rerun()
        else:
            st.error("Respuesta incorrecta. El desequilibrio metabólico de protones avanza sin control.")
            descontar_vida_db(token)
            st.session_state['vidas'] = max(0, st.session_state['vidas'] - 1)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
