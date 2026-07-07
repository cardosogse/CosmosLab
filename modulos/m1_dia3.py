import streamlit as st

def mostrar_dia3():
    st.subheader("Día 3: El Reactor de Fusión Atómica e Interacciones Moleculares")
    st.write("Estudia cómo la disparidad en la tracción de electrones determina la estabilidad de las uniones y la solvatación biológica celular.")
    
    escala_pauling = {"Oxígeno (O)": 3.44, "Hidrógeno (H)": 2.20, "Carbono (C)": 2.55, "Sodio (Na)": 0.93, "Cloro (Cl)": 3.16, "Cobre (Cu)": 1.90}
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🧬 Reactor de Fusión de Enlaces")
    
    col1, col2 = st.columns(2)
    with col1:
        atomo_a = st.selectbox("Selecciona el Átomo A:", list(escala_pauling.keys()), key="at_a")
        atomo_b = st.selectbox("Selecciona el Átomo B:", list(escala_pauling.keys()), key="at_b")
        fusionar = st.button("Colisionar Capas de Valencia")
        
    with col2:
        if fusionar:
            if atomo_a == "Cobre (Cu)" and atomo_b == "Cobre (Cu)":
                st.success("🪙 Enlace Detectado: Metálico (Mar de Electrones)")
                st.write("**Fundamento Físico:** Los electrones se deslocalizan por completo formando una matriz móvil. Explica la conductividad eléctrica y térmica esencial en sensores médicos de laboratorio.")
            else:
                diff = abs(escala_pauling[atomo_a] - scala_pauling[atomo_b])
                st.metric("Diferencia de Electronegatividad (Δχ)", f"{diff:.2f}")
                
                if diff < 0.4:
                    st.success("🔬 Tipo: Enlace Covalente No Polar (Apolar)")
                    st.info("Compartición simétrica. *Lehninger* fundamenta que este equilibrio molecular da origen al comportamiento hidrofóbico de los lípidos, forzando la organización de las membranas celulares.")
                elif 0.4 <= diff <= 1.7:
                    st.warning("🌊 Tipo: Enlace Covalente Polar")
                    st.info("Tirón asimétrico de cargas creando un dipolo permanente. Citando al texto *Harper*, esta polaridad le confiere una **elevada constante dieléctrica al agua (78.5)**, rompiendo redes cristalinas de sales (Solvatación biológica).")
                else:
                    st.error("⚡ Tipo: Enlace Iónico (Salino)")
                    st.info("Transferencia neta de electrones. Genera uniones salinas de atracción electrostática pura que, bajo el libro *Laguna*, se disocian de inmediato en el citoplasma celular libre.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🧮 Laboratorio Métrico: Calculadora de Molaridad")
    
    c1, c2 = st.columns(2)
    with c1:
        masa = st.slider("Masa del Soluto (Gramos de NaCl):", min_value=1.0, max_value=100.0, value=5.8)
        volumen = st.slider("Volumen de la Disolución (Litros de Agua):", min_value=0.1, max_value=5.0, value=1.0)
    
    peso_molecular_nacl = 58.44
    moles = masa / peso_molecular_nacl
    molaridad = moles / volumen
    
    with c2:
        st.markdown("#### Parámetros de Concentración")
        st.write(f"**Masa Molecular NaCl fijo:** {peso_molecular_nacl} g/mol")
        st.write(f"**Moles calculados:** {moles:.4f} mol")
        st.metric("Molaridad Resultante (M):", f"{molaridad:.3f} mol/L")
    st.markdown("</div>", unsafe_allow_html=True)
