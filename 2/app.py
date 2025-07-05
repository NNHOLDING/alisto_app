
import streamlit as st
from datetime import datetime
import pytz

# Estilo personalizado con fondo azul claro y marco plateado claro
st.markdown(
    """
    <style>
    .main {
        background-color: #e0f0ff;
    }
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
st.title("Formulario de Alisto - Almacén")

# Obtener fecha y hora actual en zona horaria de Costa Rica
cr_timezone = pytz.timezone("America/Costa_Rica")
now_cr = datetime.now(cr_timezone)

# Contenedor del formulario con estilo
with st.container():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    with st.form("formulario_alisto"):
        st.write("Por favor complete los siguientes campos:")

        # Fecha actual
        fecha = st.date_input("Fecha", value=now_cr.date())

        # Lista desplegable para seleccionar placa
        opciones_placa = [200, 300, 400, 500]
        opcion = st.selectbox("Seleccione una opción de placa", opciones_placa)

        # Campo Placa autocompletado con la opción seleccionada
        placa = st.text_input("Placa", value=str(opcion))

        # Campo Número de orden
        numero_orden = st.text_input("Número de orden")

        # Campo Código (para lector de código de barras)
        codigo = st.text_input("Código (use lector de código de barras)")

        # Cantidad de líneas
        cantidad_lineas = st.number_input("Cantidad de líneas", min_value=0, step=1)

        # Hora actual
        hora = st.time_input("Hora", value=now_cr.time())

        # Botón de envío
        submit = st.form_submit_button("Iniciar")

        if submit:
            st.success("Formulario enviado correctamente")
            st.write("**Resumen de datos ingresados:**")
            st.write(f"📅 Fecha: {fecha}")
            st.write(f"🚚 Placa: {placa}")
            st.write(f"🧾 Número de orden: {numero_orden}")
            st.write(f"🔍 Código: {codigo}")
            st.write(f"📦 Cantidad de líneas: {cantidad_lineas}")
            st.write(f"🕒 Hora: {hora}")

    st.markdown('</div>', unsafe_allow_html=True)
