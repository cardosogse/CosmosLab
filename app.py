import streamlit as st
import sqlite3
import random
import string
from datetime import datetime

# ==========================================
# 0. CONFIGURACIÓN E INICIALIZACIÓN DE LA BD
# ==========================================
def init_db():
    conn = sqlite3.connect("mainlab_data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cupones (
            token TEXT PRIMARY KEY,
            modulo_maximo TEXT DEFAULT 'Ninguno',
            puntos INT DEFAULT 0,
            vidas INT DEFAULT 3,
            racha INT DEFAULT 1,
            ultima_conexion TEXT,
            vigencia_dias INT DEFAULT 30,
            fecha_creacion TEXT,
            estado TEXT DEFAULT 'Activo',
            intentos_quiz INT DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Inicialización estricta de estados de sesión
if "auth" not in st.session_state: st.session_state["auth"] = False
if "admin_auth" not in st.session_state: st.session_state["admin_auth"] = False
if "token_actual" not in st.session_state: st.session_state["token_actual"] = None
if "puntos_acumulados" not in st.session_state: st.session_state["puntos_acumulados"] = 0
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "racha" not in st.session_state: st.session_state["racha"] = 1
if "estacion" not in st.session_state: st.session_state["estacion"] = "Día 1: Introducción"
if "advertencia_ph" not in st.session_state: st.session_state["advertencia_ph"] = False
if "errores_quiz" not in st.session_state: st.session_state["errores_quiz"] = 0

def validar_token_db(token):
    conn = sqlite3.connect("mainlab_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT modulo_maximo, puntos, vidas, racha FROM cupones WHERE token=? AND estado='Activo'", (token,))
    res = cursor.fetchone()
    conn.close()
    return res

def actualizar_conexion_db(token):
    conn = sqlite3.connect("mainlab_data.db")
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("UPDATE cupones SET ultima_conexion=? WHERE token=?", (ahora, token))
    conn.commit()
    conn.close()

# ==========================================
# 1. INYECCIÓN DE ESTILOS AVANZADOS (UI/UX)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #0d1117 0%, #07090e 100%);
        font-family: 'Inter', sans-serif;
        color: #c9d1d9;
    }
    
    /* Animación Radiactiva del Logo 'Lab' */
    @keyframes pulso-radiactivo {
        0% { text-shadow: 0 0 4px #00f2fe, 0 0 8px #00f2fe; color: #00f2fe; }
        50% { text-shadow: 0 0 16px #4facfe, 0 0 25px #00f2fe, 0 0 30px #4facfe; color: #ffffff; }
        100% { text-shadow: 0 0 4px #00f2fe, 0 0 8px #00f2fe; color: #00f2fe; }
    }
    .brand-main { font-family: 'Orbitron', sans-serif; font-size: 3rem; font-weight: 700; color: #ffffff; text-align: center; margin-bottom: 0px; }
    .brand-lab { animation: pulso-radiactivo 3s infinite ease-in-out; }
    
    .sub-title { font-size: 1.1rem; color: #8b949e; text-align: center; margin-top: 5px; margin-bottom: 25px; font-weight: 300; }
    .section-header-custom { font-family: 'Orbitron', sans-serif; font-size: 1.15rem; color: #ffffff; font-weight: 600; margin-bottom: 15px; }
    
    .lab-panel {
        background: rgba(22, 27, 34, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
    }
    
    /* KPIs Redimensionados y Armónicos (No gigantes) */
    .kpi-card-mini {
        background: rgba(13, 17, 23, 0.6);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .kpi-val { font-family: 'Orbitron', sans-serif; font-size: 1.4rem; font-weight: bold; margin: 5px 0; }
    
    .card-success { background: rgba(46, 204, 113, 0.1); border-left: 5px solid #2ecc71; padding: 12px; border-radius: 4px; color: #2ecc71; }
    .card-error { background: rgba(231, 76, 60, 0.1); border-left: 5px solid #e74c3c; padding: 12px; border-radius: 4px; color: #e74c3c; }
    .card-hint { background: rgba(52, 152, 219, 0.1); border-left: 5px solid #3498db; padding: 12px; border-radius: 4px; color: #3498db; }
</style>
""", unsafe_allow_html=True)

# Encabezado Principal de la Marca
st.markdown("<h1 class='brand-main'>Main<span class='brand-lab'>Lab</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Bioquímica aplicada. Ciencia interactiva. Sin límites.</p>", unsafe_allow_html=True)

def interceptor_infraestructura():
    st.markdown("<div class='card-error'><b>🚨 MONITOR DE INFRAESTRUCTURA: ANOMALÍA DETECTADA EN LA LÓGICA</b></div>", unsafe_allow_html=True)

# ==========================================
# 2. SISTEMA DE AUTENTICACIÓN OCULTO
# ==========================================
if not st.session_state["auth"] and not st.session_state["admin_auth"]:
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header-custom'>🔒 Acceso a Estaciones de Trabajo</div>", unsafe_allow_html=True)
    
    input_token = st.text_input("Introduce tu Cupón de Acceso:", type="password", placeholder="ML-XXXXXX / Código Especial").strip()
    
    if st.button("Autenticar e Ingresar", use_container_width=True):
        if input_token == "SYS-ADMIN-99":
            st.session_state["admin_auth"] = True
            st.success("Consola del Administrador Desbloqueada.")
            st.rerun()
        elif input_token:
            datos = validar_token_db(input_token)
            if datos:
                st.session_state["auth"] = True
                st.session_state["token_actual"] = input_token
                st.session_state["estacion"] = datos[0] if datos[0] != 'Ninguno' else "Día 1: Introducción"
                st.session_state["puntos_acumulados"] = datos[1]
                st.session_state["vidas"] = datos[2]
                st.session_state["racha"] = datos[3]
                actualizar_conexion_db(input_token)
                st.rerun()
            else:
                st.error("Cupón inválido o inexistente.")
        else:
            st.warning("Escribe un código.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 3. ENTORNO EXCLUSIVO DEL ADMINISTRADOR
# ==========================================
elif st.session_state["admin_auth"]:
    st.markdown("<div class='lab-panel' style='border-color: #ff00ff;'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header-custom'>🔑 Consola de Administración y Control de Cupones</div>", unsafe_allow_html=True)
    
    # Inyector de Licencias
    dias_vigencia = st.number_input("Vigencia de la licencia (Días):", min_value=1, max_value=365, value=30)
    if st.button("Generar e Inyectar Token", use_container_width=True):
        prefix = "MLP-" if dias_vigencia >= 90 else "ML-"
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        nuevo_token = f"{prefix}{random_str}"
        
        conn = sqlite3.connect("mainlab_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cupones (token, fecha_creacion, vigencia_dias) VALUES (?, ?, ?)",
                       (nuevo_token, datetime.now().strftime("%Y-%m-%d"), dias_vigencia))
        conn.commit()
        conn.close()
        st.success(f"Licencia inyectada: **{nuevo_token}** ({dias_vigencia} Días)")
    st.markdown("</div>", unsafe_allow_html=True)

    # Monitor Detallado de Tokens (Abajo del generador)
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header-custom'>📋 Monitor de Cupones Activos</div>", unsafe_allow_html=True)
    
    conn = sqlite3.connect("mainlab_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT token, modulo_maximo, puntos, vidas, racha, ultima_conexion FROM cupones")
    filas = cursor.fetchall()
    conn.close()
    
    if filas:
        for f in filas:
            icono_vida = "💚 3/3" if f[3] == 3 else ("⚠️ 2/3" if f[3] == 2 else "🚨 1/3")
            st.write(f"**Cupón:** `{f[0]}` | **Estación:** {f[1]} | **Puntos:** {f[2]} | **Vidas:** {icono_vida} | **Conexión:** {f[5]}")
    else:
        st.info("No hay cupones registrados.")
    st.markdown("</div>", unsafe_allow_html=True)

    # SECCIÓN INFERIOR: KPIs Globales Redimensionados y Armónicos
    st.markdown("<div class='lab-panel' style='border-color: #3498db;'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header-custom'>📊 Métricas Macro del Ecosistema</div>", unsafe_allow_html=True)
    
    conn = sqlite3.connect("mainlab_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), AVG(puntos), COUNT(*) FROM cupones WHERE vidas = 1")
    totales = cursor.fetchone()
    total_t = totales[0] if totales[0] else 0
    media_p = round(totales[1], 1) if totales[1] else 0
    criticos = totales[2] if totales[2] else 0
    conn.close()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='kpi-card-mini'><small style='color:#2ecc71;'>🏆 Promedio Rendimiento</small><div class='kpi-val' style='color:#2ecc71;'>{media_p} PTS</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='kpi-card-mini'><small style='color:#e74c3c;'>💔 Riesgos de Lisis</small><div class='kpi-val' style='color:#e74c3c;'>{criticos} Alum.</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='kpi-card-mini'><small style='color:#f1c40f;'>🎫 Total Cupones</small><div class='kpi-val' style='color:#f1c40f;'>{total_t} u.</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Cerrar Consola del Administrador", type="primary", use_container_width=True):
        st.session_state["admin_auth"] = False
        st.rerun()

# ==========================================
# 4. ENTORNO NORMAL DEL ESTUDIANTE
# ==========================================
if st.session_state["auth"] and not st.session_state["admin_auth"]:
    st.markdown("<div class='lab-panel' style='border-color: #00f2fe;'>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-header-custom'>🧬 Panel Estudiantil • Usuario: {st.session_state['token_actual']}</div>", unsafe_allow_html=True)
    
    col_e1, col_e2, col_e3 = st.columns(3)
    col_e1.metric("Puntos", f"{st.session_state['puntos_acumulados']} PTS")
    col_e2.metric("Sistemas Vitales", f"{st.session_state['vidas']} / 3")
    col_e3.metric("Racha", f"{st.session_state['racha']}x")
    
    estacion_actual = st.selectbox(
        "Estación de Trabajo:",
        ["Día 1: Introducción", "Día 2: Biomoléculas", "Día 3: Termodinámica", "Día 4: Equilibrio Ácido-Base"],
        index=["Día 1: Introducción", "Día 2: Biomoléculas", "Día 3: Termodinámica", "Día 4: Equilibrio Ácido-Base"].index(st.session_state["estacion"]) if st.session_state["estacion"] in ["Día 1: Introducción", "Día 2: Biomoléculas", "Día 3: Termodinámica", "Día 4: Equilibrio Ácido-Base"] else 0
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    def sincronizar_progreso_db(token, puntos, intentos_sumar=0):
        conn = sqlite3.connect("mainlab_data.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE cupones SET modulo_maximo=?, puntos=?, intentos_quiz = intentos_quiz + ? WHERE token?", 
                       (estacion_actual, puntos, intentos_sumar, token))
        conn.commit()
        conn.close()

    try:
        if "Día 1" in estacion_actual:
            st.info("Módulo 1: Conceptos introductorios e instrumental analítico.")
        elif "Día 2" in estacion_actual:
            st.info("Módulo 2: Interacciones estereoquímicas macromoleculares.")
        elif "Día 3" in estacion_actual:
            st.info("Módulo 3: Entropía y bioenergética del enlace celular.")
        elif "Día 4" in estacion_actual:
            from modulos.m1_dia4 import mostrar_dia4
            mostrar_dia4()
    except Exception as e:
        interceptor_infraestructura()
        st.error(f"Detalle: {e}")
        
    if st.button("Cerrar Sesión del Laboratorio", use_container_width=True):
        st.session_state["auth"] = False
        st.session_state["token_actual"] = None
        st.rerun()
