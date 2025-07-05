import streamlit as st
from datetime import datetime
import pytz
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Función para guardar datos en Google Sheets usando credenciales desde st.secrets
def guardar_en_google_sheets(datos):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1RsNWb6CwsKd6xt-NffyUDmVgDOgqSo_wgR863Mxje30").worksheet("TCertificados")
    sheet.append_row(datos)

# Estilo personalizado
st.markdown(
    """
    <style>
    .form-container {
        background-color: #f0f0f0;
        border: 2px solid #c0c0c0;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título
st.title("Smart Intelligence Tools - Almacén Unimar")

# Hora local de Costa Rica
cr_timezone = pytz.timezone("America/Costa_Rica")
now_cr = datetime.now(cr_timezone)

# Contenedor del formulario
with st.container():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    with st.form("formulario_alisto"):
        st.write("Por favor complete los siguientes campos:")

        fecha = st.date_input("Fecha", value=now_cr.date())

        opciones_placa = [
            200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219,
            300, 310, 302, 303, 304, 305, 306, 307, 308, 309, 311, 312, 313, 314, 315, 316, 317, 318, 319,
            400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412,
            500, "SIGMA", "POZUELO", "MAFAM", "COMAPAN", "UNIVERSAL ALIMENTOS", "POPS", "HILLTOP", "SAM",
            "WALMART", "MEGASUPER", "GESSA", "F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08"
        ]
        opcion = st.selectbox("Seleccione una opción de placa", opciones_placa)
        placa = st.text_input("Placa", value=str(opcion))
        numero_orden = st.text_input("Número de orden")
        codigo = st.text_input("Código (use lector de código de barras)")
        descripcion = st.text_input("Descripción de producto")
        lote = st.text_input("Lote")
        fecha_lote = st.date_input("Fecha vencimiento del lote")
        valores_selector = [51417, 51416, 51918, 59907]
        codigo_seleccionado = st.selectbox("Seleccione un código adicional", valores_selector)
        nombre_empleado = st.text_input("Nombre de empleado")
        hora = st.time_input("Hora", value=now_cr.time())

        submit = st.form_submit_button("Guardar")

        if submit:
            st.success("Datos enviados correctamente")
            st.write("**Resumen de datos ingresados:**")
            st.write(f"📅 Fecha: {fecha}")
            st.write(f"🚚 Placa: {placa}")
            st.write(f"🧾 Número de orden: {numero_orden}")
            st.write(f"🔍 Código: {codigo}")
            st.write(f"📝 Descripción: {descripcion}")
            st.write(f"🏷️ Lote: {lote}")
            st.write(f"📆 Fecha del lote: {fecha_lote}")
            st.write(f"🔢 Código adicional seleccionado: {codigo_seleccionado}")
            st.write(f"👤 Nombre de empleado: {nombre_empleado}")
            st.write(f"🕒 Hora: {hora}")

            guardar_en_google_sheets([
                str(fecha), placa, numero_orden, codigo, descripcion, lote,
                str(fecha_lote), str(codigo_seleccionado), nombre_empleado, str(hora)
            ])

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <hr style="margin-top: 50px; border: none; border-top: 1px solid #ccc;" />
    <div style="text-align: center; color: gray; font-size: 0.9em; margin-top: 20px;">
        NN HOLDING SOLUTIONS &copy; 2025, Todos los derechos reservados
    </div>
    """,
    unsafe_allow_html=True
)