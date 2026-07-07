import sqlite3
import uuid

DB_NAME = "mainlab_auth.db"

def inicializar_db():
    """Crea la base de datos local y la tabla de control si no existen."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
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

# ========================================================
# CONSOLA DE ADMINISTRACIÓN DE TOKENS (SISTEMA MAESTRO)
# ========================================================

def generar_token(dias=30):
    """Genera un identificador alfanumérico único para un nuevo alumno."""
    nuevo_token = str(uuid.uuid4()).split('-')[0].upper()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tokens_acceso (token, dias_restantes) VALUES (?, ?)", (nuevo_token, dias))
    conn.commit()
    conn.close()
    return nuevo_token

def listar_todos_los_tokens():
    """Recupera la totalidad de los registros de la base de datos para el panel de control."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT token, en_uso, dias_restantes, puntos, vidas, dia_completado FROM tokens_acceso")
    filas = c.fetchall()
    conn.close()
    return filas

def revocar_eliminar_token(token):
    """Elimina permanentemente un token de la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token.strip().upper(),))
    conn.commit()
    conn.close()

def forzar_liberacion_sesion(token):
    """Resetea el estado de uso de un token si la sesión se quedó colgada en el servidor."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token.strip().upper(),))
    conn.commit()
    conn.close()

# ========================================================
# AUTENTICACIÓN Y FLUJO DEL ESTUDIANTE
# ========================================================

def validar_token(token):
    """Valida el token y bloquea accesos simultáneos en múltiples dispositivos."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT en_uso FROM tokens_acceso WHERE token = ?", (token.strip().upper(),))
    row = c.fetchone()
    if row:
        if row[0] == 0:
            c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token.strip().upper(),))
            conn.commit()
            conn.close()
            return True, "Acceso concedido"
        else:
            conn.close()
            return False, "El token ya está activo en otro dispositivo"
    conn.close()
    return False, "Token inválido o inexistente"

def liberar_token(token):
    """Libera el token al cerrar la sesión de forma voluntaria."""
    if token:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token.strip().upper(),))
        conn.commit()
        conn.close()

def obtener_datos_usuario(token):
    """Recupera el estado exacto de puntos, vidas y avance diario del alumno."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT puntos, vidas, dia_completado FROM tokens_acceso WHERE token = ?", (token.strip().upper(),))
    row = c.fetchone()
    conn.close()
    return row if row else (0, 3, 0)

# ========================================================
# MOTOR DE PERSISTENCIA JUEGO / APRENDIZAJE
# ========================================================

def sincronizar_progreso_db(token, puntos_ganados, dia_completado):
    """Guarda los puntos obtenidos y actualiza la bitácora de viaje."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE tokens_acceso 
        SET puntos = puntos + ?, 
            dia_completado = MAX(dia_completado, ?) 
        WHERE token = ?
    """, (puntos_ganados, dia_completado, token.strip().upper()))
    conn.commit()
    conn.close()

def descontar_vida_db(token):
    """Resta un punto de estabilidad celular al disco duro sin bajar de 0."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = MAX(0, vidas - 1) WHERE token = ?", (token.strip().upper(),))
    conn.commit()
    conn.close()

def restaurar_vida_db(token):
    """Suma un punto de estabilidad celular tras superar retos de rescate (Máximo 3)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = MIN(3, vidas + 1) WHERE token = ?", (token.strip().upper(),))
    conn.commit()
    conn.close()
