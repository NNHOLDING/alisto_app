import streamlit as st
from datetime import datetime
import pytz
import gspread
import pandas as pd
import matplotlib.pyplot as plt
from oauth2client.service_account import ServiceAccountCredentials

# -------------------------------
# Configuración de autenticación
# -------------------------------
def conectar_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    service_account_info = st.secrets["gcp_service_account"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    client = gspread.authorize(credentials)
    return client

# -------------------------------
# Guardar datos en Google Sheets
# -------------------------------
def guardar_en_google_sheets(datos):
    client = conectar_google_sheets()
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1RsNWb6CwsKd6xt-NffyUDmVgDOgqSo_wgR863Mxje30/edit").worksheet("TCertificados")
    sheet.append_row(datos)

# -------------------------------
# Obtener historial como DataFrame
# -------------------------------
@st.cache_data(ttl=300)
def obtener_historial():
    client = conectar_google_sheets()
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1RsNWb6CwsKd6xt-NffyUDmVgDOgqSo_wgR863Mxje30/edit").worksheet("TCertificados")
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# -------------------------------
# Estilo personalizado
# -------------------------------
st.markdown("""
<style>
.form-container {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 25px;
    margin-top: 20px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
}
.stButton>button:hover {
    background-color: #45a049;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Diccionario de empleados
# -------------------------------
empleados = {
    51417: "Nestor Bustamante",
    51416: "Esteban Ulate",
    51918: "Andres Castro",
    59907: "Manfred Zepeda",
    59292: "Keynor Vargas"
}

# -------------------------------
# Hora local de Costa Rica
# -------------------------------
cr_timezone = pytz.timezone("America/Costa_Rica")
now_cr = datetime.now(cr_timezone)

# -------------------------------
# Tabs principales
# -------------------------------
tab1, tab2 = st.tabs(["📋 Formulario", "📑 Historial"])

# -------------------------------
# TAB 1: Formulario
# -------------------------------
with tab1:
    st.title("📦 Smart Intelligence Tools - Almacén Unimar")
    codigo_escaneado = st.query_params.get("codigo", [""])[0]

    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)

        with st.form("formulario_alisto"):
            st.subheader("📝 Ingreso de datos")

            col1, col2 = st.columns(2)
            with col1:
                fecha = st.date_input("📅 Fecha", value=now_cr.date())
                numero_orden = st.text_input("🧾 Número de orden")
                cantidad = st.number_input("📦 Cantidad", min_value=1, step=1)
                fecha_lote = st.date_input("📆 Fecha vencimiento del lote")
            with col2:
                opciones_placa = [
                    200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219,
                    300, 310, 302, 303, 304, 305, 306, 307, 308, 309, 311, 312, 313, 314, 315, 316, 317, 318, 319,
                    400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412,
                    500, "SIGMA", "POZUELO", "MAFAM", "COMAPAN", "UNIVERSAL ALIMENTOS", "POPS", "HILLTOP", "SAM",
                    "WALMART", "MEGASUPER", "GESSA", "F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08"
                ]
                opcion = st.selectbox("🚚 Seleccione una opción de placa", opciones_placa)
                placa = st.text_input("🔢 Placa", value=str(opcion))
                lote = st.text_input("🏷️ Lote")
                hora = st.time_input("🕒 Hora", value=now_cr.time())

            scan_url = "intent://scan/#Intent;scheme=zxing;package=com.datalogic.scan.demo;end"
            st.markdown(f'<a href="{scan_url}"><button type="button">📷 Escanear código</button></a>', unsafe_allow_html=True)

            codigo = st.text_input("🔍 Código (use lector de código de barras)", value=codigo_escaneado)
            codigo_seleccionado = st.selectbox("👤 Seleccione un código de empleado", list(empleados.keys()))
            nombre_empleado = empleados.get(codigo_seleccionado, "")
            descripcion = ""

            submit = st.form_submit_button("✅ Guardar")

            if submit:
                guardar_en_google_sheets([
                    str(fecha), placa, numero_orden, codigo, descripcion, cantidad, lote,
                    str(fecha_lote), str(codigo_seleccionado), nombre_empleado, str(hora)
                ])
                st.toast("✅ Datos enviados correctamente")
                st.success("Datos guardados con éxito.")
                with st.expander("📋 Ver resumen de datos ingresados"):
                    st.write(f"📅 Fecha: {fecha}")
                    st.write(f"🚚 Placa: {placa}")
                    st.write(f"🧾 Número de orden: {numero_orden}")
                    st.write(f"🔍 Código: {codigo}")
                    st.write(f"📦 Cantidad: {cantidad}")
                    st.write(f"🏷️ Lote: {lote}")
                    st.write(f"📆 Fecha del lote: {fecha_lote}")
                    st.write(f"👤 Empleado: {nombre_empleado} ({codigo_seleccionado})")
                    st.write(f"🕒 Hora: {hora}")

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# TAB 2: Historial
# -------------------------------
with tab2:
    st.subheader("📑 Historial de registros")

    try:
        df = obtener_historial()
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        # Convertir fechas
        if "fecha" in df.columns:
            df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            filtro_empleado = st.selectbox("👤 Filtrar por código de empleado", ["Todos"] + list(empleados.keys()))
        with col2:
            fecha_inicio = st.date_input("📆 Fecha inicio", value=df["fecha"].min().date() if "fecha" in df.columns else now_cr.date())
            fecha_fin = st.date_input("📆 Fecha fin", value=df["fecha"].max().date() if "fecha" in df.columns else now_cr.date())

        if filtro_empleado != "Todos" and "código_de_empleado" in df.columns:
            df = df[df["código_de_empleado"] == int(filtro_empleado)]

        if "fecha" in df.columns:
            df = df[(df["fecha"] >= pd.to_datetime(fecha_inicio)) & (df["fecha"] <= pd.to_datetime(fecha_fin))]

        st.dataframe(df, use_container_width=True)

        # Exportación
        csv = df.to_csv(index=False).encode("utf-8")
        excel = df.to_excel(index=False, engine="openpyxl")
        st.download_button("⬇️ Descargar CSV", data=csv, file_name="historial.csv", mime="text/csv")
        st.download_button("⬇️ Descargar Excel", data=excel, file_name="historial.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # Gráficos
        if "nombre_empleado" in df.columns:
            st.subheader("📊 Registros por empleado")
            conteo = df["nombre_empleado"].value_counts()
            fig, ax = plt.subplots()
            conteo.plot(kind="bar", ax=ax)
            ax.set_ylabel("Cantidad de registros")
            st.pyplot(fig)

        if "fecha" in df.columns:
            st.subheader("📈 Registros por fecha")
            conteo_fecha = df["fecha"].dt.date.value_counts().sort_index()
            fig2, ax2 = plt.subplots()
            conteo_fecha.plot(kind="line", marker="o", ax=ax2)
            ax2.set_ylabel("Cantidad")
            ax2.set_xlabel("Fecha")
            st.pyplot(fig2)

    except Exception as e:
        st.error("⚠️ No se pudo cargar el historial.")
        st.exception(e)

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
<hr style="margin-top: 50px; border: none; border-top: 1px solid #ccc;" />
<div style="text-align: center; color: gray; font-size: 0.9em; margin-top: 20px;">
    NN HOLDING SOLUTIONS &copy; 2025, Todos los derechos reservados
</div>
""", unsafe_allow_html=True)
