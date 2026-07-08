import streamlit as st
import sqlite3
import random
import string
from datetime import datetime, timedelta

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

# Inicialización de estados globales
if "auth" not in st.session_state: st.session_state["auth"] = False
if "admin_auth" not in st.session_state: st.session_state["admin_auth"] = False
if "token_actual" not in st.session_state: st.session_state["token_actual"] = None
if "puntos_acumulados" not in st.session_state: st.session_state["puntos_acumulados"] = 0
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "racha" not in st.session_state: st.session_state["racha"] = 1
if "estacion" not in st.session_state: st.session_state["estacion"] = "Día 1: Introducción"
if "advertencia_ph" not in st.session_state: st.session_state["advertencia_ph"] = False
if "errores_quiz" not in st.session_state: st.session_state["errores_quiz"] = 0

# Funciones de soporte para Base de Datos
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
    
    /* Fondo del Universo Profundo */
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
    .brand-main { font-family: 'Orbitron', sans-serif; font-size: 3.2rem; font-weight: 700; color: #ffffff; text-align: center; margin-bottom: 0px; }
    .brand-lab { animation: pulso-radiactivo 3s infinite ease-in-out; }
    
    /* Título de sección Armonizado y Simétrico */
    .sub-title { font-size: 1.15rem; color: #8b949e; text-align: center; margin-top: 5px; margin-bottom: 30px; font-weight: 300; }
    .section-header-custom { font-family: 'Orbitron', sans-serif; font-size: 1.25rem; color: #ffffff; font-weight: 600; margin-bottom: 15px; }
    
    /* Paneles de Neón Traslúcidos (Glassmorphism) */
    .lab-panel {
        background: rgba(22, 27, 34, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Contenedores para Tarjetas de KPIs individuales */
    .kpi-card {
        background: rgba(13, 17, 23, 0.6);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }
    
    /* Alertas Clínicas Especializadas */
    .card-success { background: rgba(46, 204, 113, 0.1); border-left: 5px solid #2ecc71; padding: 12px; border-radius: 4px; color: #2ecc71; margin: 10px 0; }
    .card-warning { background: rgba(241, 196, 15, 0.1); border-left: 5px solid #f1c40f; padding: 12px; border-radius: 4px; color: #f1c40f; margin: 10px 0; }
    .card-error { background: rgba(231, 76, 60, 0.1); border-left: 5px solid #e74c3c; padding: 12px; border-radius: 4px; color: #e74c3c; margin: 10px 0; }
    .card-hint { background: rgba(52, 152, 219, 0.1); border-left: 5px solid #3498db; padding: 12px; border-radius: 4px; color: #3498db; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. ENCABEZADO UNIFICADO DE LA PLATAFORMA
# ==========================================
st.markdown("<h1 class='brand-main'>Main<span class='brand-lab'>Lab</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Bioquímica aplicada. Ciencia interactiva. Sin límites.</p>", unsafe_allow_html=True)

# Interceptor de fallos estructurales para fases de compilación modular
def interceptor_infraestructura():
    st.markdown("""
    <div style='background: rgba(139,0,0,0.15); border: 1px solid #ff4d4d; border-radius:8px; padding:15px; margin-bottom:20px;'>
        <span style='color:#ff4d4d; font-weight:bold;'>🚨 MONITOR DE CONTROL: ERROR DE COMPILACIÓN DETECTADO EN LOS MÓDULOS</span><br>
        <small style='color:#aaa;'>Interceptor de Infraestructura Activo</small>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. COMPORTAMIENTO LÓGICO DE AUTENTICACIÓN
# ==========================================

# Caso A: Nadie ha iniciado sesión (Pantalla limpia de Login)
if not st.session_state["auth"] and not st.session_state["admin_auth"]:
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header-custom'>🔒 Acceso a Estaciones de Trabajo</div>", unsafe_allow_html=True)
    
    input_token = st.text_input("Introduce tu Cupón de Acceso o Código de Validación:", type="password", placeholder="ML-XXXXXX / Código Maestro").strip()
    
    if st.button("Autenticar e Ingresar", use_container_width=True):
        if input_token == "SYS-ADMIN-99":
            st.session_state["admin_auth"] = True
            st.success("Consola del Administrador Desbloqueada con Éxito.")
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
                st.success("Acceso estudiantil autorizado.")
                st.rerun()
            else:
                st.error("Cupón inválido, expirado o inexistente en SQLite.")
        else:
            st.warning("Por favor, digita un código válido.")
    st.markdown("</div>", unsafe_allow_html=True)

# Caso B: Consola de Administración Activa (Con opción de Sesión Dual Integrada)
elif st.session_state["admin_auth"]:
    st.markdown("<div class='lab-panel' style='border-color: #ff00ff;'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header-custom'>📊 Tablero General de KPIs de Rendimiento</div>", unsafe_allow_html=True)
    
    # Consulta analítica macro en SQLite
    conn = sqlite3.connect("mainlab_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), AVG(puntos), AVG(vidas), SUM(intentos_quiz) FROM cupones")
    totales = cursor.fetchone()
    total_tokens = totales[0] if totales[0] else 0
    prom_puntos = round(totales[1], 1) if totales[1] else 0
    prom_vidas = round(totales[2], 2) if totales[2] else 0
    total_quizzes = totales[3] if totales[3] else 0
    
    cursor.execute("SELECT COUNT(*) FROM cupones WHERE vidas = 1")
    criticos_lisis = cursor.fetchone()[0]
    conn.close()
    
    # Render de las Tarjetas KPI con Diseño Esmerilado de Neón
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='kpi-card' style='border-top: 4px solid #2ecc71;'>
            <h4 style='color:#2ecc71; margin:0;'>🏆 Rendimiento Modular</h4>
            <h2 style='margin:10px 0; font-family:Orbitron;'>{prom_puntos} <span style='font-size:1rem;'>PTS</span></h2>
            <p style='font-size:0.85rem; color:#aaa; margin:0;'>Media Académica Global</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""
        <div class='kpi-card' style='border-top: 4px solid #3498db;'>
            <h4 style='color:#3498db; margin:0;'>📅 Evaluaciones Ejecutadas</h4>
            <h2 style='margin:10px 0; font-family:Orbitron;'>{total_quizzes} <span style='font-size:1rem;'>Tests</span></h2>
            <p style='font-size:0.85rem; color:#aaa; margin:0;'>Intentos Totales en Quizzes</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        color_lisis = "#e74c3c" if criticos_lisis > 0 else "#2ecc71"
        st.markdown(f"""
        <div class='kpi-card' style='border-top: 4px solid {color_lisis};'>
            <h4 style='color:{color_lisis}; margin:0;'>💔 Tasa de Riesgo de Lisis</h4>
            <h2 style='margin:10px 0; font-family:Orbitron;'>{criticos_lisis} <span style='font-size:1rem;'>Alumnos</span></h2>
            <p style='font-size:0.85rem; color:#aaa; margin:0;'>Usuarios con Alerta Crítica (1 Vida)</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""
        <div class='kpi-card' style='border-top: 4px solid #f1c40f;'>
            <h4 style='color:#f1c40f; margin:0;'>🚀 Licencias del Ecosistema</h4>
            <h2 style='margin:10px 0; font-family:Orbitron;'>{total_tokens} <span style='font-size:1rem;'>Activas</span></h2>
            <p style='font-size:0.85rem; color:#aaa; margin:0;'>Cupones Totales Distribuidos</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Herramientas de Gestión de Cupones (Nomenclatura ML y MLP Automática)
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header-custom'>🛠️ Inyector y Generador de Licencias</div>", unsafe_allow_html=True)
    
    dias_vigencia = st.number_input("Establecer vigencia de la licencia (Días):", min_value=1, max_value=365, value=30)
    
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
        st.success(f"Licencia inyectada con éxito: **{nuevo_token}** ({dias_vigencia} Días de duración)")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Monitor Detallado por Token en Tiempo Real
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header-custom'>📋 Monitor Detallado por Token (Tiempo Real)</div>", unsafe_allow_html=True)
    
    conn = sqlite3.connect("mainlab_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT token, modulo_maximo, puntos, vidas, racha, ultima_conexion FROM cupones")
    filas = cursor.fetchall()
    conn.close()
    
    if filas:
        for f in filas:
            icono_vida = "💚 3/3" if f[3] == 3 else ("⚠️ 2/3" if f[3] == 2 else "🚨 1/3")
            st.write(f"**ID:** `{f[0]}` | **Fase:** {f[1]} | **Puntos:** {f[2]} | **Vidas:** {icono_vida} | **Racha:** {f[4]} | **Conexión:** {f[5]}")
    else:
        st.info("No hay cupones registrados en la base de datos.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Panel de Auditoría Dual Interna (Modo Espejo)
    st.markdown("<div class='lab-panel' style='border-color: #3498db;'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header-custom'>🔬 Auditoría de Calidad (Sesión Dual)</div>", unsafe_allow_html=True)
    st.write("Inspecciona el comportamiento y experiencia de un cupón sin perder tus credenciales de administrador.")
    
    token_auditoria = st.text_input("Ingresa un Token Activo para simular:", key="auditar_token_input")
    if st.button("Montar Simulación de Usuario", use_container_width=True):
        datos_aud = validar_token_db(token_auditoria)
        if datos_aud:
            st.session_state["auth"] = True
            st.session_state["token_actual"] = token_auditoria
            st.session_state["estacion"] = datos_aud[0] if datos_aud[0] != 'Ninguno' else "Día 1: Introducción"
            st.session_state["puntos_acumulados"] = datos_aud[1]
            st.session_state["vidas"] = datos_aud[2]
            st.session_state["racha"] = datos_aud[3]
            st.success(f"Espejo enlazado al token `{token_auditoria}`. Baja la página para interactuar.")
        else:
            st.error("Token no válido para auditoría.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Cerrar Sesión del Administrador", type="primary", use_container_width=True):
        st.session_state["admin_auth"] = False
        st.session_state["auth"] = False
        st.session_state["token_actual"] = None
        st.rerun()

# Caso C: Interfaz del Estudiante Activa (O Modo Espejo de Calidad)
if st.session_state["auth"]:
    # Si estamos en sesión dual, mostramos un banner informativo flotante
    if st.session_state["admin_auth"]:
        st.markdown("<div class='card-hint'>⚙️ <b>MODO ESPEJO ACTIVO:</b> Estás visualizando la app como el usuario <code>{}</code>. Los cambios se sincronizan en caliente.</div>".format(st.session_state["token_actual"]), unsafe_allow_html=True)
        
    st.markdown("<div class='lab-panel' style='border-color: #00f2fe;'>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-header-custom'>🧬 Panel de Trabajo: {st.session_state['token_actual']}</div>", unsafe_allow_html=True)
    
    col_e1, col_e2, col_e3 = st.columns(3)
    col_e1.metric("Puntos Acumulados", f"{st.session_state['puntos_acumulados']} PTS")
    col_e2.metric("Sistemas Vitales (Vidas)", f"{st.session_state['vidas']} / 3")
    col_e3.metric("Racha Cuántica", f"{st.session_state['racha']}x")
    
    # Cronograma y selector de Estaciones de Trabajo
    estacion_actual = st.selectbox(
        "Seleccionar Estación de Simulación Autorizada:",
        ["Día 1: Introducción", "Día 2: Biomoléculas", "Día 3: Termodinámica", "Día 4: Equilibrio Ácido-Base"],
        index=["Día 1: Introducción", "Día 2: Biomoléculas", "Día 3: Termodinámica", "Día 4: Equilibrio Ácido-Base"].index(st.session_state["estacion"]) if st.session_state["estacion"] in ["Día 1: Introducción", "Día 2: Biomoléculas", "Día 3: Termodinámica", "Día 4: Equilibrio Ácido-Base"] else 0
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Funciones de guardado en SQLite del progreso del estudiante
    def sincronizar_progreso_db(token, puntos, intentos_sumar=0):
        conn = sqlite3.connect("mainlab_data.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE cupones SET modulo_maximo=?, puntos=?, intentos_quiz = intentos_quiz + ? WHERE token=?", 
                       (estacion_actual, puntos, intentos_sumar, token))
        conn.commit()
        conn.close()

    def descontar_vida_db(token):
        conn = sqlite3.connect("mainlab_data.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE cupones SET vidas = max(0, vidas - 1) WHERE token=?", (token,))
        conn.commit()
        conn.close()
    
    # Carga limpia y controlada de módulos dinámicos mediante el interceptor
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
        st.error(f"Detalle técnico de la anomalía: {e}")
        
    if st.button("Desconectarse del Ecosistema", use_container_width=True):
        st.session_state["auth"] = False
        st.session_state["token_actual"] = None
        st.rerun()
