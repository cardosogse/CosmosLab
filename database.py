import sqlite3
import datetime
from datetime import timedelta
import random
import string

# Cambiamos el nombre para romper el Write-Lock en Streamlit Cloud
DB_NAME = 'mainlab_pro_auth.db'

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso
                 (token TEXT PRIMARY KEY, 
                  fecha_expiracion DATE, 
                  en_uso BOOLEAN, 
                  identificador_usuario TEXT,
                  modulo_actual INTEGER DEFAULT 1,
                  score_puntos INTEGER DEFAULT 0,
                  vidas INTEGER DEFAULT 3)''')
    
    token_prueba = "SYNAPSIS-PRO-2026"
    fecha_futura = datetime.date.today() + timedelta(days=30)
    c.execute("INSERT OR IGNORE INTO tokens_acceso (token, fecha_expiracion, en_uso, identificador_usuario, modulo_actual, score_puntos, vidas) VALUES (?, ?, ?, ?, 1, 0, 3)", 
              (token_prueba, fecha_futura, False, "Admin"))
    conn.commit()
    conn.close()

def obtener_datos_usuario(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT score_puntos, vidas, modulo_actual FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    conn.close()
    return res if res else (0, 3, 1)

def obtener_todos_los_tokens():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT token, en_uso, fecha_expiracion, score_puntos, vidas, modulo_actual FROM tokens_acceso")
    rows = c.fetchall()
    conn.close()
    
    datos_procesados = []
    hoy = datetime.date.today()
    for row in rows:
        f_exp = datetime.datetime.strptime(row[2], "%Y-%m-%d").date()
        dias_restantes = max(0, (f_exp - hoy).days)
        datos_procesados.append([row[0], "Sí" if row[1] else "No", dias_restantes, row[3], row[4], row[5]])
    return datos_procesados if datos_procesados else rows

def listar_todos_los_tokens():
    return obtener_todos_los_tokens()

def sincronizar_progreso_db(token, puntos, modulo_comp):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET score_puntos = ?, modulo_actual = ? WHERE token = ?", (puntos, modulo_comp, token))
    conn.commit()
    conn.close()

def actualizar_modulo_db(token, modulo):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET modulo_actual = ? WHERE token = ?", (modulo, token))
    conn.commit()
    conn.close()

def otorgar_tiempo_extra_db(token, dias=7):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT fecha_expiracion FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    if res:
        fecha_act = datetime.datetime.strptime(res[0], "%Y-%m-%d").date()
        nueva_fecha = fecha_act + timedelta(days=dias)
        c.execute("UPDATE tokens_acceso SET fecha_expiracion = ? WHERE token = ?", (nueva_fecha.strftime("%Y-%m-%d"), token))
        conn.commit()
    conn.close()

def forzar_cancelacion_licencia(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    ayer = datetime.date.today() - timedelta(days=1)
    c.execute("UPDATE tokens_acceso SET fecha_expiracion = ? WHERE token = ?", (ayer.strftime("%Y-%m-%d"), token))
    conn.commit()
    conn.close()

def revocar_eliminar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def forzar_liberacion_sesion(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def liberar_token(token):
    forzar_liberacion_sesion(token)

def descontar_vida_db(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = max(0, vidas - 1) WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def restaurar_vida_db(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = min(3, vidas + 1) WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def generar_token(vigencia_dias):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    caracteres = string.ascii_uppercase + string.digits
    nuevo_tok = "MAINLAB-" + "".join(random.choice(caracteres) for _ in range(8))
    exp = datetime.date.today() + timedelta(days=vigencia_dias)
    c.execute("INSERT INTO tokens_acceso (token, fecha_expiracion, en_uso, identificador_usuario, modulo_actual, score_puntos, vidas) VALUES (?, ?, 0, 'Estudiante Autónomo', 1, 0, 3)", 
              (nuevo_tok, exp))
    conn.commit()
    conn.close()
    return nuevo_tok

def validar_token(token_ingresado):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT fecha_expiracion, en_uso FROM tokens_acceso WHERE token = ?", (token_ingresado.strip().upper(),))
    resultado = c.fetchone()
    
    if resultado:
        fecha_exp = datetime.datetime.strptime(resultado[0], "%Y-%m-%d").date()
        en_uso = resultado[1]
        if datetime.date.today() > fecha_exp:
            conn.close()
            return False, "El token ha expirado o fue cancelado por el administrador."
        if en_uso:
            conn.close()
            return False, "Acceso denegado: Token activo en otro dispositivo."
        
        c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token_ingresado.strip().upper(),))
        conn.commit()
        conn.close()
        return True, "Acceso concedido."
    conn.close()
    return False, "Token inexistente o inválido."
