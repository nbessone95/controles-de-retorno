import streamlit as st
from datetime import datetime
import os
import pandas as pd
from openpyxl import load_workbook

st.set_page_config(page_title="Control Retornos", layout="wide")
st.title("🧾 Control Retornos Rio Segundo")

os.makedirs("templates", exist_ok=True)
os.makedirs("data", exist_ok=True)

menu = st.sidebar.selectbox("Menú", ["Completar Formulario", "Subir Plantillas", "Historial"])

if menu == "Subir Plantillas":
    st.header("📤 Subir Plantillas")
    uploaded = st.file_uploader("Subir Excel", type="xlsx", accept_multiple_files=True)
    if uploaded:
        with st.spinner("Guardando..."):
            for file in uploaded:
                with open(f"templates/{file.name}", "wb") as f:
                    f.write(file.getbuffer())
                st.success(f"✅ {file.name}")
        st.rerun()

elif menu == "Completar Formulario":
    st.header("Completar Control")
    
    files = [f for f in os.listdir("templates") if f.endswith(".xlsx")]
    if not files:
        st.warning("Sube una plantilla primero")
    else:
        selected = st.selectbox("Seleccionar archivo", files)
        
        if st.button("Cargar Formulario", type="primary"):
            st.session_state.selected_file = selected
            st.rerun()
        
        if 'selected_file' in st.session_state:
            st.success(f"Editando: {st.session_state.selected_file}")
            
            # Formulario más compacto
            st.subheader("Retornos")
            c1, c2 = st.columns(2)
            with c1:
                ret_2500 = st.number_input("Retorno 2500", value=0.0, step=0.01, format="%.2f")
                ret_2000 = st.number_input("Retorno 2000", value=0.0, step=0.01, format="%.2f")
            with c2:
                ret_1250 = st.number_input("Retorno 1250", value=0.0, step=0.01, format="%.2f")

            st.subheader("Otras Operaciones")
            col1, col2, col3 = st.columns(3)
            with col1:
                venta = st.number_input("Venta Envases", value=0.0, step=0.01, format="%.2f")
            with col2:
                prestamos = st.number_input("Préstamos", value=0.0, step=0.01, format="%.2f")
            with col3:
                retiros = st.number_input("Retiros", value=0.0, step=0.01, format="%.2f")

            observaciones = st.text_area("Observaciones")
            firma = st.text_input("Firma (Nombre y Apellido)")

            if st.button("Guardar Control", type="primary"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                data = {
                    "Fecha": datetime.today().strftime("%d-%m-%Y"),
                    "Hora": datetime.today().strftime("%H:%M"),
                    "Archivo": st.session_state.selected_file,
                    "Retorno_2500": ret_2500,
                    "Retorno_2000": ret_2000,
                    "Retorno_1250": ret_1250,
                    "Venta_Envases": venta,
                    "Prestamos": prestamos,
                    "Retiros": retiros,
                    "Observaciones": observaciones,
                    "Firma": firma
                }
                pd.DataFrame([data]).to_csv(f"data/control_{timestamp}.csv", index=False)
                st.success("✅ Guardado!")
                st.balloons()

else:
    st.header("Historial")
    data_files = [f for f in os.listdir("data") if f.endswith(".csv")]
    if data_files:
        for f in sorted(data_files, reverse=True):
            df = pd.read_csv(f"data/{f}")
            st.subheader(f"📅 {df['Fecha'].iloc[0]}")
            st.dataframe(df, use_container_width=True)
            st.divider()
    else:
        st.info("No hay controles guardados aún.")
