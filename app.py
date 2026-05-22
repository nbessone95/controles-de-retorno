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
        st.rerun()

elif menu == "Completar Formulario":
    st.header("✍️ Completar Control")
    
    files = [f for f in os.listdir("templates") if f.endswith(".xlsx")]
    
    if not files:
        st.warning("No hay plantillas. Sube una primero.")
    else:
        if 'selected_file' not in st.session_state:
            st.session_state.selected_file = files[0] if files else None
            
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
            
            # Lectura del Excel
            equipo = "Alessandrini / Rosso / Baldoncini"
            desp_2500 = desp_2000 = desp_1250 = total_desp = 0
            try:
                wb = load_workbook(filepath, data_only=True)
                
                # Leer equipo desde Hoja 2
                if "Hoja2" in wb.sheetnames:
                    ws2 = wb["Hoja2"]
                    equipo = ws2.cell(row=2, column=2).value or equipo
                
                # Leer despachos desde Hoja 3 (Columna B)
                ws3 = wb["Hoja3"] if "Hoja3" in wb.sheetnames else wb.active
                desp_2500 = ws3.cell(row=5, column=2).value or 0
                desp_2000 = ws3.cell(row=8, column=2).value or 0
                desp_1250 = ws3.cell(row=11, column=2).value or 0
                total_desp = ws3.cell(row=24, column=5).value or (desp_2500 + desp_2000 + desp_1250)
            except:
                pass

            # ==================== HOJA 1 ====================
            st.subheader("1. CONTROL DE RETORNOS DE ENVASES")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Localidad", "Rio Segundo")
                st.metric("Equipo", equipo)
                st.metric("Camión", "AD")
                st.metric("Fecha", datetime.today().strftime("%d-%m-%Y"))
            
            with col2:
                st.metric("Cantidad 2500", desp_2500)
                st.metric("Cantidad 2000", desp_2000)
                st.metric("Cantidad 1250", desp_1250)
                st.metric("**TOTAL DESPACHADO**", total_desp)

            st.subheader("Datos Fijos (no modificables)")
            st.metric("Cantidad de Clientes", 17)
            st.metric("Pallets", 0)
            st.metric("Chapas", 0)

            # ==================== HOJA 2 ====================
            st.subheader("2. Retornos y Cambios (Completar)")
            
            st.write("**Retornos**")
            r1, r2 = st.columns(2)
            with r1:
                ret_2500 = st.number_input("Retorno 2500", value=0)
                ret_2000 = st.number_input("Retorno 2000", value=0)
            with r2:
                ret_1250 = st.number_input("Retorno 1250", value=0)

            st.write("**Cambios**")
            c1, c2, c3 = st.columns(3)
            with c1:
                cam_2500 = st.number_input("Cambio 2500", value=0)
                cam_2000 = st.number_input("Cambio 2000", value=0)
            with c2:
                cam_1250 = st.number_input("Cambio 1250", value=0)
                cam_354 = st.number_input("Cambio 354", value=0)
            with c3:
                cam_220
