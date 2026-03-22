import streamlit as st
import time
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import streamlit.components.v1 as components

st.set_page_config(page_title="Chepeconde - Plan Lector", page_icon="📖", layout="centered")

# --- FUNCIONES DE BLOQUEO ---
def bloquear_ficha():
    st.session_state.ficha_completada = True

if 'ficha_completada' not in st.session_state:
    st.session_state.ficha_completada = False

# Si el alumno ya descargó, se bloquea toda la app
if st.session_state.ficha_completada:
    st.error("🔒 **EVALUACIÓN BLOQUEADA**")
    st.success("Has generado y descargado tu evidencia con éxito. Por motivos de seguridad y evaluación, solo se permite un intento por estudiante.")
    st.info("Por favor, envía el archivo Word que se descargó en tu computadora/celular a tu profesor.")
    st.stop()

# --- 1. LA BÓVEDA DE SEGURIDAD ---
if 'autenticado_chepe' not in st.session_state:
    st.session_state.autenticado_chepe = False

if not st.session_state.autenticado_chepe:
    st.title("📖 Ecosistema Literario Transmedia")
    st.subheader("Obra: El Pueblo de Chepeconde")
    st.write("Autor: Eduardo Florez Montero")
    st.markdown("---")
    st.info("🔒 **Acceso Exclusivo:** Escribe la Clave de Aula que te indicó tu profesor.")
    
    clave = st.text_input("🔑 Clave de Acceso:", type="password", autocomplete="new-password")
    
    if st.button("Desbloquear Evaluación", use_container_width=True):
        claves_validas = ["CHEPECONDE-2026", "AGUSTIN-2A", "CARMELITAS-3B"]
        if clave in claves_validas: 
            st.session_state.autenticado_chepe = True
            st.rerun()
        else:
            st.error("❌ Clave incorrecta. Si tienes problemas, consulta con tu profesor.")
    st.stop()

# --- 2. SISTEMA DE TIEMPO INTELIGENTE ---
if 'ficha_iniciada_chepe' not in st.session_state:
    st.session_state.ficha_iniciada_chepe = False

if not st.session_state.ficha_iniciada_chepe:
    st.success("✅ ¡Clave aceptada! Bienvenido al ecosistema de El Pueblo de Chepeconde.")
    
    # ADVERTENCIA GIGANTE DE INTENTO ÚNICO
    st.warning("⚠️ **ATENCIÓN: TIENES UN SOLO INTENTO**\nLee atentamente cada pregunta. Una vez que generes tu documento Word al final de la prueba, el sistema se bloqueará y no podrás volver a ingresar ni corregir tus respuestas.")
    
    st.info("👋 Tienes 20 minutos para resolver tu evaluación de comprensión. Presiona iniciar cuando estés 100% seguro.")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🚀 ESTOY LISTO, INICIAR EVALUACIÓN", use_container_width=True, type="primary"):
            st.session_state.ficha_iniciada_chepe = True
            st.session_state.inicio_tiempo_chepe = time.time()
            st.session_state.minutos_asignados_chepe = 20
            st.rerun()
    st.stop()

segundos_transcurridos = time.time() - st.session_state.inicio_tiempo_chepe
segundos_restantes = (st.session_state.minutos_asignados_chepe * 60) - segundos_transcurridos
tiempo_agotado = segundos_restantes <= 0
bloquear_inputs = tiempo_agotado 

# --- MENÚ LATERAL: RELOJ VISUAL ---
with st.sidebar:
    st.markdown("### ⏱️ Tiempo Restante")
    if not tiempo_agotado:
        reloj_html = f"""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #e0e4eb;">
            <h2 id="reloj" style="margin: 0; color: #2ecc71; font-family: monospace; font-size: 38px;">--:--</h2>
        </div>
        <script>
            var tiempo = {int(segundos_restantes)};
            var display = document.getElementById('reloj');
            var intervalo = setInterval(function() {{
                if (tiempo <= 0) {{
                    clearInterval(intervalo);
                    display.innerHTML = "00:00";
                    display.style.color = "#e74c3c";
                }} else {{
                    var min = Math.floor(tiempo / 60).toString().padStart(2, '0');
                    var sec = (tiempo % 60).toString().padStart(2, '0');
                    display.innerHTML = min + ":" + sec;
                    if (tiempo <= 300) display.style.color = "#f39c12"; 
                    if (tiempo <= 60) display.style.color = "#e74c3c"; 
                    tiempo--;
                }}
            }}, 1000);
        </script>
        """
        components.html(reloj_html, height=85)
    else:
        st.error("## 00:00\n⚠️ TIEMPO AGOTADO")
        st.write("Tu ficha ha sido bloqueada. Descarga tu avance abajo.")

# --- 3. CONTENIDO LITERARIO ---
st.markdown("### 📖 EL PUEBLO DE CHEPECONDE")
st.markdown("**Autor:** Eduardo Florez Montero | **Categoría:** Pre-Adolescentes")
st.markdown("---")

institucion = st.text_input("Institución Educativa (Nombre completo):", disabled=bloquear_inputs)

col1, col2, col3 = st.columns(3)
with col1: nombre = st.text_input("Estudiante (Apellidos y Nombres):", disabled=bloquear_inputs)
with col2: nivel = st.selectbox("Nivel:", ["", "Primaria", "Secundaria"], disabled=bloquear_inputs)
with col3: grado = st.selectbox("Grado:", ["", "1ro", "2do", "3ro", "4to", "5to", "6to"], disabled=bloquear_inputs)

col4, col5 = st.columns(2)
with col4: seccion = st.selectbox("Sección:", ["", "A", "B", "C", "D", "E", "F", "G", "H", "Única"], disabled=bloquear_inputs)
with col5: fecha = st.text_input("Fecha:", disabled=bloquear_inputs)

st.markdown("---")
st.subheader("NIVEL 1: COMPRENSIÓN LITERAL")
q1 = st.text_input("1) ¿Quién es el personaje principal y cuál es su mayor característica?", disabled=bloquear_inputs)
q2 = st.text_area("2) Según el inicio del libro, describe brevemente cómo es El Pueblo de Chepeconde:", disabled=bloquear_inputs)

st.markdown("---")
st.subheader("NIVEL 2: ANÁLISIS E INFERENCIA (Requiere desarrollo)")
q3 = st.text_area("3) ¿Por qué crees que el protagonista tomó esa decisión difícil? ¿Qué hubieras hecho tú?", disabled=bloquear_inputs)
q4 = st.text_input("4) Identifica el conflicto principal de la historia. ¿Era un problema interno o externo?", disabled=bloquear_inputs)

st.markdown("---")
st.subheader("NIVEL 3: VALORACIÓN CRÍTICA (Requiere desarrollo)")
q5 = st.text_area("5) Reflexión profunda: ¿Qué enseñanza o valor nos deja la historia de Chepeconde para la sociedad actual?", disabled=bloquear_inputs)

st.markdown("---")

# AVISO FINAL ANTES DE DESCARGAR
st.error("🚨 **ÚLTIMO PASO:** Revisa bien tus respuestas. Al hacer clic en el botón de abajo, se generará tu Word y el sistema bloqueará tu acceso permanentemente.")

# LOGICA DE GENERACIÓN DE WORD
if not institucion.strip() or not nombre.strip() or nivel == "" or grado == "" or seccion == "" or not q1.strip() or not q2.strip() or not q3.strip() or not q4.strip() or not q5.strip():
    st.warning("Completa todos tus datos y respuestas para habilitar la descarga.")
else:
    doc = Document()
    title = doc.add_heading('EVALUACIÓN DEL PLAN LECTOR', level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    inst_paragraph = doc.add_paragraph()
    inst_paragraph.add_run(f'I.E.: {institucion.upper()}').bold = True
    inst_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph('Obra: El Pueblo de Chepeconde | Autor: Eduardo Florez Montero').alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph('_' * 50).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(f'Estudiante: {nombre}\nNivel: {nivel} | Grado: {grado} | Sección: {seccion} | Fecha: {fecha}')
    doc.add_heading('NIVEL 1 (Literal)', level=2)
    doc.add_paragraph('1) ¿Quién es el personaje principal y cuál es su mayor característica?').bold = True
    doc.add_paragraph(f'Respuesta: {q1}\n')
    doc.add_paragraph('2) Describe brevemente cómo es El Pueblo de Chepeconde:').bold = True
    doc.add_paragraph(f'Respuesta: {q2}\n')
    doc.add_heading('NIVEL 2 (Inferencia)', level=2)
    doc.add_paragraph('3) ¿Por qué crees que el protagonista tomó esa decisión difícil? ¿Qué hubieras hecho tú?').bold = True
    doc.add_paragraph(f'Respuesta: {q3}\n')
    doc.add_paragraph('4) Identifica el conflicto principal de la historia. ¿Era un problema interno o externo?').bold = True
    doc.add_paragraph(f'Respuesta: {q4}\n')
    doc.add_heading('NIVEL 3 (Crítico)', level=2)
    doc.add_paragraph('5) ¿Qué enseñanza o valor nos deja la historia de Chepeconde para la sociedad actual?').bold = True
    doc.add_paragraph(f'Respuesta: {q5}\n')
    doc.add_page_break()
    doc.add_heading('Lista de Cotejo - Evaluación del Docente', level=2)
    doc.add_paragraph('Instrucción para el docente: Marque con una (X) el nivel de logro alcanzado por el estudiante.\n')
    table = doc.add_table(rows=1, cols=5)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'CRITERIOS DE EVALUACIÓN'
    hdr_cells[1].text = 'INICIO'
    hdr_cells[2].text = 'PROCESO'
    hdr_cells[3].text = 'LOGRADO'
    hdr_cells[4].text = 'DESTACADO'
    criterios = [
        "NIVEL 1: Identifica correctamente personajes y describe escenarios basándose en la obra.",
        "NIVEL 2: Analiza los motivos y clasifica los conflictos internos o externos de la trama.",
        "NIVEL 3: Argumenta sólidamente una reflexión ética o social vinculada al texto."
    ]
    for crit in criterios:
        row_cells = table.add_row().cells
        row_cells[0].text = crit
        row_cells[1].text = "[   ]"
        row_cells[2].text = "[   ]"
        row_cells[3].text = "[   ]"
        row_cells[4].text = "[   ]"
    doc.add_paragraph('\nObservaciones / Feedback al estudiante:')
    doc.add_paragraph('__________________________________________________________________________________')
    
    bio = io.BytesIO()
    doc.save(bio)
    
    # EL BOTÓN AHORA TIENE LA FUNCION "on_click=bloquear_ficha"
    st.download_button(
        label="📥 Generar y Descargar mi Evidencia", 
        data=bio.getvalue(), 
        file_name=f"Chepeconde_{grado}_{seccion}_{nombre.replace(' ', '_')}.docx", 
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        on_click=bloquear_ficha,
        type="primary"
    )
