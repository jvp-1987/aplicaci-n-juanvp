import streamlit as st
from fpdf import FPDF
import os
import pathlib

# Configuración inicial
st.set_page_config(page_title="Escala SALUFAM", layout="wide", initial_sidebar_state="collapsed")
st.title("🏥 Escala SALUFAM - Evaluación de Vulnerabilidad Familiar")
st.markdown("---")

# Campos adicionales con mejor diseño
st.subheader("📋 Información del Evaluador")
col1, col2 = st.columns(2)
with col1:
    fecha = st.date_input("📅 Fecha de la evaluación:")
    entrevistador = st.text_input("👤 Nombre del Entrevistador:")
with col2:
    entrevistado = st.text_input("👤 Nombre del Entrevistado:")
    rut = st.text_input("🆔 RUT del Entrevistado:")

establecimiento = st.selectbox("🏥 Establecimiento:", ["CESFAM Coñaripe", "CECOSF Liquiñe"])
st.markdown("---")

# Obtener la ruta de la carpeta de Descargas
downloads_path = str(pathlib.Path.home() / "Downloads")

preguntas = [
    "Estamos de acuerdo en cómo deben actuar los miembros de nuestra familia.",
    "Estamos de acuerdo en las cosas que son importantes para nuestra familia.",
    "Sabemos qué queremos lograr como familia en el futuro.",
    "Intentamos mirar el lado positivo de las cosas.",
    "Cuando hay un problema, logramos ver los aspectos positivos y negativos.",
    "Intentamos olvidar nuestros problemas durante un tiempo cuando parecen insuperables.",
    "Cada uno de nosotros es capaz de escuchar las dos versiones de una historia.",
    "En nuestra familia tenemos al menos un día en que realizamos alguna actividad todos juntos.",
    "Podemos pedir ayuda a alguien de afuera de nuestra familia si lo necesitamos.",
    "Nuestros amigos y familiares nos ayudarán si lo necesitamos.",
    "Podemos confiar en el apoyo de los demás cuando algo va mal.",
    "A nuestros amigos o familiares les gusta visitarnos.",
    "Hacemos un esfuerzo por ayudar a nuestros parientes cuando lo necesitan."
]

opciones = {"Nunca": 1, "Pocas veces": 2, "Algunas veces": 3, "Muchas veces": 4, "Siempre": 5, "No sabe": 0}

# Capturar respuestas desde la interfaz con mejor presentación
st.subheader("📝 Cuestionario")
respuestas = []
for i, pregunta in enumerate(preguntas):
    respuesta = st.radio(f"**{i+1}.** {pregunta}", opciones.keys(), key=f"preg_{i}", horizontal=True)
    respuestas.append(respuesta)

st.markdown("---")

# Mostrar puntaje solo si todas las respuestas han sido seleccionadas
if None not in respuestas:
    puntaje = sum(opciones[respuesta] for respuesta in respuestas) / len(respuestas)
    st.subheader(f"📊 Puntaje Promedio: {puntaje:.2f}")
    if puntaje <= 3.7:
        st.error("🚨 Alta Vulnerabilidad Familiar en Salud")
    else:
        st.success("🟢 Baja Vulnerabilidad Familiar en Salud")
else:
    puntaje = None

# Función para exportar resultados a un PDF visualmente mejorado en una sola hoja
def exportar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, "Resultados de la Escala SALUFAM", ln=True, align='C')
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 7, f"Fecha: {fecha}", ln=False)
    pdf.cell(95, 7, f"Entrevistador: {entrevistador}", ln=True)
    pdf.cell(95, 7, f"Entrevistado: {entrevistado}", ln=False)
    pdf.cell(95, 7, f"RUT: {rut}", ln=True)
    pdf.cell(200, 7, f"Establecimiento: {establecimiento}", ln=True)
    pdf.ln(5)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(0, 7, "Respuestas del Cuestionario", ln=True, align='C', fill=True)
    pdf.ln(3)
    pdf.set_font("Arial", size=9)
    for i, pregunta in enumerate(preguntas):
        pdf.cell(130, 5, f"{i+1}. {pregunta[:50]}...", ln=False)
        pdf.cell(50, 5, f"{respuestas[i]}", ln=True)
    pdf.ln(5)
    if puntaje is not None:
        pdf.set_font("Arial", style='B', size=10)
        pdf.cell(200, 7, f"Puntaje Promedio: {puntaje:.2f}", ln=True, align='C')
        if puntaje <= 3.7:
            pdf.set_text_color(255, 0, 0)
            pdf.cell(200, 7, "Resultado: Alta Vulnerabilidad Familiar en Salud", ln=True, align='C')
        else:
            pdf.set_text_color(0, 128, 0)
            pdf.cell(200, 7, "Resultado: Baja Vulnerabilidad Familiar en Salud", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf_path = os.path.join(downloads_path, f"{rut}_resultado_salufam.pdf")
    pdf.output(pdf_path)
    return pdf_path

# Botón para descargar el PDF
if None not in respuestas:
    with open(exportar_pdf(), "rb") as f:
        st.download_button("📥 Descargar PDF", f, file_name=f"{rut}_resultado_salufam.pdf", mime="application/pdf")

st.write("💡 Aplicación optimizada para la evaluación de la vulnerabilidad familiar en salud con la Escala SALUFAM.")
