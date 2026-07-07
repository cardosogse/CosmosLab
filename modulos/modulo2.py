import streamlit as st
import math
from assets import ELEMENTOS, generar_svg_tira_afloja
from database import actualizar_modulo_db

def mostrar_modulo2():
    actualizar_modulo_db(st.session_state["token_actual"], 2)
    st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>Módulo 2: Electronegatividad (El Estira y Afloja Celular)</h2>", unsafe_allow_html=True)
    
    estacion_m2 = st.radio("Navegación Sub-Módulo 2:", options=["⚡ Estación A: Escala de Pauling Interactiva", "🧫 Estación B: Fisiología de Membrana (Ecuación de Nernst)"], horizontal=True, label_visibility="collapsed")
    st.markdown("---")

    if "Estación A" in estacion_m2:
        st.markdown("### El Gradiente de Afinidad Electrónica en Bioelementos")
        col_sel1, col_sel2 = st.columns(2)
        e1_name = col_sel1.selectbox("Elemento Primario:", list(ELEMENTOS.keys()), index=1)
        e2_name = col_sel2.selectbox("Elemento Secundario:", list(ELEMENTOS.keys()), index=2)
        
        el1, el2 = ELEMENTOS[e1_name], ELEMENTOS[e2_name]
        diff_m2 = abs(el1['fuerza'] - el2['fuerza'])
        
        st.components.v1.html(generar_svg_tira_afloja(el1['fuerza'], el1['color'], el1['sym'], el2['fuerza'], el2['color'], el2['sym']), height=130, scrolling=False)
        
        if diff_m2 == 0: st.markdown(f"<div class='card-success'><b>🤝 Enlace Covalente No Polar Puro (Diferencia de Electronegatividad = 0.0)</b></div>", unsafe_allow_html=True)
        elif diff_m2 <= 0.4: st.markdown(f"<div class='card-success'><b>🤝 Enlace Covalente No Polar (Diferencia de Electronegatividad = {diff_m2:.2f})</b></div>", unsafe_allow_html=True)
        elif diff_m2 <= 1.7: st.markdown(f"<div class='card-hint'><b>⚡ Enlace Covalente Polar (Diferencia de Electronegatividad = {diff_m2:.2f})</b></div>", unsafe_allow_html=True)
        else: st.markdown(f"<div class='card-error'><b>⚠️ Carácter Altamente Iónico / Tensión (Diferencia de Electronegatividad = {diff_m2:.2f})</b></div>", unsafe_allow_html=True)

    elif "Estación B" in estacion_m2:
        st.markdown("### Laboratorio Biofísico: Equilibrio de Nernst en Células Veterinarias")
        ion_sel = st.selectbox("Ion Bajo Estudio:", ["Potasio (K+)", "Sodio (Na+)"])
        c1_n, c2_n = st.columns(2)
        if ion_sel == "Potasio (K+)":
            c_ext = c1_n.slider("Concentración Extracelular [K+]_out (mM):", 1.0, 15.0, 4.5, 0.5)
            c_int = c2_n.slider("Concentración Intracelular [K+]_in (mM):", 100.0, 160.0, 140.0, 1.0)
        else:
            c_ext = c1_n.slider("Concentración Extracelular [Na+]_out (mM):", 100.0, 160.0, 145.0, 1.0)
            c_int = c2_n.slider("Concentración Intracelular [Na+]_in (mM):", 5.0, 30.0, 12.0, 0.5)
        
        potencial_equilibrio = 61.5 * math.log10(c_ext / c_int)
        st.markdown(f"<div class='monitor-box' style='border:1px solid #00e5ff;'><span style='color:#00e5ff; font-size:13px;'>POTENCIAL DE EQUILIBRIO CALCULADO</span><br><b style='font-size:24px; color:#ffffff;'>{potencial_equilibrio:.2f} mV</b></div>", unsafe_allow_html=True)

