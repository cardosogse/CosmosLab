import streamlit as st

FONDO_FRACTAL_CSS = """
<style>
/* Lienzo de fondo: Patrón geométrico fractal sutil de bajo contraste */
.stApp {
    background-color: #0f172a; 
    background-image: url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M40 0l40 40-40 40L0 40z' stroke='rgba(30,41,59,0.5)' stroke-width='1' fill='none'/%3E%3Cpath d='M20 20l40 40M60 20L20 60' stroke='rgba(30,41,59,0.2)' stroke-width='1' fill='none'/%3E%3C/svg%3E");
    background-attachment: fixed;
    color: #e2e8f0;
}

/* Tipografías e Identidad de Marca */
.main-title {
    font-size: 3.8rem;
    font-weight: 900;
    color: #ffffff;
    text-align: center;
    margin-bottom: 0px;
    padding-bottom: 0px;
    letter-spacing: -1px;
}
.main-title-suffix {
    color: #00e5ff; 
}
.sub-title {
    text-align: center;
    color: #64748b;
    font-size: 1.2rem;
    margin-top: -5px;
    margin-bottom: 25px;
}

/* Paneles de Laboratorio */
.lab-panel {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
}
.metric-card {
    background-color: #1e293b;
    border-left: 4px solid #00e5ff;
    padding: 12px;
    border-radius: 6px;
}
</style>
"""

def cargar_estilos():
    """Inyecta el código CSS en la aplicación de Streamlit."""
    st.markdown(FONDO_FRACTAL_CSS, unsafe_allow_html=True)
