import streamlit as st
from datetime import datetime
import pytz

# Título
st.title("Smart Intelligence Tools - Almacén")

# Obtener fecha y hora actual en zona horaria de Costa Rica
cr_timezone = pytz.timezone("America/Costa_Rica")
now_cr = datetime.now(cr_timezone)

# Formulario
with st.form("formulario_alisto"):
    st.write("Por favor complete los siguientes campos:")

    # Fecha actual
    fecha = st.date_input("Fecha", value=now_cr.date())

    # Placa
    placa = st.text_input("Placa")

    # Lista desplegable
    opcion = st.selectbox("Seleccione una opción", [200,201,202,203, 300, 400, 500])

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
        st.write(f"🔢 Opción seleccionada: {opcion}")
        st.write(f"📦 Cantidad de líneas: {cantidad_lineas}")
        st.write(f"🕒 Hora: {hora}")
