import streamlit as st
import time
from database import sincronizar_progreso_db, otorgar_tiempo_extra_db
from assets import obtener_svg_atomo, mezclar_memorama, generar_svg_enlace, ELEMENTOS

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
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown("---")

    if "Estación A" in estacion_actual:
        st.markdown("### Evolución de la Teoría Atómica, Estructura y Enlaces Químicos")
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
                st.markdown("<div class='card-dalton'><b style='color:#90a4ae; font-size: 1.2rem;'>Modelo de Dalton (1810) — Átomo Indivisible</b><br><br>• <b>Principio:</b> El átomo es una esfera sólida sin cargas.<br>• <b>Límite:</b> Incapaz de explicar uniones químicas al carecer de electrones.</div>", unsafe_allow_html=True)
            elif "Thomson" in modelo:
                st.markdown("<div class='card-thomson'><b style='color:#9c27b0; font-size: 1.2rem;'>Modelo de Thomson (1897) — El Electrón</b><br><br>• <b>Principio:</b> Descubre el electrón. Masa positiva con cargas negativas incrustadas.<br>• <b>Aporte:</b> Introduce la naturaleza eléctrica de la materia.</div>", unsafe_allow_html=True)
            elif "Rutherford" in modelo:
                st.markdown("<div class='card-rutherford'><b style='color:#2196f3; font-size: 1.2rem;'>Modelo de Rutherford (1911) — El Espacio Vacío</b><br><br>• <b>Principio:</b> Núcleo denso positivo y espacio vacío periférico.<br>• <b>Aporte:</b> Electrones libres en la corteza listos para interactuar.</div>", unsafe_allow_html=True)
            elif "Bohr" in modelo:
                st.markdown("<div class='card-bohr'><b style='color:#ffb142; font-size: 1.2rem;'>Modelo de Bohr (1913) — Órbitas Cuantizadas</b><br><br>• <b>Principio:</b> Niveles fijos de energía.<br>• <b>Límite:</b> Su rigidez 2D no explica la geometría tridimensional orgánica.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card-schrodinger'><b style='color:#00e5ff; font-size: 1.2rem;'>Modelo de Schrödinger (1926) — Orbitales Cuánticos</b><br><br>• <b>Principio:</b> Densidades probabilísticas 3D.<br>• <b>Eje Estructural:</b> Justifica los ángulos de enlace exactos (como el agua en 'V') y la flexibilidad de acoplamiento enzima-sustrato.</div>", unsafe_allow_html=True)
        
        with col_svg:
            st.components.v1.html(f"<div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px; background-color:rgba(255,255,255,0.02); border-radius:8px;'>{obtener_svg_atomo(modelo)}</div>", height=120, scrolling=False)

        st.markdown("---")
        st.markdown("### 🧠 Desafío de Consolidación: Memorama Atómico")
        if st.session_state["memo_completado"]:
            st.caption("✨ *Modo Práctica Activo: Avance oficial sellado en el servidor. Repasa libremente.*")
        else:
            st.caption("🔥 *Modo Oficial Activo: Consigue una racha de 2 aciertos consecutivos sin errores para ganar puntos e incrementar tu licencia.*")

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
                if id_par in st.session_state["memo_resueltas"]:
                    label = f"✅ {val_tarjeta}"
                    deshabilitado = True
                elif i in st.session_state["memo_reveladas"]:
                    label = f"👀 {val_tarjeta}"
                    deshabilitado = True
                else:
                    label = "⚛️ Revelar"
                    deshabilitado = False
                if st.button(label, key=f"btn_memo_{i}", use_container_width=True, disabled=deshabilitado):
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

        st.write("---")

        st.markdown("### ⚛️ 2. Estructura de un Átomo y Propiedades Periódicas")
        st.markdown("""
        El átomo es la unidad fundamental de la materia. Para comprender la bioquímica celular y el equilibrio osmótico, 
        debemos entender cómo interactúan sus partículas subatómicas: **protones** (con carga positiva, definen la identidad del elemento), 
        **neutrones** (neutros, aportan estabilidad nuclear) y **electrones** (con carga negativa, responsables directos de los enlaces químicos).
        """)

        st.markdown("#### 🛠️ Simulador: Construye y Analiza tu Átomo")
        st.caption("Modifica las partículas subatómicas usando los controles deslizantes (barras rojas) para observar las propiedades en tiempo real:")

        col1_at, col2_at = st.columns([1, 1])

        with col1_at:
            protones = st.slider("Protones (Número Atómico Z)", min_value=1, max_value=20, value=6, step=1, help="Define la identidad del elemento químico.")
            neutrones = st.slider("Neutrones (Estabilidad Nuclear)", min_value=0, max_value=22, value=6, step=1, help="Sumados a los protones determinan la masa total.")
            electrones = st.slider("Electrones (Capa de Valencia)", min_value=0, max_value=20, value=6, step=1, help="Determinan la carga eléctrica neta del átomo.")

        tabla_elementos = {
            1: {"simbolo": "H", "nombre": "Hidrógeno", "bio": "Componente fundamental del agua y biomoléculas orgánicas; clave en la regulación del pH hídrico celular."},
            6: {"simbolo": "C", "nombre": "Carbono", "bio": "El esqueleto estructural de la bioquímica macromolecular. Capaz de organizar hasta 4 enlaces estables."},
            7: {"simbolo": "N", "nombre": "Nitrógeno", "bio": "Estructura maestra constituyente de los aminoácidos (proteínas) y bases nitrogenadas (ADN y ARN)."},
            8: {"simbolo": "O", "nombre": "Oxígeno", "bio": "Aceptor final de electrones en la respiración mitocondrial celular y componente central del agua."},
            11: {"simbolo": "Na", "nombre": "Sodio", "bio": "Catión extracelular principal; indispensable para regular el potencial de acción y la presión osmótica."},
            12: {"simbolo": "Mg", "nombre": "Magnesio", "bio": "Cofactor esencial en más de 300 reacciones enzimáticas, incluyendo el uso biológico energético de ATP."},
            15: {"simbolo": "P", "nombre": "Fósforo", "bio": "Constituyente de los enlaces fosfodiéster en ácidos nucleicos y de las uniones de alta energía del ATP."},
            16: {"simbolo": "S", "nombre": "Azufre", "bio": "Presente en aminoácidos como la cisteína, formando puentes disulfuro determinantes en la estructura proteica."},
            17: {"simbolo": "Cl", "nombre": "Cloro", "bio": "Anión extracelular primario; encargado de mantener el balance de neutralidad y balance hídrico."},
            20: {"simbolo": "Ca", "nombre": "Calcio", "bio": "Segundo mensajero celular; esencial en la contracción muscular, cascada de coagulación y soporte mineral óseo."}
        }

        masa_atomica = protones + neutrones
        carga_neta = protones - electrones

        if protones in tabla_elementos:
            nombre_elem = tabla_elementos[protones]["nombre"]
            simbolo_elem = tabla_elementos[protones]["simbolo"]
            info_bio = tabla_elementos[protones]["bio"]
        else:
            nombre_elem = "Elemento Genérico / Isótopo Especial"
            simbolo_elem = "X"
            info_bio = "Estudiado en química general por sus propiedades de configuración periférica y estabilidad electrónica."

        with col2_at:
            st.markdown(f"""
            <div style="background-color: #1e293b; padding: 22px; border-radius: 12px; border-left: 5px solid #3b82f6; color: #f8fafc; margin-bottom: 15px;">
                <h4 style="margin-top: 0; color: #60a5fa;">📊 Estado del Átomo: {nombre_elem} (<sup>{masa_atomica}</sup><sub>{protones}</sub>{simbolo_elem})</h4>
                <p style="margin: 6px 0; font-size: 1.05rem;"><b>Número Atómico (Z):</b> {protones} <span style="color: #94a3b8;">(Total de protones en el núcleo)</span></p>
                <p style="margin: 6px 0; font-size: 1.05rem;"><b>Masa Atómica (A):</b> {masa_atomica} u.m.a. <span style="color: #94a3b8;">(Protones + Neutrones)</span></p>
                <p style="margin: 6px 0; font-size: 1.05rem;"><b>Carga Eléctrica Neta:</b> {f"+{carga_neta}" if carga_neta > 0 else carga_neta}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if carga_neta == 0:
                st.success(f"✨ **Átomo Eléctricamente Neutro:** El número de protones coincide simétricamente con el de electrones periféricos.")
            elif carga_neta > 0:
                st.warning(f"🔋 **Catión (Ion con carga positiva):** Ha cedido o perdido {carga_neta} electrón(es). Posee afinidad por zonas negativas.")
            else:
                st.info(f"🪫 **Anión (Ion con carga negativa):** Ha ganado {abs(carga_neta)} electrón(es). Posee una alta densidad de carga electrónica.")
                
            st.markdown(f"**Relevancia Fisiológica Celular:** *{info_bio}*")

        st.write("---")

        st.markdown("### 🧬 3. Enlaces Químicos e Interacciones Moleculares")
        st.markdown("""
        Los enlaces químicos representan las fuerzas moleculares estables que mantienen unidos a los átomos para organizar compuestos complejos. 
        La naturaleza de cada interacción depende estrictamente de la **electronegatividad**, la cual mide la fuerza relativa que posee un núcleo 
        para atraer electrones de valencia compartidos.
        """)

        st.markdown("#### 🔬 Juego de Simulación: Laboratorio de Fusión Atómica")
        st.caption("Selecciona dos átomos para fundirlos y descubrir el tipo de enlace exacto de acuerdo a su Diferencia de Electronegatividad (Delta-X):")

        electronegatividades_m1 = {
            "Hidrógeno (H)": 2.20,
            "Carbono (C)": 2.55,
            "Nitrógeno (N)": 3.04,
            "Oxígeno (O)": 3.44,
            "Sodio (Na)": 0.93,
            "Cloro (Cl)": 3.16,
            "Calcio (Ca)": 1.00
        }

        col_fusion1, col_fusion2 = st.columns(2)
        with col_fusion1:
            atomo_a_m1 = st.selectbox("Selecciona el Átomo A:", list(electronegatividades_m1.keys()), index=1)
        with col_fusion2:
            atomo_b_m1 = st.selectbox("Selecciona el Átomo B:", list(electronegatividades_m1.keys()), index=3)

        if st.button("🧬 Iniciar Fusión Atómica", use_container_width=True):
            chi_a = electronegatividades_m1[atomo_a_m1]
            chi_b = electronegatividades_m1[atomo_b_m1]
            delta_chi = round(abs(chi_a - chi_b), 2)
            
            st.markdown(f"<h4 style='text-align: center; color: #10b981;'>Resultado de la Reacción (Diferencia de Electronegatividad = {delta_chi})</h4>", unsafe_allow_html=True)
            
            if (atomo_a_m1 == "Hidrógeno (H)" and atomo_b_m1 == "Oxígeno (O)") or (atomo_a_m1 == "Oxígeno (O)" and atomo_b_m1 == "Hidrógeno (H)"):
                st.markdown(f"""
                <div style="background-color: #eff6ff; padding: 20px; border-radius: 8px; border: 1px solid #bfdbfe; color: #1e3a8a;">
                    <h5>🌊 Enlace Covalente Polar + Potencial de Puente de Hidrógeno</h5>
                    <p>La diferencia de electronegatividad es de <b>{delta_chi}</b>. El Oxígeno atrae los electrones del Hidrógeno de forma asimétrica, 
                    induciendo densidades de carga parcial (carga parcial negativa en el Oxígeno y carga parcial positiva en el Hidrógeno).</p>
                    <p><b>¡Pilar Biológico!</b> Esta asimetría de cargas permite que el hidrógeno cargado positivamente de una molécula de agua atraiga electrostáticamente 
                    al oxígeno con carga negativa de otra molécula vecina. Esto forma un <b>Puente de Hidrógeno</b>, clave en la cohesión y el elevado calor específico celular.</p>
                </div>
                """, unsafe_allow_html=True)
            elif delta_chi >= 1.7:
                st.markdown(f"""
                <div style="background-color: #fff7ed; padding: 20px; border-radius: 8px; border: 1px solid #fed7aa; color: #7c2d12;">
                    <h5>⚡ Enlace No Covalente: Iónico</h5>
                    <p>La diferencia de electronegatividad es crítica (<b>{delta_chi} mayor o igual a 1.7</b>). En este escenario, no se comparten electrones.</p>
                    <p>El elemento altamente electronegativo arranca por completo el electrón periférico del átomo electropositivo, generando 
                    un catión y un anión estables que permanecen estrechamente consolidados por **atracción electrostática**.</p>
                </div>
                """, unsafe_allow_html=True)
            elif 0.4 <= delta_chi < 1.7:
                st.markdown(f"""
                <div style="background-color: #faf5ff; padding: 20px; border-radius: 8px; border: 1px solid #e9d5ff; color: #581c87;">
                    <h5>🧪 Enlace Covalente Polar</h5>
                    <p>La diferencia de electronegatividad se encuentra en un rango intermedio (<b>{delta_chi}</b>).</p>
                    <p>Los átomos comparten electrones, pero lo hacen de forma asimétrica. El enlace común en carbohidratos y cadenas de aminoácidos solubles.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; border: 1px solid #bbf7d0; color: #14532d;">
                    <h5>💎 Enlace Covalente No Polar (Apolar)</h5>
                    <p>La diferencia de electronegatividad es baja o nula (<b>{delta_chi} menor a 0.4</b>).</p>
                    <p>Es un enlace de alta estabilidad hidrofóbica que define el comportamiento protector de los lípidos moleculares y membranas biológicas.</p>
                </div>
                """, unsafe_allow_html=True)

    elif "Estación B" in estacion_actual:
        st.markdown("### Fuerzas Intermoleculares y Solubilidad")
        st.info("""**Puentes de Hidrógeno e Interacciones de Van der Waals**
        \n* **Fuerzas Cohesivas:** Dipolo-dipolo extremo en el agua. Explica su punto de ebullición y calor específico.
        \n* **Fuerzas de Van der Waals:** Interacciones débiles que estabilizan núcleos hidrofóbicos proteicos.
        \n* **Efecto Hidrofóbico:** Exclusión termodinámica de solutos apolares, forzando el ensamblaje de la bicapa lipídica celular.""")
        
        st.markdown("#### 🧪 Calculadora de Disoluciones Molares")
        g_soluto = st.number_input("Masa de Soluto (g):", min_value=1.0, value=18.0)
        vol_l = st.slider("Volumen de la Disolución (L):", 0.1, 5.0, 1.0, 0.1)
        molaridad = (g_soluto / 180.15) / vol_l
        st.success(f"Concentración Calculada: **{molaridad:.3f} M** (Glucosa).")

    elif "Estación C" in estacion_actual:
        st.markdown("### Estructura de los Grupos Funcionales")
        grupo = st.selectbox("Grupo Funcional a Inspeccionar:", ["Carbonilo (C=O)", "Metilo (CH3)", "Hidroxilo (-OH)", "Tiol / Disulfuro (-SH)", "Fosforilo (-PO3)"])
        if "Carbonilo" in grupo:
            st.warning("**Carbonilo:** Propio de aldehídos/cetonas. Centro neurálgico del metabolismo de glúcidos.")
        elif "Metilo" in grupo:
            st.warning("**Metilo:** Hidrofóbico, crítico en empaquetamiento estructural y marcas epigenéticas de metilación en el ADN.")
        elif "Tiol" in grupo:
            st.warning("**Tiol/Disulfuro:** Puentes covalentes cruzados de cisteína. Brindan rigidez mecánica a pezuñas y cuernos por la queratina.")
        else:
            st.warning("Grupo funcional característico de biomoléculas celulares.")

    else:
        st.markdown("### pH y Sistemas Amortiguadores")
        solucion = st.radio("Cámara de Perfusión Sanguínea:", ["Plasma con Amortiguador Bicarbonato (pH 7.4)", "Agua Destilada Pura (pH 7.0)"])
        if st.button("Inyectar 10 mL de HCl", use_container_width=True):
            if "Agua" in solucion:
                if not st.session_state.advertencia_ph:
                    st.markdown("<div class='card-hint'>💡 <b>ALERTA INTERACTIVA:</b> El agua destilada carece de tampones. Inyectar HCl causará desnaturalización ácida masiva. Presiona de nuevo si deseas ejecutar la acción.</div>", unsafe_allow_html=True)
                    st.session_state.advertencia_ph = True
                else:
                    st.markdown("<div class='card-error'>🩸 <b>CHOQUE POR ACIDOSIS:</b> El pH colapsó a 2.0. Proteínas plasmáticas destruidas. <b>-1 Vida.</b></div>", unsafe_allow_html=True)
                    st.session_state.vidas -= 1
                    st.session_state.advertencia_ph = False
            else:
                st.markdown("<div class='card-success'>🛡️ <b>EFECTO TAMPÓN EXITOSO:</b> El amortiguador fisiológico absorbió los protones (H+) generando ácido carbónico, el cual se disociará en CO2 eliminable vía pulmonar.</div>", unsafe_allow_html=True)
                st.session_state.advertencia_ph = False
