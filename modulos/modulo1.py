import streamlit as st
import random
from assets import obtener_svg_atomo
from database import sincronizar_progreso_db, otorgar_tiempo_extra_db

def mezclar_memorama():
    contenido = [
        ("Dalton (1810)", 1), ("Materia indivisible sin cargas", 1),
        ("Thomson (1897)", 2), ("Esfera positiva con electrones incrustados", 2),
        ("Rutherford (1911)", 3), ("Núcleo denso positivo y espacio vacío", 3),
        ("Bohr (1913)", 4), ("Órbitas circulares planas cuantizadas", 4),
        ("Schrödinger (1926)", 5), ("Orbitales 3D (Flexibilidad cuántica)", 5)
    ]
    random.shuffle(contenido)
    return contenido

def mostrar_modulo1():
    st.markdown("# Módulo 1: Fundamentos de Química Biológica")
    
    estacion_actual = st.radio(
        "Selecciona una Estación de Trabajo FMVZ M1:",
        options=[
            "⚛️ Estación A: Evolución, Estructura y Enlaces",
            "💧 Estación B: Fuerzas del Agua",
            "🧬 Estación C: Grupos Funcionales",
            "🩸 Estación D: pH y Buffers respiratorios"
        ],
        horizontal=True, label_visibility="collapsed"
    )
    st.markdown("---")

    if "Estación A" in estacion_actual:
        st.markdown("### Evolución de la Teoría Atómica, Estructura y Enlaces Químicos")
        st.markdown("<span class='foco-parpadeante'>💡</span> <i>Deslice la línea del tiempo horizontal (barra azul cian) para descubrir la evolución del átomo.</i><br>", unsafe_allow_html=True)
        
        modelo = st.select_slider("Navegación Cronológica:", options=["Dalton (1810)", "Thomson (1897)", "Rutherford (1911)", "Bohr (1913)", "Schrödinger (1926)"], label_visibility="collapsed")
        
        col_txt, col_svg = st.columns([3, 1])
        with col_txt:
            if "Dalton" in modelo:
                st.markdown("<div class='card-dalton'><b style='color:#90a4ae; font-size: 1.2rem;'>Modelo de Dalton (1810) — Átomo Indivisible</b><br><br>• <b>Principio:</b> Esfera sólida sin cargas.<br>• <b>Límite:</b> Incapaz de explicar uniones químicas al carecer de electrones.</div>", unsafe_allow_html=True)
            elif "Thomson" in modelo:
                st.markdown("<div class='card-thomson'><b style='color:#9c27b0; font-size: 1.2rem;'>Modelo de Thomson (1897) — El Electrón</b><br><br>• <b>Principio:</b> Descubre el electrón. Masa positiva con cargas negativas incrustadas.<br>• <b>Aporte:</b> Introduce la naturaleza eléctrica de la materia.</div>", unsafe_allow_html=True)
            elif "Rutherford" in modelo:
                st.markdown("<div class='card-rutherford'><b style='color:#2196f3; font-size: 1.2rem;'>Modelo de Rutherford (1911) — El Espacio Vacío</b><br><br>• <b>Principio:</b> Núcleo denso positivo y espacio vacío periférico.<br>• <b>Aporte:</b> Electrones libres en la corteza listos para interactuar.</div>", unsafe_allow_html=True)
            elif "Bohr" in modelo:
                st.markdown("<div class='card-bohr'><b style='color:#ffb142; font-size: 1.2rem;'>Modelo de Bohr (1913) — Órbitas Cuantizadas</b><br><br>• <b>Principio:</b> Niveles fijos de energía.<br>• <b>Límite:</b> Su rigidez 2D no explica la geometría tridimensional orgánica.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card-schrodinger'><b style='color:#00e5ff; font-size: 1.2rem;'>Modelo de Schrödinger (1926) — Orbitales Cuánticos</b><br><br>• <b>Principio:</b> Densidades probabilísticas 3D. Justifica los ángulos de enlace exactos en biomoléculas.</div>", unsafe_allow_html=True)
        
        with col_svg:
            st.components.v1.html(f"<div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px; background-color:rgba(255,255,255,0.02); border-radius:8px;'>{obtener_svg_atomo(modelo)}</div>", height=120, scrolling=False)

        st.markdown("---")
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
                        sincronizar_progreso_db(st.session_state["token_actual"], st.session_state["puntos_acumulados"], 0)
                st.toast("⚡ ¡Afinidad molecular correcta!", icon="✅")
            else:
                st.session_state["racha_consecutiva"] = 0
                st.toast("❌ Los modelos no interactúan.", icon="⚠️")
            st.session_state["memo_reveladas"] = []

        if len(st.session_state["memo_resueltas"]) == 5 and not st.session_state["memo_completado"]:
            st.session_state["memo_completado"] = True
            sincronizar_progreso_db(st.session_state["token_actual"], st.session_state["puntos_acumulados"], 1)

        cols_memo = st.columns(5)
        for i in range(10):
            col_idx = i % 5
            with cols_memo[col_idx]:
                val_tarjeta, id_par = st.session_state["memo_tablero"][i]
                deshabilitado = (id_par in st.session_state["memo_resueltas"]) or (i in st.session_state["memo_reveladas"])
                label = f"✅ {val_tarjeta}" if id_par in st.session_state["memo_resueltas"] else (f"👀 {val_tarjeta}" if i in st.session_state["memo_reveladas"] else "⚛️ Revelar")
                if st.button(label, key=f"btn_memo_{i}", use_container_width=True, disabled=deshabilitado):
                    st.session_state["memo_reveladas"].append(i)
                    st.rerun()

        c_reset, _ = st.columns([1, 3])
        with c_reset:
            if st.button("🔄 Reiniciar Memorama", use_container_width=True):
                st.session_state["memo_tablero"] = mezclar_memorama()
                st.session_state["memo_reveladas"] = []
                st.session_state["memo_resueltas"] = []
                if not st.session_state["memo_completado"]: st.session_state["racha_consecutiva"] = 0
                st.rerun()

        st.write("---")
        st.markdown("### ⚛️ 2. Estructura de un Átomo y Propiedades Periódicas")
        st.markdown("El átomo es la unidad fundamental de la materia. Para comprender la bioquímica celular y el equilibrio osmótico, debemos entender cómo interactúan sus partículas subatómicas.")

        col1_at, col2_at = st.columns([1, 1])
        with col1_at:
            protones = st.slider("Protones (Número Atómico Z)", min_value=1, max_value=20, value=6, step=1)
            neutrones = st.slider("Neutrones (Masa Nuclear)", min_value=0, max_value=22, value=6, step=1)
            electrones = st.slider("Electrones (Capa Externa)", min_value=0, max_value=20, value=6, step=1)

        tabla_elementos = {
            1: {"simbolo": "H", "nombre": "Hidrógeno"}, 6: {"simbolo": "C", "nombre": "Carbono"},
            7: {"simbolo": "N", "nombre": "Nitrógeno"}, 8: {"simbolo": "O", "nombre": "Oxígeno"},
            11: {"simbolo": "Na", "nombre": "Sodio"}, 12: {"simbolo": "Mg", "nombre": "Magnesio"},
            15: {"simbolo": "P", "nombre": "Fósforo"}, 16: {"simbolo": "S", "nombre": "Azufre"},
            17: {"simbolo": "Cl", "nombre": "Cloro"}, 20: {"simbolo": "Ca", "nombre": "Calcio"}
        }

        masa_atomica = protones + neutrones
        carga_neta = protones - electrones
        elem = tabla_elementos.get(protones, {"simbolo": "X", "nombre": "Elemento Genérico"})

        with col2_at:
            st.markdown(f"""
            <div style="background-color: #1e293b; padding: 22px; border-radius: 12px; border-left: 5px solid #3b82f6; color: #f8fafc; margin-bottom: 15px;">
                <h4 style="margin-top: 0; color: #60a5fa;">📊 Estado del Átomo: {elem['nombre']} (<sup>{masa_atomica}</sup><sub>{protones}</sub>{elem['simbolo']})</h4>
                <p style="margin: 6px 0;"><b>Número Atómico (Z):</b> {protones} (Protones en el núcleo)</p>
                <p style="margin: 6px 0;"><b>Masa Atómica (A):</b> {masa_atomica} u.m.a. (Protones + Neutrones)</p>
                <p style="margin: 6px 0;"><b>Carga Eléctrica Neta:</b> {f"+{carga_neta}" if carga_neta > 0 else carga_neta}</p>
            </div>
            """, unsafe_allow_html=True)
            if carga_neta == 0: st.success("✨ **Átomo Eléctricamente Neutro**")
            elif carga_neta > 0: st.warning("🔋 **Catión (Ion positivo)**")
            else: st.info("🪫 **Anión (Ion negativo)**")

        st.write("---")
        st.markdown("### 🧬 3. Enlaces Químicos e Interacciones Moleculares")
        
        electronegatividades_m1 = {"Hidrógeno (H)": 2.20, "Carbono (C)": 2.55, "Nitrógeno (N)": 3.04, "Oxígeno (O)": 3.44, "Sodio (Na)": 0.93, "Cloro (Cl)": 3.16, "Calcio (Ca)": 1.00}
        col_fusion1, col_fusion2 = st.columns(2)
        with col_fusion1: atomo_a_m1 = st.selectbox("Átomo A:", list(electronegatividades_m1.keys()), index=1)
        with col_fusion2: atomo_b_m1 = st.selectbox("Átomo B:", list(electronegatividades_m1.keys()), index=3)

        if st.button("🧬 Iniciar Fusión Atómica", use_container_width=True):
            delta_chi = round(abs(electronegatividades_m1[atomo_a_m1] - electronegatividades_m1[atomo_b_m1]), 2)
            st.markdown(f"<h4 style='text-align: center; color: #10b981;'>Resultado de la Reacción (Diferencia de Electronegatividad = {delta_chi})</h4>", unsafe_allow_html=True)
            
            if (atomo_a_m1 == "Hidrógeno (H)" and atomo_b_m1 == "Oxígeno (O)") or (atomo_a_m1 == "Oxígeno (O)" and atomo_b_m1 == "Hidrógeno (H)"):
                st.markdown("""<div class='card-hint'><h5>🌊 Enlace Covalente Polar + Potencial de Puente de Hidrógeno</h5><p>Se inducen densidades de carga parcial. Forma puentes de hidrógeno, clave en el agua celular.</p></div>""", unsafe_allow_html=True)
            elif delta_chi >= 1.7:
                st.markdown("""<div class='card-error'><h5>⚡ Enlace No Covalente: Iónico</h5><p>Se generan un catión y un anión estables unidos por atracción electrostática permanente.</p></div>""", unsafe_allow_html=True)
            elif 0.4 <= delta_chi < 1.7:
                st.markdown("""<div style='background-color: #faf5ff; padding: 20px; border-radius: 8px; border: 1px solid #e9d5ff; color: #581c87;'><h5>🧪 Enlace Covalente Polar</h5><p>Los átomos comparten electrones de forma asimétrica, reteniendo carga parcial en los polos moleculares.</p></div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class='card-success'><h5>💎 Enlace Covalente No Polar (Apolar)</h5><p>Distribución equitativa y simétrica. Alta estabilidad hidrofóbica biológica en membranas.</p></div>""", unsafe_allow_html=True)

    elif "Estación B" in estacion_actual:
        st.markdown("### Fuerzas Intermoleculares y Solubilidad")
        st.info("**Puentes de Hidrógeno e Interacciones de Van der Waals**\n* **Fuerzas Cohesivas:** Dipolo-dipolo extremo.\n* **Fuerzas de Van der Waals:** Estabilizan núcleos hidrofóbicos.")
        g_soluto = st.number_input("Masa de Soluto (g):", min_value=1.0, value=18.0)
        vol_l = st.slider("Volumen (L):", 0.1, 5.0, 1.0, 0.1)
        st.success(f"Concentración: **{((g_soluto / 180.15) / vol_l):.3f} M** (Glucosa).")

    elif "Estación C" in estacion_actual:
        st.markdown("### Estructura de los Grupos Funcionales")
        grupo = st.selectbox("Grupo Funcional:", ["Carbonilo (C=O)", "Metilo (CH3)", "Hidroxilo (-OH)", "Tiol / Disulfuro (-SH)", "Fosforilo (-PO3)"])
        st.warning(f"Revisando propiedades bioquímicas del grupo {grupo}.")

    else:
        st.markdown("### pH y Sistemas Amortiguadores")
        solucion = st.radio("Cámara de Perfusión Sanguínea:", ["Plasma con Bicarbonato (pH 7.4)", "Agua Destilada (pH 7.0)"])
        if st.button("Inyectar 10 mL de HCl", use_container_width=True):
            if "Agua" in solucion:
                if not st.session_state.advertencia_ph:
                    st.markdown("<div class='card-hint'>💡 El agua carece de tampones. Presiona de nuevo para confirmar.</div>", unsafe_allow_html=True)
                    st.session_state.advertencia_ph = True
                else:
                    st.markdown("<div class='card-error'>🩸 <b>CHOQUE POR ACIDOSIS</b> <b>-1 Vida.</b></div>", unsafe_allow_html=True)
                    st.session_state.vidas -= 1
                    st.session_state.advertencia_ph = False
            else:
                st.markdown("<div class='card-success'>🛡️ <b>EFECTO TAMPÓN EXITOSO.</b></div>", unsafe_allow_html=True)

