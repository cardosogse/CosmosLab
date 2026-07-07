import streamlit as st
from modulos.m1_dia1 import mostrar_dia1
from modulos.m1_dia2 import mostrar_dia2
from modulos.m1_dia3 import mostrar_dia3
from modulos.m1_dia4 import mostrar_dia4

def mostrar_modulo1():
    st.header("🏛️ Módulo 1: Fundamentos de Química Biológica")
    
    # Cuadro de mandos global
    col_pts, col_vds, col_blank = st.columns([1.5, 1.5, 5])
    with col_pts:
        st.markdown(f"<div class='metric-card'><b>Marcador Total:</b><br>🪙 {st.session_state.get('puntos', 0)} PTS</div>", unsafe_allow_html=True)
    with col_vds:
        st.markdown(f"<div class='metric-card' style='border-left-color: #ff1744;'><b>Estabilidad Celular:</b><br>💔 {st.session_state.get('vidas', 3)}/3 Vidas</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🗺️ Bitácora de Viaje")
    
    # Menú de navegación por días
    dia_seleccionado = st.radio(
        "Estaciones de trabajo disponibles para tu token:",
        options=["📊 Día 1: Materia", "⚛️ Día 2: Átomos y Tabla", "🧬 Día 3: Fusión y Enlaces", "🧪 Día 4: pH y Homeostasis"],
        horizontal=True
    )
    st.markdown("---")
    
    dia_progreso = st.session_state.get('dia_completado', 0)
    
    if "Día 1" in dia_seleccionado:
        mostrar_dia1()
        
    elif "Día 2" in dia_seleccionado:
        if dia_progreso >= 1:
            mostrar_dia2()
        else:
            st.warning("🔒 Acceso Restringido: Debes resolver y aprobar el Reto del Día 1 para liberar esta estación.")
            
    elif "Día 3" in dia_seleccionado:
        if dia_progreso >= 2:
            mostrar_dia3()
        else:
            st.warning("🔒 Acceso Restringido: Requiere la aprobación del mapa de electronegatividad del Día 2.")
            
    elif "Día 4" in dia_seleccionado:
        if dia_progreso >= 3:
            mostrar_dia4()
        else:
            st.warning("🔒 Acceso Restringido: Supera el Reactor de Fusión Atómica del Día 3 para abrir la cámara de perfusión.")
