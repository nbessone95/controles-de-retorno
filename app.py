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
    st.header("✍️ Completar Control")
    
    files = [f for f in os.listdir("templates") if f.endswith(".xlsx")]
    
    if not files:
        st.warning("No hay plantillas. Sube una primero.")
    else:
        if 'selected_file' not in st.session_state:
            st.session_state.selected_file = None
            
        col_select, col_btn = st.columns([3,1])
        with col_select:
            selected = st.selectbox("Seleccionar archivo a completar", files, 
                                  index=files.index(st.session_state.selected_file) if st.session_state.selected_file in files else 0)
        
        with col_btn:
            if st.button("Cargar y Leer Datos del Excel", type="primary"):
                st.session_state.selected_file = selected
                st.rerun()
        
        if st.session_state.selected_file:
            filepath = f"templates/{st.session_state.selected_file}"
            st.success(f"Trabajando con: **{st.session_state.selected_file}**")
            
            # ==================== LECTURA DEL EXCEL (con error seguro) ====================
            despacho_2500 = despacho_2000 = despacho_1250 = 0
            try:
                wb = load_workbook(filepath, data_only=True)
                ws = wb.active  # Usamos la hoja activa por seguridad
                
                # Intentamos leer las celdas comunes
                despacho_2500 = ws.cell(row=5, column=1).value or 0
                despacho_2000 = ws.cell(row=8, column=1).value or 0
                despacho_1250 = ws.cell(row=11, column=1).value or 0
                
                st.success("✅ Datos del Excel leídos correctamente")
            except Exception as e:
                st.error(f"Error al leer Excel: {str(e)}")
                st.info("Se usarán valores en 0. Puedes completarlos manualmente.")

            # ==================== HOJA 1 - SOLO LECTURA ====================
            st.subheader("📦 1. CONTROL DE RETORNOS DE ENVASES")
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write("**DESPACHO (no modificable)**")
                st.metric("2500", despacho_2500)
                st.metric("2000", despacho_2000)
                st.metric("1250", despacho_1250)
            
            with col2:
                st.write("**RETORNOS (completar)**")
                c1, c2, c3 = st.columns(3)
                with c1:
                    ret_2500 = st.number_input("Retorno 2500", value=0)
                    ret_2000 = st.number_input("Retorno 2000", value=0)
                with c2:
                    ret_1250 = st.number_input("Retorno 1250", value=0)
                    pallets = st.number_input("Pallets", value=0)
                with c3:
                    chapas = st.number_input("Chapas", value=0)
                    clientes = st.number_input("Cantidad de Clientes", value=17)

            total_vacios = st.number_input("**TOTAL VACÍOS RETORNADOS**", value=0)

            # Hoja 2
            st.subheader("📋 2. Retorno Llenos")
            rl1, rl2 = st.columns(2)
            with rl1:
                lleno_2500 = st.number_input("Retorno Lleno 2500", value=0)
                lleno_2000 = st.number_input("Retorno Lleno 2000", value=0)
            with rl2:
                lleno_1250 = st.number_input("Retorno Lleno 1250", value=0)
                venta_envases = st.number_input("Venta de Envases", value=0)

            merc
