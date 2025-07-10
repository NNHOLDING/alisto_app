import streamlit as st
from datetime import datetime
import pytz
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Función para guardar datos en Google Sheets
def guardar_en_google_sheets(datos):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    service_account_info = st.secrets["gcp_service_account"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1RsNWb6CwsKd6xt-NffyUDmVgDOgqSo_wgR863Mxje30/edit").worksheet("TCertificados")
    sheet.append_row(datos)

# Estilo personalizado
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

# Título
st.title("📦 Smart Intelligence Tools ")

# Hora local de Costa Rica
cr_timezone = pytz.timezone("America/Costa_Rica")
now_cr = datetime.now(cr_timezone)

# Captura del código escaneado desde la URL
codigo_escaneado = st.query_params.get("codigo", [""])[0]

# Diccionario de empleados
empleados = {
    51857: "Carlos Carvajal Villalobos",
    59157: "Allan Valenciano Delgado",
    59683: "Jerlyn Villalobos Morales",
    50440: "Stanley Araya Arce",
    59433: "Ronald Vargas Sanchez",
    56353: "Alfredo Mota Somarriba",
    50319: "Jesus Eduarte Alvarez",
    50156: "Marco Alcazar Umaña",
    52182: "Gerald Corrales castillo",
    55926: "Juan Montiel sequeira",
    51417: "Nestor Andrey bustamenta urrutia",
    54170: "Joel Antonio Gutierrez Obando",
    54555: "Kevin Inces Cerdas",
    55501: "Jean Poul Gamboa Campos",
    59116: "Maureen Ureña Esquivel",
    58898: "Maria Solis Garcia",
    52106: "Hellen Ceciliano Campos",
    55503: "Esteban Brenes Solis",
    53960: "Jeremy Gonzalez Cersosimo",
    51918: "Andres castro Gonzalez",
    51416: "Esteban Armando Brenes Ulate",
    57713: "EddHAnk Antonio Rodriguez Bryan",
    59292: "keynor Andree Vargas Mena",
    54921: "Harold Lopez Cespedes",
    59907: "Manfred Zepeda",
    53990: "Gerson Granados",
    52106: "EileenCeciliano Campos",
    56475: "Alexander Navarro",
    58631: "Alex Segura",
    20025: "Planta/producción",
    20254: "Fernando Brizuela",
    51423: "Esteban Brens Solis",
    50205: "Hanzel Díaz",
    50403: "Administrador1"
}
# Contenedor del formulario
with st.container():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    with st.form("formulario_alisto"):
        st.subheader("📝 Almacèn Unimar")

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

        # Botón para abrir la app de escaneo
        scan_url = "intent://scan/#Intent;scheme=zxing;package=com.datalogic.scan.demo;end"
        st.markdown(f'<a href="{scan_url}"><button type="button">📷 Escanear código</button></a>', unsafe_allow_html=True)

        codigo = st.text_input("🔍 Código (use lector de código de barras)", value=codigo_escaneado)

        # Selector de código de empleado
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

# Footer
st.markdown("""
<hr style="margin-top: 50px; border: none; border-top: 1px solid #ccc;" />
<div style="text-align: center; color: gray; font-size: 0.9em; margin-top: 20px;">
    NN HOLDING SOLUTIONS &copy; 2025, Todos los derechos reservados
</div>
""", unsafe_allow_html=True)
