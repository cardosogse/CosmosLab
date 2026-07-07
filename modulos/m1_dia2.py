import streamlit as st

def mostrar_dia2():
    st.subheader("Día 2: El Micro-Constructor Atómico y Propiedades Periódicas")
    st.write("Manipula los componentes fundamentales del átomo para estudiar cómo su balance de carga rige la logística celular.")
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Configuración de Partículas Subatómicas")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        protones = st.slider("Protones (Número Atómico Z):", min_value=1, max_value=20, value=1)
        neutrones = st.slider("Neutrones (Masa Nuclear N):", min_value=1, max_value=20, value=1)
        electrones = st.slider("Electrones (Capa de Valencia):", min_value=1, max_value=20, value=1)
        
    masa_atómica = protones + neutrones
    carga_neta = protones - electrones
    
    if carga_neta == 0:
        estado_quimico = "Átomo Neutro"
        color_alerta = "inverse"
    elif carga_neta > 0:
        estado_quimico = f"Catión (Ion Positivo +{carga_neta})"
        color_alerta = "success"
    else:
        estado_quimico = f"Anión (Ion Negativo {carga_neta})"
        color_alerta = "error"
        
    with col2:
        st.markdown("#### Matriz Atómica")
        st.metric("Identidad (Z)", f"Protones: {protones}")
        st.metric("Masa Total (A)", f"{masa_atómica} u")
        if color_alerta == "success": st.success(estado_quimico)
        elif color_alerta == "error": st.error(estado_quimico)
        else: st.info(estado_quimico)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🗺️ Silueta Periódica Dinámica y Tendencias Espaciales")
    st.write("Observa cómo la ubicación del elemento determina su avidez electrónica (Electronegatividad de Pauling):")
    
    base_elementos = {
        1: {"simbolo": "H", "nombre": "Hidrógeno", "electroneg": "2.20", "rol": "Determinante directo del pH e interacciones por puentes de hidrógeno."},
        6: {"simbolo": "C", "nombre": "Carbono", "electroneg": "2.55", "rol": "Esqueleto tetraédrico de todas las biomoléculas orgánicas."},
        7: {"simbolo": "N", "nombre": "Nitrógeno", "electroneg": "3.04", "rol": "Componente estructural de grupos a-amino y bases nitrogenadas."},
        8: {"simbolo": "O", "nombre": "Oxígeno", "electroneg": "3.44", "rol": "Aceptor final de electrones en la respiración mitocondrial celular."},
        11: {"simbolo": "Na", "nombre": "Sodio", "electroneg": "0.93", "rol": "Catión extracelular primario. Regula la presión osmótica plasmática."},
        12: {"simbolo": "Mg", "nombre": "Magnesio", "electroneg": "1.31", "rol": "Cofactor indispensable según *Lehninger* para estabilizar las cargas del ATP."},
        17: {"simbolo": "Cl", "nombre": "Cloro", "electroneg": "3.16", "rol": "Anión extracelular principal encargado de mantener la neutralidad eléctrica plasmática."}
    }
    
    if protones in base_elementos:
        el = base_elementos[protones]
        st.subheader(f"📍 Elemento Detectado: {el['nombre']} ({el['simbolo']})")
        
        col_tabla, col_flechas = st.columns([2, 1])
        with col_tabla:
            st.markdown(f"""
            <div style="display: flex; gap: 10px; align-items: center; background-color: #0f172a; padding: 20px; border-radius: 8px; border: 1px solid #334155;">
                <div style="background-color: #00e5ff; color: #0f172a; font-size: 2.5rem; font-weight: 900; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; border-radius: 8px;">
                    {el['simbolo']}
                </div>
                <div>
                    <b>Electronegatividad de Pauling:</b> {el['electroneg']}<br>
                    <b>Rol Biológico:</b> {el['rol']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_flechas:
            st.markdown("""
            <div style="text-align: center; color: #00e5ff; font-weight: bold;">
                ▲ Vertical (Sube en Grupos)<br>
                ► Horizontal (Aumenta en Periodos)<br>
                <svg width="120" height="60" viewBox="0 0 120 60">
                    <line x1="10" y1="50" x2="110" y2="50" stroke="#00e5ff" stroke-width="4" marker-end="url(#arrow)" />
                    <line x1="10" y1="50" x2="10" y2="10" stroke="#00e5ff" stroke-width="4" />
                    <defs>
                        <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                            <path d="M 0 0 L 10 5 L 0 10 z" fill="#00e5ff"/>
                        </marker>
                    </defs>
                </svg>
                <br><span style="color:#64748b; font-size:0.8rem;">A mayor cercanía al núcleo celular, mayor tracción electrónica.</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Mueve las barras subatómicas superiores. Si construyes H, C, N, O, Na, Mg o Cl, se iluminará su casilla espacial en la tabla periódica.")
    st.markdown("</div>", unsafe_allow_html=True)
