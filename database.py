import sqlite3
import datetime
from datetime import timedelta

DB_NAME = 'synapsis_auth.db'

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
                  memo_completado INTEGER DEFAULT 0)''')
    
    token_prueba = "SYNAPSIS-PRO-2026"
    fecha_futura = datetime.date.today() + timedelta(days=30)
    c.execute("INSERT OR IGNORE INTO tokens_acceso (token, fecha_expiracion, en_uso, identificador_usuario, modulo_actual, score_puntos, memo_completado) VALUES (?, ?, ?, ?, 1, 0, 0)", 
              (token_prueba, fecha_futura, False, "Admin"))
    conn.commit()
    conn.close()

def obtener_datos_usuario(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT score_puntos, memo_completado FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    conn.close()
    return res if res else (0, 0)

def obtener_todos_los_tokens():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT token, fecha_expiracion, en_uso, identificador_usuario, score_puntos, memo_completado FROM tokens_acceso")
    res = c.fetchall()
    conn.close()
    return res

def sincronizar_progreso_db(token, puntos, memo_comp):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET score_puntos = ?, memo_completado = ? WHERE token = ?", (puntos, memo_comp, token))
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

def eliminar_registro_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def validar_y_bloquear_token(token_ingresado):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT fecha_expiracion, en_uso FROM tokens_acceso WHERE token = ?", (token_ingresado,))
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
        
        c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token_ingresado,))
        conn.commit()
        conn.close()
        return True, "Acceso concedido."
    conn.close()
    return False, "Token inexistente o inválido."

def liberar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def registrar_nuevo_usuario(token, dias_duracion, identificador="Nuevo Estudiante"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    exp = datetime.date.today() + timedelta(days=dias_duracion)
    try:
        c.execute("INSERT INTO tokens_acceso (token, fecha_expiracion, en_uso, identificador_usuario, modulo_actual, score_puntos, memo_completado) VALUES (?, ?, ?, ?, 1, 0, 0)", 
                  (token.upper(), exp, False, identificador))
        conn.commit()
        mensaje = f"Token {token} registrado con éxito hasta {exp}"
    except sqlite3.IntegrityError:
        mensaje = f"Error: El token ya existe en el servidor."
    conn.close()
    return mensaje
