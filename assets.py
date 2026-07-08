import streamlit as st
import random

def cargar_estilos():
    st.markdown("""
    <style>
        /* Fondo Universo: Negro Absoluto + Galaxias / Nebulosas de polvo cósmico */
        .stApp {
            background-color: #000000 !important;
            background-image: \
                radial-gradient(circle at 20% 30%, rgba(0, 229, 255, 0.05) 0%, transparent 45%), \
                radial-gradient(circle at 75% 70%, rgba(156, 39, 176, 0.06) 0%, transparent 50%), \
                radial-gradient(white 1px, transparent 1px), \
                radial-gradient(white 1.5px, transparent 1.5px);
            background-size: 100% 100%, 100% 100%, 250px 250px, 160px 150px;
            background-position: 0 0, 0 0, 0 0, 40px 60px;
            background-attachment: fixed;
        }
        .main-title { text-align: center; color: #ffffff; font-size: 3.8rem; font-weight: 800; margin-bottom: 0px; letter-spacing: 2px; text-shadow: 0 0 15px rgba(255,255,255,0.1); }
        
        /* Contenedores de Laboratorio Modulares (Glassmorphism Avanzado - Optimizado) */
        .lab-panel {
            background: rgba(13, 27, 42, 0.65) !important;
            backdrop-filter: blur(12px) saturate(180%);
            -webkit-backdrop-filter: blur(12px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.07) !important;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 15px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        
        /* Alertas Personalizadas */
        .card-hint {
            background: rgba(30, 41, 59, 0.7) !important;
            border-left: 4px solid #38bdf8 !important;
            padding: 12px;
            border-radius: 4px;
            margin: 10px 0;
            color: #e2e8f0;
        }
        
        /* Estilos globales de texto */
        h1, h2, h3, p, span, label { font-family: 'Inter', sans-serif !important; }
    </style>
    """, unsafe_allow_html=True)

# Base de Datos de Elementos para el Simulador
ELEMENTOS = {
    "H": {"nombre": "Hidrógeno", "z": 1, "m": 1.008, "color": "#ffffff", "grupo": "No metales"},
    "C": {"nombre": "Carbono", "z": 6, "m": 12.011, "color": "#90a4ae", "grupo": "No metales"},
    "N": {"nombre": "Nitrógeno", "z": 7, "m": 14.007, "color": "#2196f3", "grupo": "No metales"},
    "O": {"nombre": "Oxígeno", "z": 8, "m": 15.999, "color": "#f44336", "grupo": "No metales"},
    "Na": {"nombre": "Sodio", "z": 11, "m": 22.990, "color": "#9c27b0", "grupo": "Metales alcalinos"},
    "Cl": {"nombre": "Cloro", "z": 17, "m": 35.45, "color": "#4caf50", "grupo": "Halógenos"}
}

def mezclar_memorama():
    conceptos = [
        ("Centrifugación", 1), ("Separación por densidad", 1),
        ("Capa de Valencia", 2), ("Electrones externos", 2),
        ("Enlace Covalente", 3), ("Compartición de electrones", 3),
        ("Efecto Amortiguador", 4), ("Resistencia al cambio de pH", 4),
        ("Solución Coloidal", 5), ("Plasma Sanguíneo", 5)
    ]
    random.shuffle(conceptos)
    return conceptos

def generar_svg_enlace(sym1, sym2, val1, val2, diff):
    # Paleta dinámica
    c1 = ELEMENTOS.get(sym1, {"color": "#00e5ff"})["color"]
    c2 = ELEMENTOS.get(sym2, {"color": "#ff007f"})["color"]
    f1, f2 = float(val1), float(val2)
    
    # Lógica de distribución espacial electrónica
    if diff > 1.7: cx_e1, cx_e2, ellipse_x, stroke_color, stroke_dash = 113, 127, 120, "#ffffff", "2 2"
    elif diff > 0.4: cx_e1, cx_e2, ellipse_x, stroke_color, stroke_dash = (85, 95, 100, c1, "4 2") if f1 > f2 else (145, 155, 140, c2, "4 2")
    else: cx_e1, cx_e2, ellipse_x, stroke_color, stroke_dash = 105, 135, 120, "#b0bec5", "3 3"
    
    return f"""<div style='display:flex; justify-content:center; align-items:center; width:100%; height:130px;'><svg viewBox='0 0 240 120' width='100%' height='100%'><circle cx='70' cy='60' r='22' fill='{c1}' opacity='0.85'/><text x='64' y='65' fill='black' font-weight='bold' font-size='14'>{sym1}</text><circle cx='170' cy='60' r='18' fill='{c2}' opacity='0.85'/><text x='164' y='64' fill='black' font-weight='bold' font-size='12'>{sym2}</text><ellipse cx='{ellipse_x}' cy='60' rx='28' ry='12' fill='none' stroke='{stroke_color}' stroke-width='1.5' stroke-dasharray='{stroke_dash}'/><circle cx='{cx_e1}' cy='55' r='3.5' fill='#00ffcc'/><circle cx='{cx_e2}' cy='65' r='3.5' fill='#00ffcc'/></svg></div>"""
