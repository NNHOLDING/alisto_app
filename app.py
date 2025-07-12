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
st.title("📦 Smart Intelligence Tools - Almacén Unimar")

# Hora local de Costa Rica
cr_timezone = pytz.timezone("America/Costa_Rica")
now_cr = datetime.now(cr_timezone)

# Captura del código escaneado desde la URL
codigo_escaneado = st.query_params.get("codigo", [""])[0]

# Diccionario de empleados
empleados = {
    51417: "Nestor Bustamante",
    51416: "Esteban Ulate",
    51918: "Andres Castro",
    59907: "Manfred Zepeda",
    59292: "Keynor Vargas"
}

# Contenedor del formulario
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

# ✅ Menú lateral izquierdo
with st.sidebar:
    st.header("🧭 Menú")
    opcion_menu = st.selectbox("Seleccione una opción", ["Inicio", "🏷️ Diseñador de etiqueta ZPL"])

# ✅ Contenido del menú de impresión ZPL
if opcion_menu == "🏷️ Etiqueta Certificado ZPL":
    st.subheader("🏷️ Etiqueta Certificado ZPL")

    cliente = st.selectbox("🧑 Cliente", ["prueba1", "prueba2", "prueba3", "prueba4"])
    placa = st.selectbox("🚚 Placa", [201, 202, 203])
    cantidad_etiquetas = st.number_input("🔢 Cantidad de etiquetas", min_value=1, step=1)
    impresora_ip = "192.188.101.118"  # IP de la impresora Zebra 60SANJOSE

    if st.button("🖨️ Imprimir etiquetas"):
        exito = True
        for i in range(cantidad_etiquetas):
            zpl = (
                "^XA\n"
                "^PW600\n"
                "^LL400\n"
                "^FO50,30^A0N,40,40^FDCliente:^FS\n"
                f"^FO250,30^A0N,40,40^FD{cliente}^FS\n"
                "^FO50,100^A0N,40,40^FDPlaca:^FS\n"
                f"^FO250,100^A0N,40,40^FD{placa}^FS\n"
                f"^FO50,170^A0N,40,40^FDEtiqueta {i+1} de {cantidad_etiquetas}^FS\n"
                "^XZ\n"
            )
            try:
                import socket
                port = 9100
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as printer_socket:
                    printer_socket.connect((impresora_ip, port))
                    printer_socket.send(zpl.encode("utf-8"))
                st.write(f"✅ Etiqueta {i+1} enviada correctamente")
            except Exception as e:
                st.error(f"❌ Falló el envío de la etiqueta {i+1}: {e}")
                exito = False
                break

        if exito:
            st.success(f"✅ Se enviaron {cantidad_etiquetas} etiquetas a la impresora Zebra (60SANJOSE - IP: {impresora_ip})")
