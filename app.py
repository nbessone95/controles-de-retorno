import streamlit as st
from datetime import datetime
import os
import pandas as pd
from PIL import Image
from openpyxl import load_workbook

st.set_page_config(page_title="Control Retornos", layout="wide")

# Crear directorios si no existen
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
            st.success(f"✅ {file.name} guardado correctamente")
        st.rerun()

elif menu == "Completar Formulario":
    # 1. LOGICA DE BUSQUEDA Y SELECCIÓN DE ARCHIVOS
    files = [f for f in os.listdir("templates") if f.endswith(".xlsx")]
    
    if 'selected_file' not in st.session_state and files:
        st.session_state.selected_file = files[0]

    # Variables dinámicas por defecto por si falla la lectura o no hay archivo
    localidad_dinamica = "Rio Segundo"
    equipo_dinamico = "Alessandrini / Rosso / Baldoncini"
    camion_dinamico = "AD"
    fecha_dinamica = datetime.today().strftime("%d-%m-%Y")
    
    desp_2500 = desp_2000 = desp_1250 = total_desp = 0

    # 2. LECTURA ANTICIPADA DEL EXCEL
    if files and st.session_state.get('selected_file'):
        filepath = f"templates/{st.session_state.selected_file}"
        
        # Intentar extraer Localidad y Fecha desde el nombre del archivo de forma inteligente
        nombre_sin_ext = st.session_state.selected_file.replace(".xlsx", "")
        if "Laguna Larga" in nombre_sin_ext:
            localidad_dinamica = "Laguna Larga"
        elif "Rio Segundo" in nombre_sin_ext:
            localidad_dinamica = "Rio Segundo"
            
        # Intentar extraer la fecha del nombre del archivo (formato DD-MM-AAAA)
        partes_nombre = nombre_sin_ext.split(" ")
        for parte in partes_nombre:
            if "-" in parte and len(parte) == 10:
                fecha_dinamica = parte

        # Lectura de celdas desde el Excel
        try:
            wb = load_workbook(filepath, data_only=True)
            ws = wb["Hoja3"] if "Hoja3" in wb.sheetnames else wb.active
            
            # Leer el Camión desde la celda K1
            camion_dinamico = ws["K1"].value or camion_dinamico
            
            # Leer el Equipo desde la fila 2 (Columnas A, B, D, E, F, G)
            columnas_equipo = ["A", "B", "D", "E", "F", "G"]
            valores_equipo = []
            for col in columnas_equipo:
                celda_val = ws[f"{col}2"].value
                if celda_val:
                    valores_equipo.append(str(celda_val).strip())
            
            if valores_equipo:
                equipo_dinamico = " / ".join(valores_equipo)
            
            # Leer cantidades de despacho
            desp_2500 = ws.cell(row=5, column=2).value or 0
            desp_2000 = ws.cell(row=8, column=2).value or 0
            desp_1250 = ws.cell(row=11, column=2).value or 0
            total_desp = ws.cell(row=24, column=5).value or (desp_2500 + desp_2000 + desp_1250)
        except:
            pass

    # 3. RENDERIZADO DE TÍTULOS CON DATOS EN VIVO
    st.title(f"🧾 Control de Retornos - {localidad_dinamica}")
    st.caption(f"Equipo: {equipo_dinamico}")
    st.header("✍️ Completar Control")
    
    if not files:
        st.warning("No hay plantillas. Ve a 'Subir Plantillas' primero.")
    else:
        col_select, col_btn = st.columns([3,1])
        with col_select:
            selected = st.selectbox("Seleccionar archivo a completar", files, 
                                  index=files.index(st.session_state.selected_file) if st.session_state.selected_file in files else 0,
                                  key="file_selector")
        
        with col_btn:
            if st.button("Cargar y Leer Datos del Excel", type="primary"):
                st.session_state.selected_file = selected
                st.rerun()
        
        if st.session_state.selected_file:
            st.success(f"Trabajando con: **{st.session_state.selected_file}**")
            
            # HOJA 1 - Solo Lectura
            st.subheader("1. CONTROL DE RETORNOS DE ENVASES (Solo Lectura)")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Localidad", localidad_dinamica)
                st.metric("Equipo", equipo_dinamico)
                st.metric("Camión", camion_dinamico)
                st.metric("Fecha", fecha_dinamica)
            with col2:
                st.metric("Cantidad 2500", desp_2500)
                st.metric("Cantidad 2000", desp_2000)
                st.metric("Cantidad 1250", desp_1250)
                st.metric("**TOTAL DESPACHADO**", total_desp)

            st.subheader("Otros Datos (no modificables)")
            st.metric("Cantidad de Clientes", 17)
            st.metric("Pallets", 0)
            st.metric("Chapas", 0)

            # HOJA 2 - Editable
            st.subheader("2. Retornos y Cambios (Completar)")
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
                cam_220 = st.number_input("Cambio 220", value=0)
                cam_473 = st.number_input("Cambio 473", value=0)

            st.write("**Retorno Lleno**")
            rl1, rl2 = st.columns(2)
            with rl1:
                lleno_2500 = st.number_input("Retorno Lleno 2500", value=0)
                lleno_2000 = st.number_input("Retorno Lleno 2000", value=0)
            with rl2:
                lleno_1250 = st.number_input("Retorno Lleno 1250", value=0)

            observaciones = st.text_area("Observaciones", height=100)

            # Firma
            st.subheader("✍️ Firma Digital")
            from streamlit_drawable_canvas import st_canvas
            canvas = st_canvas(height=280, width=700, stroke_width=4, stroke_color="#000000", 
                             background_color="#ffffff", key="canvas")

            if st.button("💾 Guardar Control Completo", type="primary"):
                if canvas.image_data is not None:
                    img = Image.fromarray(canvas.image_data.astype("uint8"))
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                    firma_path = f"completed/firma_{timestamp}.png"
                    img.save(firma_path)
                    
                    data = {key: value for key, value in locals().items() if key in [
                        'ret_2500','ret_2000','ret_1250','cam_2500','cam_2000','cam_1250',
                        'cam_354','cam_220','cam_473','lleno_2500','lleno_2000','lleno_1250',
                        'observaciones']}
                    data.update({
                        "Fecha": fecha_dinamica,
                        "Localidad": localidad_dinamica,
                        "Equipo": equipo_dinamico,
                        "Camion": camion_dinamico,
                        "Archivo": st.session_state.selected_file,
                        "Total_Despachado": total_desp
                    })
                    pd.DataFrame([data]).to_csv(f"data/control_{timestamp}.csv", index=False)

                    st.success("✅ ¡Control guardado correctamente!")
                    st.image(firma_path, caption="Firma guardada")
                    st.balloons()
                else:
                    st.error("Por favor realizá tu firma digital")

else:
    st.header("📋 Historial")
    data_files = [f for f in os.listdir("data") if f.endswith(".csv")]
    if data_files:
        for f in sorted(data_files, reverse=True):
            df = pd.read_csv(f"data/{f}")
            loc = df['Localidad'].iloc[0] if 'Localidad' in df.columns else ''
            st.subheader(f"📅 {df['Fecha'].iloc[0]} - {loc}")
            st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay controles guardados.")
