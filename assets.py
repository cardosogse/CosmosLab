import streamlit as st

# Estética Premium: Negro Absoluto + Fractal de Líneas Matemáticas + Paneles Traslúcidos
FONDO_FRACTAL_CSS = """
<style>
/* 1. Fondo Negro Absoluto con un Fractal Lineal Matemático sutil (Órbita de Atractor) */
.stApp {
    background-color: #000000; 
    background-image: url("data:image/svg+xml,%3Csvg width='200' height='200' viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M10 80 Q 52.5 10, 95 80 T 180 80' stroke='rgba(0, 229, 255, 0.04)' stroke-width='1' fill='none'/%3E%3Cpath d='M20 90 Q 62.5 20, 105 90 T 190 90' stroke='rgba(0, 229, 255, 0.02)' stroke-width='0.5' fill='none'/%3E%3Ccircle cx='100' cy='100' r='60' stroke='rgba(255,255,255,0.01)' stroke-width='1' fill='none'/%3E%3Ccircle cx='100' cy='100' r='30' stroke='rgba(0, 229, 255, 0.03)' stroke-width='0.5' fill='none'/%3E%3C/svg%3E");
    background-attachment: fixed;
    color: #f1f5f9;
}

/* 2. Paneles Traslúcidos de Alta Tecnología (Glassmorphism) */
.lab-panel {
    background: rgba(15, 23, 42, 0.45) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 16px !important;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

/* Tarjetas métricas traslúcidas */
.metric-card {
    background: rgba(30, 41, 59, 0.4) !important;
    backdrop-filter: blur(8px) !important;
    border-left: 4px solid #00e5ff !important;
    border-top: 1px solid rgba(255,255,255,0.05) !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
    padding: 14px;
    border-radius: 8px;
}

/* 3. Tipografías de la Marca MainLab */
.main-title {
    font-size: 4rem;
    font-weight: 900;
    color: #ffffff;
    text-align: center;
    margin-bottom: 0px;
    padding-bottom: 0px;
    letter-spacing: -2px;
    text-shadow: 0 0 20px rgba(0, 229, 255, 0.2);
}
.main-title-suffix {
    color: #00e5ff;
}
.sub-title {
    text-align: center;
    color: #475569;
    font-size: 1.1rem;
    margin-top: -5px;
    margin-bottom: 35px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Botones estilo terminal neon */
.stButton>button {
    background: rgba(0, 229, 255, 0.05) !important;
    color: #00e5ff !important;
    border: 1px solid rgba(0, 229, 255, 0.4) !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: rgba(0, 229, 255, 0.2) !important;
    border: 1px solid #00e5ff !important;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
}

/* Personalización de inputs para encajar en el modo oscuro */
input {
    background-color: rgba(15, 23, 42, 0.6) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}
</style>
"""

def cargar_estilos():
    """Inyecta el entorno estético oscuro y traslúcido."""
    st.markdown(FONDO_FRACTAL_CSS, unsafe_allow_html=True)
