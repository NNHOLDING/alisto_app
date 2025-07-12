import streamlit as st
from datetime import datetime
import pytz
import gspread
import socket
from oauth2client.service_account import ServiceAccountCredentials

# ✅ Guardar en Google Sheets
def guardar_en_google_sheets(datos):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    service_account_info = st.secrets["gcp_service_account"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1RsNWb6CwsKd6xt-NffyUDmVgDOgqSo_wgR863Mxje30/edit").worksheet("TCertificados")
    sheet.append_row(datos, value_input_option='USER_ENTERED')

# ✅ Enviar ZPL a impresora
def enviar_a_impresora(ip, zpl_data):
    try:
        port = 9100
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as printer_socket:
            printer_socket.connect((ip, port))
            printer_socket.send(zpl_data.encode('utf-8'))
        return True
    except Exception as e:
        st.error(f"❌ Error al imprimir: {e}")
        return False

# 🎨 Estilo personalizado
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
    background-color: #4CAF50 !important;
    color: white !important;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
}
.stButton>button:hover {
    background-color: #388E3C !important;
}
</style>
""", unsafe_allow_html=True)

# 🖼️ Logo y título
logo_url = "https://drive.google.com/uc?id=1_2lXCttnYd9mPBuiWtVGTKNV_lmZgsTD"
st.markdown(f"""
<div style="display: flex; align-items: center;">
    <img src="{logo_url}" alt="Logo" width="60" style="margin-right: 15px;">
    <h1 style="margin: 0;">📦 Smart Intelligence Tools</h1>
</div>
""", unsafe_allow_html=True)

# ⏰ Hora local Costa Rica
cr_timezone = pytz.timezone("America/Costa_Rica")
now_cr = datetime.now(cr_timezone)
codigo_escaneado = st.query_params.get("codigo", [""])[0]

# 👥 Diccionario de empleados (simplificado)
empleados = {
    51857: "Carlos Carvajal",
    59157: "Allan Valenciano",
    59683: "Jerlyn Villalobos",
    50403: "Admin1"
}

# 🖱️ Tabs
tab1, tab2, tab3 = st.tabs(["📦 Formulario principal", "🏷️ Generador de etiqueta", "🖨️ Printer"])

# 📦 Formulario principal
with tab1:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    with st.form("formulario_alisto"):
        st.subheader("📝 Almacén Unimar")

        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("📅 Fecha", value=now_cr.date())
            numero_orden = st.number_input("🧾 Número de orden", min_value=0, step=1)
            cantidad = st.number_input("📦 Cantidad", min_value=1, step=1)
            fecha_lote = st.date_input("📆 Fecha vencimiento del lote")
        with col2:
            opciones_placa = [200, 201, 202, 203, "SIGMA"]
            opcion = st.selectbox("🚚 Seleccione una opción de placa", opciones_placa)
            placa = st.text_input("🔢 Placa", value=str(opcion))
            lote = st.text_input("🏷️ Lote")
            hora = st.time_input("🕒 Hora", value=now_cr.time())

        scan_url = "intent://scan/#Intent;scheme=zxing;package=com.datalogic.scan.demo;end"
        st.markdown(f'<a href="{scan_url}"><button type="button">📷 Escanear código</button></a>', unsafe_allow_html=True)

        codigo = st.text_input("🔍 Código", value=codigo_escaneado)
        codigo_seleccionado = st.selectbox("👤 Seleccione empleado", list(empleados.keys()))
        nombre_empleado = empleados.get(codigo_seleccionado, "")
        descripcion = ""

        submit = st.form_submit_button("✅ Guardar")

        if submit:
            fila = [
                fecha.strftime("%Y-%m-%d"),
                placa,
                int(numero_orden),
                codigo,
                descripcion,
                int(cantidad),
                lote,
                fecha_lote.strftime("%Y-%m-%d"),
                int(codigo_seleccionado),
                nombre_empleado,
                hora.strftime("%H:%M:%S")
            ]
            guardar_en_google_sheets(fila)
            st.toast("✅ Datos enviados correctamente")
            st.success("Datos guardados con éxito.")
            with st.expander("📋 Ver resumen"):
                st.write(f"📅 Fecha: {fecha}")
                st.write(f"🚚 Placa: {placa}")
                st.write(f"🧾 Orden: {numero_orden}")
                st.write(f"🔍 Código: {codigo}")
                st.write(f"📦 Cantidad: {cantidad}")
                st.write(f"🏷️ Lote: {lote}")
                st.write(f"📆 Fecha lote: {fecha_lote}")
                st.write(f"👤 Empleado: {nombre_empleado}")
                st.write(f"🕒 Hora: {hora}")
    st.markdown('</div>', unsafe_allow_html=True)

# 🖨️ Printer: impresión directa
with tab3:
    st.subheader("🖨️ Impresión directa a Zebra")
    cliente = st.text_input("👤 Cliente", value="Cliente demo")
    placa = st.text_input("🚚 Placa", value="201")
    cantidad_etiquetas = st.number_input("🔢 Cantidad de etiquetas", min_value=1, step=1, value=1)
    impresora_ip = "192.168.101.119"

    if st.button("🖨️ Enviar etiquetas a impresora"):
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
                f"^FO50,170^A0N,40,40^FDEtiqueta #{i+1}^FS\n"
                "^XZ\n"
            )
            st.write(f"🖨️ Enviando etiqueta {i+1}...")
            if not enviar_a_impresora(impresora_ip, zpl):
                st.error(f"❌ Falló el envío de la etiqueta {i+1}")
                exito = False
                break
        if exito:
            st.success(f"✅ Se enviaron {cantidad_etiquetas} etiquetas correctamente a Zebra ({impresora_ip})")

# 📎 Footer
st.markdown("""
<hr style="margin-top: 50px; border: none; border-top: 1px solid #ccc;" />
<div style="text-align: center; color: gray; font-size: 0.9em; margin-top: 20px;">
    NN HOLDING SOLUTIONS &copy; 2025, Todos los derechos reservados
</div>
""", unsafe_allow_html=True)
