import streamlit as st
import random

def inyectar_css():
    st.markdown("""
    <style>
        .stApp {
            background-color: #000000 !important;
            background-image: 
                radial-gradient(white 1px, transparent 1px),
                radial-gradient(white 1px, transparent 1px);
            background-size: 250px 250px, 150px 150px;
            background-position: 0 0, 30px 40px;
        }
        .main-title { text-align: center; color: #ffffff; font-size: 3.8rem; font-weight: 800; margin-bottom: 0px; letter-spacing: 2px;}
        .main-title-suffix { color: #00e5ff; font-weight: 300; }
        .sub-title { text-align: center; font-style: italic; color: #90a4ae; font-size: 1.2rem; margin-top: 5px; margin-bottom: 30px; }
        .bio-panel { background-color: rgba(30, 41, 59, 0.6); border-left: 5px solid #00e5ff; padding: 20px; border-radius: 8px; margin-bottom: 20px; backdrop-filter: blur(5px);}
        .card-success { background-color: rgba(76, 175, 80, 0.1); border-left: 5px solid #4caf50; padding: 15px; border-radius: 5px; margin-top: 10px; }
        .card-error { background-color: rgba(244, 67, 54, 0.1); border-left: 5px solid #f44336; padding: 15px; border-radius: 5px; margin-top: 10px; }
        .card-hint { background-color: rgba(255, 177, 66, 0.1); border-left: 5px solid #ffb142; padding: 15px; border-radius: 5px; margin-top: 10px; color: #ffda79;}
        .monitor-box { background-color: rgba(255,255,255,0.05); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px;}
        
        .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
        .stTabs [data-baseweb="tab"] { background-color: rgba(255,255,255,0.05); border-radius: 4px 4px 0 0; padding: 10px 20px; color: #90a4ae; font-weight: bold; cursor: pointer !important;}
        .stTabs [aria-selected="true"] { background-color: rgba(0, 229, 255, 0.15) !important; color: #00e5ff !important; border-bottom: 2px solid #00e5ff !important; }
        
        div[data-testid="stRadio"] > div{
            flex-direction: row !important;
            gap: 12px !important;
            flex-wrap: wrap;
        }
        div[data-testid="stRadio"] label {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            padding: 10px 18px !important;
            border-radius: 20px !important;
            color: #cfd8dc !important;
            transition: all 0.2s ease-in-out !important;
            cursor: pointer !important;
        }
        div[data-testid="stRadio"] label:hover {
            background-color: rgba(0, 229, 255, 0.08) !important;
            border-color: #00e5ff !important;
            color: #ffffff !important;
        }
        div[data-testid="stRadio"] label[data-checked="true"] {
            background-color: rgba(0, 229, 255, 0.18) !important;
            border-color: #00e5ff !important;
            color: #00e5ff !important;
            font-weight: bold !important;
        }
        div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"]-prefix {
            display: none !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }

        div[data-testid="stSlider"] {
            cursor: pointer !important;
        }
        div[data-testid="stSlider"] [role="slider"] {
            cursor: grab !important;
        }
        div[data-testid="stSlider"] [role="slider"]:active {
            cursor: grabbing !important;
        }

        div[data-testid="stElementToolbar"] + div div[data-baseweb="slider-track"] > div {
            background: linear-gradient(to right, #00e5ff, #00e5ff) !important;
        }
        div[data-testid="stElementToolbar"] + div [role="slider"] {
            background-color: #00e5ff !important;
            box-shadow: 0 0 8px #00e5ff !important;
        }

        @keyframes parpadeoPulso {
            0% { opacity: 0.3; text-shadow: 0 0 0px transparent; }
            50% { opacity: 1; text-shadow: 0 0 8px #ffb142; }
            100% { opacity: 0.3; text-shadow: 0 0 0px transparent; }
        }
        .foco-parpadeante {
            animation: parpadeoPulso 2.5s infinite ease-in-out;
            color: #ffb142;
            font-weight: bold;
            display: inline-block;
        }

        .card-dalton { background-color: rgba(144, 164, 174, 0.08); border: 1px solid rgba(144, 164, 174, 0.3); border-left: 5px solid #90a4ae; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
        .card-thomson { background-color: rgba(156, 39, 176, 0.08); border: 1px solid rgba(156, 39, 176, 0.3); border-left: 5px solid #9c27b0; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
        .card-rutherford { background-color: rgba(33, 150, 243, 0.08); border: 1px solid rgba(33, 150, 243, 0.3); border-left: 5px solid #2196f3; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
        .card-bohr { background-color: rgba(255, 177, 66, 0.08); border: 1px solid rgba(255, 177, 66, 0.3); border-left: 5px solid #ffb142; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
        .card-schrodinger { background-color: rgba(0, 229, 255, 0.08); border: 1px solid rgba(0, 229, 255, 0.3); border-left: 5px solid #00e5ff; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

def obtener_svg_atomo(modelo_nombre):
    if "Dalton" in modelo_nombre:
        return """
        <svg viewBox="0 0 100 100" width="90" height="90">
            <circle cx="50" cy="50" r="34" fill="none" stroke="#90a4ae" stroke-width="2.5"/>
            <circle cx="50" cy="50" r="31" fill="#90a4ae" opacity="0.15"/>
        </svg>
        """
    elif "Thomson" in modelo_nombre:
        return """
        <svg viewBox="0 0 100 100" width="90" height="90">
            <circle cx="50" cy="50" r="34" fill="#9c27b0" opacity="0.15" stroke="#9c27b0" stroke-width="1.5"/>
            <circle cx="34" cy="38" r="4" fill="#ffffff"/><text x="32" y="41" fill="black" font-size="9" font-weight="bold">-</text>
            <circle cx="66" cy="42" r="4" fill="#ffffff"/><text x="64" y="45" fill="black" font-size="9" font-weight="bold">-</text>
            <circle cx="48" cy="68" r="4" fill="#ffffff"/><text x="46" y="71" fill="black" font-size="9" font-weight="bold">-</text>
            <text x="45" y="54" fill="#9c27b0" font-size="14" font-weight="bold">+</text>
        </svg>
        """
    elif "Rutherford" in modelo_nombre:
        return """
        <svg viewBox="0 0 100 100" width="90" height="90">
            <circle cx="50" cy="50" r="6" fill="#2196f3"/>
            <text x="47" y="54" fill="white" font-size="9" font-weight="bold">+</text>
            <ellipse cx="50" cy="50" rx="38" ry="10" fill="none" stroke="#2196f3" stroke-width="1" opacity="0.6" transform="rotate(30 50 50)"/>
            <ellipse cx="50" cy="50" rx="38" ry="10" fill="none" stroke="#2196f3" stroke-width="1" opacity="0.6" transform="rotate(-30 50 50)"/>
            <circle cx="22" cy="34" r="2.5" fill="#ffffff"/>
            <circle cx="78" cy="66" r="2.5" fill="#ffffff"/>
        </svg>
        """
    elif "Bohr" in modelo_nombre:
        return """
        <svg viewBox="0 0 100 100" width="90" height="90">
            <circle cx="50" cy="50" r="7" fill="#ffb142"/>
            <circle cx="50" cy="50" r="20" fill="none" stroke="#ffb142" stroke-width="1" stroke-dasharray="2 2"/>
            <circle cx="50" cy="50" r="36" fill="none" stroke="#ffb142" stroke-width="1"/>
            <circle cx="50" cy="14" r="3" fill="#ffffff"/>
            <circle cx="68" cy="38" r="3" fill="#ffffff"/>
        </svg>
        """
    else:
        return """
        <svg viewBox="0 0 100 100" width="90" height="90">
            <defs>
                <radialGradient id="cloud" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.8"/>
                    <stop offset="50%" stop-color="#00e5ff" stop-opacity="0.25"/>
                    <stop offset="100%" stop-color="#00e5ff" stop-opacity="0"/>
                </radialGradient>
            </defs>
            <circle cx="50" cy="50" r="38" fill="url(#cloud)"/>
            <circle cx="50" cy="50" r="4" fill="#ffffff"/>
        </svg>
        """

ELEMENTOS = {
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "sym": "C"},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "sym": "H"},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "sym": "O"},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "sym": "N"},
    "Fósforo (P)": {"fuerza": 2.19, "color": "#ff7ff5", "sym": "P"},
    "Azufre (S)": {"fuerza": 2.58, "color": "#ffda79", "sym": "S"}
}

@st.cache_data
def generar_svg_tira_afloja(f1, c1, sym1, f2, c2, sym2):
    diff = abs(f1 - f2)
    if f1 == f2:
        cx_e = 120
        ellipse_w = 40
        stroke_color = "#ffffff"
    elif f1 > f2:
        cx_e = 80 + (1.0 / diff) * 5 if diff > 0 else 80
        ellipse_w = 55
        stroke_color = c1
    else:
        cx_e = 160 - (1.0 / diff) * 5 if diff > 0 else 160
        ellipse_w = 55
        stroke_color = c2

    return f"""
    <div style='display:flex; justify-content:center; align-items:center; width:100%; height:120px;'>
        <svg viewBox="0 0 240 100" width="100%" height="100%">
            <line x1="60" y1="50" x2="180" y2="50" stroke="#555" stroke-width="2" stroke-dasharray="4 4"/>
            <circle cx="60" cy="50" r="22" fill="{c1}" opacity="0.85"/>
            <text x="54" y="55" fill="black" font-weight="bold" font-family="sans-serif" font-size="14">{sym1}</text>
            <text x="48" y="85" fill="#cfd8dc" font-family="sans-serif" font-size="11">Electronegatividad: {f1}</text>
            
            <circle cx="180" cy="50" r="22" fill="{c2}" opacity="0.85"/>
            <text x="174" y="55" fill="black" font-weight="bold" font-family="sans-serif" font-size="14">{sym2}</text>
            <text x="168" y="85" fill="#cfd8dc" font-family="sans-serif" font-size="11">Electronegatividad: {f2}</text>
            
            <ellipse cx="{cx_e}" cy="50" rx="{ellipse_w}" ry="28" fill="none" stroke="{stroke_color}" stroke-width="1.8" stroke-dasharray="3 1"/>
            <circle cx="{cx_e}" cy="50" r="6" fill="#00e5ff"/>
        </svg>
    </div>
    """

@st.cache_data
def generar_svg_enlace(sym1, f1, c1, sym2, f2, c2):
    diff = abs(f1 - f2)
    if diff == 0:
        cx_e1, cx_e2 = 113, 127
        ellipse_x, ellipse_w = 120, 65
        stroke_color = "#ffffff"
        stroke_dash = "2 2"
    elif diff > 0.4:
        cx_e1, cx_e2 = (85, 95) if f1 > f2 else (145, 155)
        ellipse_x, ellipse_w = (100, 70) if f1 > f2 else (140, 70)
        stroke_color = c1 if f1 > f2 else c2
        stroke_dash = "4 2"
    else:
        cx_e1, cx_e2 = (105, 135)
        ellipse_x, ellipse_w = (120, 68)
        stroke_color = "#b0bec5"
        stroke_dash = "3 3"

    return f"""
    <div style='display:flex; justify-content:center; align-items:center; width:100%; height:130px;'>
        <svg viewBox="0 0 240 120" width="100%" height="100%">
            <circle cx="70" cy="60" r="22" fill="{c1}" opacity="0.85"/>
            <text x="64" y="65" fill="black" font-weight="bold" font-family="sans-serif" font-size="14">{sym1}</text>
            <circle cx="170" cy="60" r="18" fill="{c2}" opacity="0.85"/>
            <text x="164" y="64" fill="black" font-weight="bold" font-family="sans-serif" font-size="12">{sym2}</text>
            <ellipse cx="{ellipse_x}" cy="60" rx="{ellipse_w}" ry="32" fill="none" stroke="{stroke_color}" stroke-width="1.5" stroke-dasharray="{stroke_dash}"/>
            <circle cx="{cx_e1}" cy="60" r="4" fill="#ffffff"/>
            <circle cx="{cx_e2}" cy="60" r="4" fill="#ffffff"/>
        </svg>
    </div>
    """

def mezclar_memorama():
    contenido = [
        ("Dalton (1810)", 1), ("Materia indivisible sin cargas", 1),
        ("Thomson (1897)", 2), ("Esfera positiva con electrones incrustados", 2),
        ("Rutherford (1911)", 3), ("Núcleo denso positivo y espacio vacío", 3),
        ("Bohr (1913)", 4), ("Órbitas circulares planas cuantizadas", 4),
        ("Schrödinger (1926)", 5), ("Orbitales 3D (Flexibilidad cuántica)", 5)
    ]
    random.shuffle(contenido)
    return contenido
