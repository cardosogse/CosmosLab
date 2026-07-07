import streamlit as st
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
