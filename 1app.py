import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def guardar_en_google_sheets(fecha_lote, codigo_seleccionado, nombre_empleado, hora):
    # Definir el alcance de acceso
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Obtener credenciales desde st.secrets
    creds_dict = st.secrets["google_sheets"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

    # Autorizar cliente de Google Sheets
    client = gspread.authorize(creds)

    # Abrir hoja de cálculo por URL y seleccionar la pestaña
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1RsNWb6CwsKd6xt-NffyUDmVgDOgqSo_wgR863Mxje30/edit#gid=1441343050")
    worksheet = sheet.worksheet("TCertificados")

    # Agregar fila con los datos
    nueva_fila = [str(fecha_lote), str(codigo_seleccionado), nombre_empleado, str(hora)]
    worksheet.append_row(nueva_fila)

    st.success("✅ Datos guardados correctamente en la hoja 'TCertificados'.")

# Interfaz de usuario con Streamlit
def main():
    st.title("📋 Registro en Google Sheets")

    fecha_lote = st.date_input("📅 Fecha del lote")
    codigo_seleccionado = st.text_input("🔢 Código seleccionado")
    nombre_empleado = st.text_input("👤 Nombre del empleado")
    hora = st.time_input("⏰ Hora")

    if st.button("Guardar en Google Sheets"):
        guardar_en_google_sheets(fecha_lote, codigo_seleccionado, nombre_empleado, hora)

if __name__ == "__main__":
    main()
