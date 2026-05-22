import streamlit as st
from datetime import datetime
import os
import pandas as pd
from openpyxl import load_workbook

st.set_page_config(page_title="Control Retornos", layout="wide")

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
            st.title(f"🧾 {st.session_state.selected_file.replace('.xlsx', '')}")
            
            localidad = "Rio Segundo"
            equipo = "Alessandrini / Rosso / Baldoncini"
            desp_2500 = desp_2000 = desp_1250 = total_desp = 0.0
            try:
                wb = load_workbook(filepath, data_only=True)
                ws3 = wb["Hoja3"] if "Hoja3" in wb.sheetnames else wb.active
                localidad = str(ws3.cell(row=2, column=2).value or localidad)
                
                if "Hoja2" in wb.sheetnames:
                    ws2 = wb["Hoja2"]
                    equipo = str(ws2.cell(row=2, column=2).value or equipo)
                
                desp_2500 = float(ws3.cell(row=5, column=2).value or 0)
                desp_2000 = float(ws3.cell(row=8, column=2).value or 0)
                desp_1250 = float(ws3.cell(row=11, column=2).value or 0)
                total_desp = float(ws3.cell(row=24, column=5).value or (desp_2500 + desp_2000 + desp_1250))
            except:
                pass

            st.success(f"Trabajando con: **{st.session_state.selected_file}**")

            # Hoja 1
            st.subheader("1. CONTROL DE RETORNOS DE ENVASES")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Localidad", localidad)
                st.metric("Equipo", equipo)
                st.metric("Camión", "AD")
                st.metric("Fecha", datetime.today().strftime("%d-%m-%Y"))
            with col2:
                st.metric("Cantidad 2500", desp_2500)
                st.metric("Cantidad 2000", desp_2000)
                st.metric("Cantidad 1250", desp_1250)
                st.metric("**TOTAL DESPACHADO**", total_desp)

            st.subheader("Datos Fijos")
            st.metric("Clientes", 17)
            st.metric("Pallets", 0)
            st.metric("Chapas", 0)

            # Hoja 2 - Con decimales
            st.subheader("2. Retornos y Cambios")
            r1, r2 = st.columns(2)
            with r1:
                ret_2500 = st.number_input("Retorno 2500", value=0.0, step=0.01)
                ret_2000 = st.number_input("Retorno 2000", value=0.0, step=0.01)
            with r2:
                ret_1250 = st.number_input("Retorno 1250", value=0.0, step=0.01)

            st.write("**Cambios**")
            c1, c2, c3 = st.columns(3)
            with c1:
                cam_2500 = st.number_input("Cambio 2500", value=0.0, step=0.01)
                cam_2000 = st.number_input("Cambio 2000", value=0.0, step=0.01)
            with c2:
                cam_1250 = st.number_input("Cambio 1250", value=0.0, step=0.01)
                cam_354 = st.number_input("Cambio 354", value=0.0, step=0.01)
            with c3:
                cam_220 = st.number_input("Cambio 220", value=0.0, step=0.01)
                cam_473 = st.number_input("Cambio 473", value=0.0, step=0.01)

            st.write("**Retorno Lleno**")
            rl1, rl2 = st.columns(2)
            with rl1:
                lleno_2500 = st.number_input("Retorno Lleno 2500", value=0.0, step=0.01)
                lleno_2000 = st.number_input("Retorno Lleno 2000", value=0.0, step=0.01)
            with rl2:
                lleno_1250 = st.number_input("Retorno Lleno 1250", value=0.0, step=0.01)

            # Nuevas columnas
            venta_envases = st.number_input("Venta de Envases", value=0.0, step=0.01)
            prestamos = st.number_input("Préstamos", value=0.0, step=0.01)
            retiros = st.number_input("Retiros", value=0.0, step=0.01)

            observaciones = st.text_area("Observaciones", height=100)

            st.subheader("✍️ Firma Digital")
            firma_nombre = st.text_input("Nombre y Apellido (Firma)", "")

            if st.button("💾 Guardar Control Completo", type="primary"):
                if not firma_nombre.strip():
                    st.error("Por favor escriba su nombre como firma")
                else:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                    data = {
                        "Fecha": datetime.today().strftime("%d-%m-%Y"),
                        "Hora": datetime.today().strftime("%H:%M"),
                        "Localidad": localidad,
                        "Equipo": equipo,
                        "Archivo": st.session_state.selected_file,
                        "Total_Despachado": total_desp,
                        "Retorno_2500": ret_2500,
                        "Retorno_2000": ret_2000,
                        "Retorno_1250": ret_1250,
                        "Cambio_2500": cam_2500,
                        "Cambio_2000": cam_2000,
                        "Cambio_1250": cam_1250,
                        "Cambio_354": cam_354,
                        "Cambio_220": cam_220,
                        "Cambio_473": cam_473,
                        "Lleno_2500": lleno_2500,
                        "Lleno_2000": lleno_2000,
                        "Lleno_1250": lleno_1250,
                        "Venta_Envases": venta_envases,
                        "Prestamos": prestamos,
                        "Retiros": retiros,
                        "Observaciones": observaciones,
                        "Firma": firma_nombre
                    }
                    pd.DataFrame([data]).to_csv(f"data/control_{timestamp}.csv", index=False)

                    st.success("✅ ¡Control guardado correctamente!")
                    st.info(f"Firma: **{firma_nombre}** - {datetime.now().strftime('%d-%m-%Y %H:%M')}")
                    st.balloons()

else:  # Historial Corregido
    st.header("📋 Historial de Controles")
    data_files = [f for f in os.listdir("data") if f.endswith(".csv")]
    
    if data_files:
        for f in sorted(data_files, reverse=True):
            try:
                df = pd.read_csv(f"data/{f}")
                fecha = df['Fecha'].iloc[0] if 'Fecha' in df.columns else "Sin fecha"
                hora = df['Hora'].iloc[0] if 'Hora' in df.columns else ""
                
                st.subheader(f"📅 {fecha} {hora} - {df['Archivo'].iloc[0]}")
                
                loc = df['Localidad'].iloc[0] if 'Localidad' in df.columns else "Rio Segundo"
                eq = df['Equipo'].iloc[0] if 'Equipo' in df.columns else "N/A"
                st.caption(f"Localidad: {loc} | Equipo: {eq}")
                
                st.dataframe(df, use_container_width=True)
                st.divider()
            except:
                st.warning(f"Error al leer {f}")
    else:
        st.info("Aún no hay controles guardados.")
