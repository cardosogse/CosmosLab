import sqlite3
import uuid

DB_NAME = "mainlab_auth.db"

def inicializar_db():
    """Crea la base de datos y la tabla de usuarios si no existen."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Tabla reforzada: Manejo de tokens + Gamificación
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso (
                    token TEXT PRIMARY KEY,
                    en_uso INTEGER DEFAULT 0,
                    dias_restantes INTEGER DEFAULT 30,
                    puntos INTEGER DEFAULT 0,
                    vidas INTEGER DEFAULT 3,
                    dia_completado INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

# ==========================================
# SISTEMA DE SEGURIDAD Y TOKENS (INTACTO)
# ==========================================
def generar_token(dias=30):
    """Genera un nuevo token alfanumérico para un alumno."""
    nuevo_token = str(uuid.uuid4()).split('-')[0].upper()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tokens_acceso (token, dias_restantes) VALUES (?, ?)", (nuevo_token, dias))
    conn.commit()
    conn.close()
    return nuevo_token

def validar_token(token):
    """Verifica si el token existe y si no está siendo usado en otro dispositivo."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT en_uso FROM tokens_acceso WHERE token = ?", (token,))
    row = c.fetchone()
    if row:
        if row[0] == 0:
            # Bloquea el token para que nadie más lo use al mismo tiempo
            c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token,))
            conn.commit()
            conn.close()
            return True, "Acceso concedido"
        else:
            conn.close()
            return False, "El token ya está en uso en otro dispositivo"
    conn.close()
    return False, "Token inválido o inexistente"

def liberar_token(token):
    """Libera el token cuando el alumno cierra sesión."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

# ==========================================
# SISTEMA DE GAMIFICACIÓN MAINLAB
# ==========================================
def obtener_datos_usuario(token):
    """Extrae el progreso actual del alumno al iniciar sesión."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT puntos, vidas, dia_completado FROM tokens_acceso WHERE token = ?", (token,))
    row = c.fetchone()
    conn.close()
    return row if row else (0, 3, 0)

def sincronizar_progreso_db(token, puntos_ganados, dia_completado):
    """Guarda los puntos y avanza el candado del día."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE tokens_acceso 
        SET puntos = puntos + ?, dia_completado = MAX(dia_completado, ?) 
        WHERE token = ?
    """, (puntos_ganados, dia_completado, token))
    conn.commit()
    conn.close()

def descontar_vida_db(token):
    """Resta 1 vida celular en caso de fallo metabólico (Mínimo 0)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = MAX(0, vidas - 1) WHERE token = ?", (token,))
    conn.commit()
    conn.close()
