import streamlit as st
from datetime import datetime
import os
import pandas as pd
from PIL import Image
from openpyxl import load_workbook

st.set_page_config(page_title="Control Retornos", layout="wide")
st.title("🧾 Control de Retornos - Rio Segundo")
st.caption("Equipo: Alessandrini / Rosso / Baldoncini")

os.makedirs("templates", exist_ok=True)
os.makedirs("completed", exist_ok=True)
os.makedirs("data", exist_ok=True)

menu = st.sidebar.selectbox("Menú", ["Completar Formulario", "Subir Plantillas", "Historial"])

if menu == "Subir Plantillas":
    st.header("📤 Subir Plantillas del Día")
    uploaded = st.file_uploader("Subir uno o varios Excels", type="xlsx", accept_multiple_files=True)
    if uploaded:
        for file in uploaded:
            with open(f"templates/{file.name}", "wb") as f:
                f.write(file.getbuffer())
            st.success(f"✅ {file.name} guardado")

elif menu == "Completar Formulario":
    st.header("✍️ Completar Control Completo")
    
    files = [f for f in os.listdir("templates") if f.endswith(".xlsx")]
    
    if not files:
        st.warning("No hay plantillas. Sube una primero.")
    else:
        if 'selected_file' not in st.session_state:
            st.session_state.selected_file = None
            
        col_select, col_btn = st.columns([3,1])
        with col_select:
            selected = st.selectbox("Seleccionar archivo", files, 
                                  index=files.index(st.session_state.selected_file) if st.session_state.selected_file in files else
