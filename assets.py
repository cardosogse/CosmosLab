import streamlit as st

FONDO_FRACTAL_CSS = """
<style>
/* Fondo general con patrón geométrico sutil (Fractal/Red Celular) */
.stApp {
    background-color: #0f172a; /* Azul pizarra muy oscuro y elegante */
    background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 0l30 30-30 30L0 30z' stroke='rgba(30,41,59,0.6)' stroke-width='1' fill='none'/%3E%3Cpath d='M15 15l30 30M45 15L15 45' stroke='rgba(30,41,59,0.3)' stroke-width='1' fill='none'/%3E%3C/svg%3E");
    background-attachment: fixed;
    color: #e2e8f0;
}

/* Identidad MainLab */
.main-title {
    font-size: 3.5rem;
    font-weight: 800;
    color: #ffffff;
    text-align: center;
    margin-bottom: 0px;
    padding-bottom: 0px;
}
.main-title-suffix {
    color: #00e5ff; /* Cian tecnológico */
}
.sub-title {
    text-align: center;
    color: #94a3b8;
    font-size: 1.2rem;
    margin-top: -10px;
    margin-bottom: 30px;
}
</style>
"""

def cargar_estilos():
    """Inyecta el CSS directamente en la aplicación."""
    st.markdown(FONDO_FRACTAL_CSS, unsafe_allow_html=True)
