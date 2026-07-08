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
            estado TEXT DEFAULT 'Activo'
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Inicialización de estados de sesión originales
if "auth" not in st.session_state: st.session_state["auth"] = False
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
# 1. INYECCIÓN DE ESTILOS E ANIMACIÓN NEÓN
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #0d1117 0%, #07090e 100%);
        font-family: 'Inter', sans-serif;
        color: #c9d1d9;
    }
    
    /* Animación Radiactiva del Logo 'Lab' (Preservada) */
    @keyframes pulso-radiactivo {
        0% { text-shadow: 0 0 4px #00f2fe, 0 0 8px #00f2fe; color: #00f2fe; }
        50% { text-shadow: 0 0 16px #4facfe, 0 0 25px #00f2fe, 0 0 30px #4facfe; color: #ffffff; }
        100% { text-shadow: 0 0 4px #00f2fe, 0 0 8px #00f2fe; color: #00f2fe; }
    }
    .brand-main { font-family: 'Orbitron', sans-serif; font-size: 3.2rem; font-weight: 700; color: #ffffff; text-align: center; margin-bottom: 0px; }
    .brand-lab { animation: pulso-radiactivo 3s infinite ease-in-out; }
    
    .sub-title { font-size: 1.15rem; color: #8b949e; text-align: center; margin-top: 5px; margin-bottom: 30px; font-weight: 300; }
</style>
""", unsafe_allow_html=True)

# Encabezado con efecto Neón
st.markdown("<h1 class='brand-main'>Main<span class='brand-lab'>Lab</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Bioquímica aplicada. Ciencia interactiva. Sin límites.</p>", unsafe_allow_html=True)

# ==========================================
# 2. PESTAÑAS DE NAVEGACIÓN ORIGINALES
# ==========================================
pestaña = st.sidebar.radio("Seleccionar Entorno:", ["Portal del Estudiante", "Consola del Administrador"])

# ------------------------------------------
# ENTORNO: CONSOLA DEL ADMINISTRADOR (ORIGINAL)
# ------------------------------------------
if pestaña == "Consola del Administrador":
    st.header("🔑 Autenticación de Seguridad del Administrador")
    pass_admin = st.text_input("Contraseña de Infraestructura:", type="password")
    
    if pass_admin == "admin123": # Reemplaza por tu contraseña original si era diferente
        st.success("Acceso exclusivo concedido al Administrador.")
        
        st.subheader("🛠️ Generación de Cupones de Acceso")
        dias = st.number_input("Días de vigencia:", min_value=1, max_value=365, value=30)
        
        if st.button("Generar Nuevo Token"):
            # Formato de token largo de la versión base original
            nuevo_token = "MAINLAB-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            fecha_c = datetime.now().strftime("%Y-%m-%d")
            
            conn = sqlite3.connect("mainlab_data.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO cupones (token, fecha_creacion, vigencia_dias) VALUES (?, ?, ?)",
                           (nuevo_token, fecha_c, dias))
            conn.commit()
            conn.close()
            st.success(f"Token Creado Exitosamente: `{nuevo_token}`")
            
        st.subheader("📋 Matriz de Monitoreo de Actividad (Tablero Tipo Excel)")
        conn = sqlite3.connect("mainlab_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT token, modulo_maximo, puntos, vidas, racha, ultima_conexion, vigencia_dias, fecha_creacion, estado FROM cupones")
        filas = cursor.fetchall()
        conn.close()
        
        if filas:
            import pandas as pd
            # Reconstrucción exacta de la matriz de datos tipo Excel original
            df = pd.DataFrame(filas, columns=[
                "Token / Cupón", "Módulo Máximo", "Puntos Acumulados", 
                "Vidas Restantes", "Racha Actual", "Última Conexión", 
                "Vigencia (Días)", "Fecha Creación", "Estado"
            ])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay registros de tokens en la base de datos actual.")
            
    elif pass_admin:
        st.error("Credencial de infraestructura incorrecta.")

# ------------------------------------------
# ENTORNO: PORTAL DEL ESTUDIANTE (ORIGINAL)
# ------------------------------------------
else:
    if not st.session_state["auth"]:
        st.header("🔒 Acceso a Estaciones de Trabajo")
        input_token = st.text_input("Introduce tu Cupón de Acceso:", type="password").strip()
        
        if st.button("Autenticar e Ingresar"):
            if input_token:
                datos = validar_token_db(input_token)
                if datos:
                    st.session_state["auth"] = True
                    st.session_state["token_actual"] = input_token
                    st.session_state["estacion"] = datos[0] if datos[0] != 'Ninguno' else "Día 1: Introducción"
                    st.session_state["puntos_acumulados"] = datos[1]
                    st.session_state["vidas"] = datos[2]
                    st.session_state["racha"] = datos[3]
                    actualizar_conexion_db(input_token)
                    st.success("Acceso autorizado al laboratorio.")
                    st.rerun()
                else:
                    st.error("El cupón ingresado no es válido o ha expirado.")
            else:
                st.warning("Por favor, introduce un token.")
                
    else:
        st.subheader(f"🧬 Panel Estudiantil • Usuario: `{st.session_state['token_actual']}`")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Puntos", f"{st.session_state['puntos_acumulados']} PTS")
        col2.metric("Sistemas Vitales (Vidas)", f"{st.session_state['vidas']} / 3")
        col3.metric("Racha Activa", f"{st.session_state['racha']}x")
        
        st.session_state["estacion"] = st.selectbox(
            "Seleccionar Estación de Trabajo:",
            ["Día 1: Introducción", "Día 2: Biomoléculas", "Día 3: Termodinámica", "Día 4: Equilibrio Ácido-Base"],
            index=["Día 1: Introducción", "Día 2: Biomoléculas", "Día 3: Termodinámica", "Día 4: Equilibrio Ácido-Base"].index(st.session_state["estacion"]) if st.session_state["estacion"] in ["Día 1: Introducción", "Día 2: Biomoléculas", "Día 3: Termodinámica", "Día 4: Equilibrio Ácido-Base"] else 0
        )
        
        # Carga del contenido de los módulos originales
        estacion_actual = st.session_state["estacion"]
        if "Día 1" in estacion_actual:
            st.info("Módulo 1: Conceptos introductorios e instrumental analítico.")
        elif "Día 2" in estacion_actual:
            st.info("Módulo 2: Interacciones estereoquímicas macromoleculares.")
        elif "Día 3" in estacion_actual:
            st.info("Módulo 3: Entropía y bioenergética del enlace celular.")
        elif "Día 4" in estacion_actual:
            try:
                from modulos.m1_dia4 import mostrar_dia4
                mostrar_dia4()
            except Exception as e:
                st.error(f"Error al cargar la estación: {e}")
                
        if st.button("Cerrar Sesión del Laboratorio", type="primary"):
            st.session_state["auth"] = False
            st.session_state["token_actual"] = None
            st.rerun()
