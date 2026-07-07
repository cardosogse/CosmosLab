import sqlite3
import os

# Nueva identidad de la base de datos
DB_NAME = "mainlab_auth.db"

def inicializar_db():
    """Crea la base de datos y la tabla de usuarios si no existen."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso (
                    token TEXT PRIMARY KEY,
                    dias_restantes INTEGER,
                    puntos INTEGER DEFAULT 0,
                    vidas INTEGER DEFAULT 3,
                    dia_completado INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

def obtener_datos_usuario(token):
    """Extrae el progreso actual del alumno."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT puntos, vidas, dia_completado FROM tokens_acceso WHERE token = ?", (token,))
    row = c.fetchone()
    conn.close()
    return row

def sincronizar_progreso_db(token, puntos_ganados, dia_completado):
    """Guarda los puntos y avanza el candado del día."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Actualiza los puntos sumándolos y asegura que el dia_completado solo avance, no retroceda
    c.execute("""
        UPDATE tokens_acceso 
        SET puntos = puntos + ?, 
            dia_completado = MAX(dia_completado, ?) 
        WHERE token = ?
    """, (puntos_ganados, dia_completado, token))
    conn.commit()
    conn.close()

def descontar_vida_db(token):
    """Resta 1 vida celular en caso de fallo metabólico."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = MAX(0, vidas - 1) WHERE token = ?", (token,))
    conn.commit()
    conn.close()
