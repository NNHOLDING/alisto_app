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
st.title("📦 Smart Intelligence Tools")

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
        st.subheader("📝 Almacen Unimar 60")

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
        descripcion = "" # campo oculto

        submit = st.form_submit_button("✅ Guardar")

        if submit:
            # Validación de campos requeridos
            errores = []

            if not placa:
                errores.append("🚫 La placa no puede estar vacía.")
            if not lote:
                errores.append("🚫 El lote no puede estar vacío.")
            if not codigo:
                errores.append("🚫 El código escaneado no puede estar vacío.")
            if cantidad <= 0:
                errores.append("🚫 La cantidad debe ser mayor a cero.")

            if errores:
                for error in errores:
                    st.error(error)
                st.warning("❗ Corrige los errores antes de continuar.")
            else:
                # Registro en Google Sheets
                datos = [
                    str(fecha),
                    numero_orden,
                    placa,
                    codigo,
                    descripcion,  # ← corregido
                    cantidad,
                    lote,
                    str(fecha_lote),
                    str(codigo_seleccionado),
                    nombre_empleado,
                    str(hora)
                ]
                guardar_en_google_sheets(datos)
                st.toast("✅ Datos enviados correctamente")
                st.success("Datos guardados con éxito.")

                # Mostrar resumen
                with st.expander("📋 Ver resumen de datos ingresados"):
                    st.write(f"📅 Fecha: {fecha}")
                    st.write(f"🏷️ Lote: {lote}")
                    st.write(f"🚚 Placa: {placa}")
                    st.write(f"👤 Código empleado: {codigo_seleccionado}")
                    st.write(f"🔍 Código escaneado: {codigo}")
                    st.write(f"📦 Cantidad: {cantidad}")
                    st.write(f"📆 Fecha del lote: {fecha_lote}")
                    st.write(f"👤 Empleado: {nombre_empleado}")
                    st.write(f"🕒 Hora: {hora}")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<hr style="margin-top: 50px; border: none; border-top: 1px solid #ccc;" />
<div style="text-align: center; color: gray; font-size: 0.9em; margin-top: 20px;">
    NN HOLDING SOLUTIONS &copy; 2025, Todos los derechos reservados
</div>
""", unsafe_allow_html=True)

# 🟢 Inicializar estados
if "nombre_impresora_qr" not in st.session_state:
    st.session_state["nombre_impresora_qr"] = ""
if "component_value" not in st.session_state:
    st.session_state["component_value"] = ""

# 🔐 IPs válidas
ips_impresoras_validas = [
    "192.188.101.118",
    "192.168.1.201",
    "10.0.0.10"
]

# 🔧 Menú lateral
with st.sidebar:
    st.markdown("## ☰ Menú")
    opcion_menu = st.radio("Selecciona una opción:", [
        "Inicio",
        "🏷️ Diseñador de etiqueta SIT",
        "📷 Escáner de impresora (cámara)"
    ], label_visibility="collapsed")

# 🏠 INICIO
if opcion_menu == "Inicio":
    st.title(" ")
    st.info(" ")

# 🏷️ DISEÑADOR
elif opcion_menu == "🏷️ Diseñador de etiqueta SIT":
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.subheader("🏷️ Diseñador de Etiqueta SIT")

    col1, col2 = st.columns(2)
    with col1:
        cliente = st.selectbox("🧑 Cliente", [
            "prueba1", "COMPAN", "MAFAM", "DEMASA", "BIMBO COSTA RICA", "INDUSTRIA KURI",
            "QUIMICAS MUNDIALES", "POPS", "ALIMENTOS LIJEROS"
        ])
    with col2:
        placa = st.selectbox("🚚 Placa", [
            201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215,
            "SIGMA", "POZUELO", "COMAPAN", "UNIVERSAL ALIMENTOS", "HILLTOP", "WALMART"
        ])

    cantidad_etiquetas = st.number_input("🔢 Cantidad de etiquetas", min_value=1, step=1)

    # 🧠 Detectar valor escaneado y actualizar en sesión
    valor_qr = st.session_state.get("component_value", "")
    if valor_qr and valor_qr != st.session_state["nombre_impresora_qr"]:
        st.session_state["nombre_impresora_qr"] = valor_qr

    # 🖨️ Campo editable de IP sincronizado
    ip_impresora = st.text_input(
        "🖨️ IP de la impresora",
        value=st.session_state["nombre_impresora_qr"],
        key="campo_ip_impresora"
    )
    st.session_state["nombre_impresora_qr"] = ip_impresora

    # 📷 Botón para escanear QR
    activar_lector = st.button("📷 Escanear código QR de impresora")
    if activar_lector:
        import streamlit.components.v1 as components
        components.html("""
            <script src="https://unpkg.com/html5-qrcode"></script>
            <div id="reader" style="width:300px;margin:auto;"></div>
            <script>
            let lectorActivo = true;
            function sendToStreamlit(text) {
                if (lectorActivo) {
                    window.parent.postMessage({type: "streamlit:setComponentValue", value: text}, "*");
                    lectorActivo = false;
                    document.getElementById("reader").remove();
                }
            }
            function onScanSuccess(decodedText, decodedResult) {
                sendToStreamlit(decodedText);
            }
            let html5QrcodeScanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 });
            html5QrcodeScanner.render(onScanSuccess);
            </script>
        """, height=550)

    # 🖨️ Imprimir etiquetas
    if st.button("🖨️ Imprimir etiquetas"):
        if ip_impresora not in ips_impresoras_validas:
            st.error("❌ IP inválida. Escanea o escribe una IP autorizada.")
        else:
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
                        printer_socket.connect((ip_impresora, port))
                        printer_socket.send(zpl.encode("utf-8"))
                    st.write(f"✅ Etiqueta {i+1} enviada correctamente")
                except Exception as e:
                    st.error(f"❌ Falló el envío de la etiqueta {i+1}: {e}")
                    exito = False
                    break
            if exito:
                st.success(f"✅ Se enviaron {cantidad_etiquetas} etiquetas a la impresora ({ip_impresora})")

    st.markdown('</div>', unsafe_allow_html=True)
