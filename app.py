import streamlit as st
from datetime import datetime
import os
import pandas as pd
from openpyxl import load_workbook

st.set_page_config(page_title="Control Retornos", layout="wide")
st.title("🧾 Controles de Retornos ")

os.makedirs("templates", exist_ok=True)
os.makedirs("data", exist_ok=True)

menu = st.sidebar.selectbox("Menú", ["Completar Formulario", "Subir Plantillas", "Historial"])

if menu == "Subir Plantillas":
    st.header("📤 Subir Plantillas del Día")
    uploaded = st.file_uploader("Subir uno o varios Excels", type="xlsx", accept_multiple_files=True)
    if uploaded:
        with st.spinner("Guardando..."):
            for file in uploaded:
                with open(f"templates/{file.name}", "wb") as f:
                    f.write(file.getbuffer())
                st.success(f"✅ {file.name} guardado")
        st.rerun()

elif menu == "Completar Formulario":
    st.header("✍️ Completar Control")
    
    files = [f for f in os.listdir("templates") if f.endswith(".xlsx")]
    if not files:
        st.warning("Sube una plantilla primero")
    else:
        selected = st.selectbox("Seleccionar archivo", files)
        
        if st.button("Cargar Formulario", type="primary"):
            st.session_state.selected_file = selected
            st.rerun()
        
        if 'selected_file' in st.session_state:
            filepath = f"templates/{st.session_state.selected_file}"
            st.title(f"🧾 {st.session_state.selected_file.replace('.xlsx', '')}")
            
            # ==================== LECTURA AUTOMÁTICA DEL EXCEL ====================
            localidad = "Rio Segundo"
            equipo = "Alessandrini / Rosso / Baldoncini"
            clientes = 17
            total_desp = 0.0
            try:
                wb = load_workbook(filepath, data_only=True)
                ws3 = wb["Hoja3"] if "Hoja3" in wb.sheetnames else wb.active
                
                # Localidad (B2)
                localidad = str(ws3.cell(row=2, column=2).value or localidad)
                
                # Equipo (Hoja2 B2)
                if "Hoja2" in wb.sheetnames:
                    ws2 = wb["Hoja2"]
                    equipo = str(ws2.cell(row=2, column=2).value or equipo)
                
                # Cantidad de Clientes (Hoja3 - alrededor de fila 32)
                clientes = int(ws3.cell(row=32, column=3).value or 17)
                
                # Total Despachado (Hoja3 fila 24 columna E o F)
                total_desp = float(ws3.cell(row=24, column=5).value or 0)
            except:
                st.warning("No se pudieron leer todos los datos del Excel")

            st.success(f"Trabajando con: **{st.session_state.selected_file}**")

            # ==================== DATOS LEÍDOS ====================
            st.subheader("1. Datos Generales (del Excel)")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Localidad", localidad)
                st.metric("Equipo", equipo)
                st.metric("Camión", "AD")
            with col2:
                st.metric("Fecha", datetime.today().strftime("%d-%m-%Y"))
                st.metric("Cantidad de Clientes", clientes)
                st.metric("Total Despachado", total_desp)

            # ==================== CAMPOS EDITABLES ====================
            st.subheader("2. Retornos y Operaciones")
            c1, c2 = st.columns(2)
            with c1:
                ret_2500 = st.number_input("Retorno 2500", value=0.0, step=0.01, format="%.2f")
                ret_2000 = st.number_input("Retorno 2000", value=0.0, step=0.01, format="%.2f")
            with c2:
                ret_1250 = st.number_input("Retorno 1250", value=0.0, step=0.01, format="%.2f")

            # ... (agrega aquí los demás campos que necesites)

            observaciones = st.text_area("Observaciones", height=80)

            st.subheader("Firmas")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                firma_rep = st.text_input("Firma Repartidor", "")
            with col_f2:
                firma_ctrl = st.text_input("Firma Controlador", "")

            if st.button("💾 Guardar Control Completo", type="primary"):
                if not firma_rep or not firma_ctrl:
                    st.error("Complete ambas firmas")
                else:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                    data = {
                        "Fecha": datetime.today().strftime("%d-%m-%Y"),
                        "Hora": datetime.today().strftime("%H:%M"),
                        "Localidad": localidad,
                        "Equipo": equipo,
                        "Clientes": clientes,
                        "Total_Despachado": total_desp,
                        "Archivo": st.session_state.selected_file,
                        "Observaciones": observaciones,
                        "Firma_Repartidor": firma_rep,
                        "Firma_Controlador": firma_ctrl
                    }
                    pd.DataFrame([data]).to_csv(f"data/control_{timestamp}.csv", index=False)
                    st.success("✅ Guardado correctamente!")
                    st.balloons()

else:
    st.header("📋 Historial")
    data_files = [f for f in os.listdir("data") if f.endswith(".csv")]
    if data_files:
        for f in sorted(data_files, reverse=True):
            df = pd.read_csv(f"data/{f}")
            st.subheader(f"📅 {df['Fecha'].iloc[0]} {df.get('Hora', [''])[0]}")
            st.dataframe(df, use_container_width=True)
            st.divider()
    else:
        st.info("Aún no hay controles guardados.")
