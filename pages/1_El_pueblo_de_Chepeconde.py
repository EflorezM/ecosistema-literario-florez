import streamlit as st
import time
from datetime import datetime
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import streamlit.components.v1 as components
import re

st.set_page_config(page_title="Chepeconde - Plan Lector", page_icon="📖", layout="centered")

# --- FUNCIONES DE BLOQUEO Y VALIDACIÓN ---
def bloquear_ficha():
    st.session_state.ficha_completada = True

if 'ficha_completada' not in st.session_state:
    st.session_state.ficha_completada = False

if st.session_state.ficha_completada:
    st.error("🔒 **EVALUACIÓN ENTREGADA Y BLOQUEADA**")
    st.success("Has generado y descargado tu evidencia con éxito. Solo se permite un intento por estudiante.")
    st.info("Por favor, envía el archivo Word que se descargó en tu equipo a tu profesor.")
    st.stop()

def contiene_spam(texto):
    palabras = texto.split()
    for palabra in palabras:
        if len(palabra) > 20: 
            return True
    return False

def obtener_minimos(grado):
    if grado == "1ro":
        return {"q3": 10, "q4": 10, "q5": 10}
    elif grado in ["2do", "3ro"]:
        return {"q3": 12, "q4": 12, "q5": 12}
    return {"q3": 10, "q4": 10, "q5": 10}

# --- 1. LA BÓVEDA DE SEGURIDAD ---
if 'autenticado_chepe' not in st.session_state:
    st.session_state.autenticado_chepe = False

if not st.session_state.autenticado_chepe:
    st.title("📖 Ecosistema Literario Transmedia")
    st.subheader("Obra: El Pueblo de Chepeconde")
    st.write("Autor: Eduardo Florez Montero")
    st.markdown("---")
    st.info("🔒 **Acceso Exclusivo:** Escribe la Clave de Aula que te indicó tu profesor.")
    
    clave = st.text_input("🔑 Clave de Acceso *:", type="password", autocomplete="new-password")
    
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
    st.warning("⚠️ **ATENCIÓN: TIENES UN SOLO INTENTO**\nAl descargar tu Word, el sistema se bloqueará permanentemente. Los campos con asterisco (*) son obligatorios.")
    
    try:
        st.image("portada_chepeconde.jpg", width=250)
    except FileNotFoundError:
        st.caption("(Aquí aparecerá la portada de tu libro)")
        
    st.info("👋 Tienes 20 minutos para resolver tu evaluación.")
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

# --- MENÚ LATERAL: RELOJ VISUAL Y AVISO DE 30 SEGUNDOS ---
with st.sidebar:
    st.markdown("### ⏱️ Tiempo Restante")
    if not tiempo_agotado:
        reloj_html = f"""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #e0e4eb;">
            <h2 id="reloj" style="margin: 0; color: #2ecc71; font-family: monospace; font-size: 38px;">--:--</h2>
        </div>
        <div id="aviso_30s" style="color: #e74c3c; font-weight: bold; font-size: 14px; text-align: center; margin-top: 10px; display: none;">
            ⚠️ ¡Aviso! Te quedan 30 segundos. Si necesitas más tiempo, pide 4 min extra abajo. Si no, prepárate para descargar tu avance.
        </div>
        <script>
            var tiempo = {int(segundos_restantes)};
            var display = document.getElementById('reloj');
            var aviso = document.getElementById('aviso_30s');
            var intervalo = setInterval(function() {{
                if (tiempo <= 0) {{
                    clearInterval(intervalo);
                    display.innerHTML = "00:00";
                    display.style.color = "#e74c3c";
                    aviso.innerHTML = "⚠️ Tiempo agotado. Descarga tu avance ahora.";
                    aviso.style.display = "block";
                }} else {{
                    var min = Math.floor(tiempo / 60).toString().padStart(2, '0');
                    var sec = (tiempo % 60).toString().padStart(2, '0');
                    display.innerHTML = min + ":" + sec;
                    
                    if (tiempo <= 300) display.style.color = "#f39c12"; 
                    if (tiempo <= 60) display.style.color = "#e74c3c"; 
                    
                    // Mostrar aviso exacto a los 30 segundos
                    if (tiempo <= 30) {{
                        aviso.style.display = "block";
                    }}
                    
                    tiempo--;
                }}
            }}, 1000);
        </script>
        """
        components.html(reloj_html, height=130)
        
        if st.button("➕ Dar 4 min extra", use_container_width=True):
            st.session_state.minutos_asignados_chepe += 4
            st.rerun()
    else:
        st.error("## 00:00\n⚠️ TIEMPO AGOTADO")
        st.write("Tu ficha ha sido bloqueada. Aún puedes descargar tu avance en la parte inferior.")

# --- 3. CONTENIDO LITERARIO ---
st.markdown("### 📖 EL PUEBLO DE CHEPECONDE")
st.markdown("**Autor:** Eduardo Florez Montero | **Categoría:** Pre-Adolescentes (1ro a 3ro Sec.)")
st.markdown("---")

institucion = st.text_input("Institución Educativa (Nombre completo) *:", disabled=bloquear_inputs)

col1, col2, col3 = st.columns(3)
with col1: nombre = st.text_input("Estudiante (Apellidos y Nombres) *:", disabled=bloquear_inputs)
with col2: nivel = st.selectbox("Nivel *:", ["", "Secundaria"], disabled=bloquear_inputs)
with col3: grado = st.selectbox("Grado *:", ["", "1ro", "2do", "3ro"], disabled=bloquear_inputs)

col4, col5, col6 = st.columns(3)
with col4: seccion = st.selectbox("Sección *:", ["", "A", "B", "C", "D", "E", "F", "G", "H", "Única"], disabled=bloquear_inputs)
with col5: area_curso = st.text_input("Área o Curso (Ej: Comunicación) *:", disabled=bloquear_inputs)
with col6: fecha_input = st.date_input("Fecha *:", disabled=bloquear_inputs)

profesor = st.text_input("Nombre de tu Profesor(a) (Opcional):", disabled=bloquear_inputs)

st.markdown("---")
st.subheader("🎬 Antes de empezar: Resumen Visual")
st.video("https://www.youtube.com/watch?v=123456789") 
st.caption("Mira el clip y responde basándote en la lectura de tu libro.")
st.markdown("---")

st.subheader("NIVEL 1: COMPRENSIÓN LITERAL")
q1 = st.text_input("1) ¿Quién es el personaje principal y cuál es su mayor característica? *", disabled=bloquear_inputs)
q2 = st.text_area("2) Según el inicio del libro, describe brevemente cómo es El Pueblo de Chepeconde: *", disabled=bloquear_inputs)

st.markdown("---")
st.subheader("NIVEL 2: ANÁLISIS E INFERENCIA")
q3 = st.text_area("3) ¿Por qué crees que el protagonista tomó esa decisión difícil? ¿Qué hubieras hecho tú? *", disabled=bloquear_inputs)
q4 = st.text_input("4) Identifica el conflicto principal de la historia. ¿Era un problema interno o externo? *", disabled=bloquear_inputs)

st.markdown("---")
st.subheader("NIVEL 3: VALORACIÓN CRÍTICA")
q5 = st.text_area("5) Reflexión profunda: ¿Qué enseñanza o valor nos deja la historia de Chepeconde para la sociedad actual? *", disabled=bloquear_inputs)

st.markdown("---")

st.error("🚨 **ÚLTIMO PASO:** Al hacer clic en el botón de abajo, se generará tu Word y el sistema bloqueará tu acceso permanentemente.")

# LOGICA INTELIGENTE DE VALIDACIÓN Y DESCARGA
faltantes = []
if not institucion.strip(): faltantes.append("Institución Educativa")
if not nombre.strip(): faltantes.append("Estudiante")
if nivel == "": faltantes.append("Nivel")
if grado == "": faltantes.append("Grado")
if seccion == "": faltantes.append("Sección")
if not area_curso.strip(): faltantes.append("Área o Curso")

# Los datos personales son obligatorios INCLUSO si se acaba el tiempo (para saber de quién es el examen)
if faltantes:
    st.error(f"⚠️ **IMPOSIBLE DESCARGAR. Te falta llenar los siguientes datos obligatorios:** {', '.join(faltantes)}")
else:
    # Verificamos si faltan preguntas, SOLO si aún hay tiempo
    preguntas_vacias = []
    if not q1.strip(): preguntas_vacias.append("Pregunta 1")
    if not q2.strip(): preguntas_vacias.append("Pregunta 2")
    if not q3.strip(): preguntas_vacias.append("Pregunta 3")
    if not q4.strip(): preguntas_vacias.append("Pregunta 4")
    if not q5.strip(): preguntas_vacias.append("Pregunta 5")

    if not tiempo_agotado and preguntas_vacias:
        st.warning(f"⚠️ **AÚN TIENES TIEMPO.** Te falta responder: {', '.join(preguntas_vacias)}.")
    elif not tiempo_agotado and (contiene_spam(q1) or contiene_spam(q2) or contiene_spam(q3) or contiene_spam(q4) or contiene_spam(q5)):
        st.error("⚠️ Hemos detectado caracteres repetidos o 'spam' en tus respuestas. Escribe con normalidad.")
    else:
        # Lógica de conteo de palabras (SOLO exige si hay tiempo)
        minimos = obtener_minimos(grado)
        palabras_q3 = len(q3.split())
        palabras_q4 = len(q4.split())
        palabras_q5 = len(q5.split())
        
        if not tiempo_agotado and palabras_q3 < minimos["q3"] and q3.strip():
            st.error(f"⚠️ Pregunta 3: Necesitas mínimo {minimos['q3']} palabras (tienes {palabras_q3}).")
        elif not tiempo_agotado and palabras_q4 < minimos["q4"] and q4.strip():
            st.error(f"⚠️ Pregunta 4: Necesitas mínimo {minimos['q4']} palabras (tienes {palabras_q4}).")
        elif not tiempo_agotado and palabras_q5 < minimos["q5"] and q5.strip():
            st.error(f"⚠️ Pregunta 5: Necesitas mínimo {minimos['q5']} palabras (tienes {palabras_q5}).")
        else:
            # SI TODO ESTÁ BIEN (O SI EL TIEMPO SE AGOTÓ), SE GENERA EL WORD
            if tiempo_agotado:
                st.info("⏱️ El tiempo se agotó. Descargando tu avance parcial...")
                
            doc = Document()
            title = doc.add_heading('EVALUACIÓN DEL PLAN LECTOR', level=1)
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            inst_paragraph = doc.add_paragraph()
            inst_paragraph.add_run(f'I.E.: {institucion.upper()}').bold = True
            inst_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph('Obra: El Pueblo de Chepeconde | Autor: Eduardo Florez Montero').alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_paragraph('_' * 50).alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            fecha_str = fecha_input.strftime("%d/%m/%Y")
            texto_area = area_curso.strip()
            texto_prof = profesor.strip() if profesor.strip() else "No especificado"

            doc.add_paragraph(f'Estudiante: {nombre}\nNivel: {nivel} | Grado: {grado} | Sección: {seccion} | Fecha: {fecha_str}')
            doc.add_paragraph(f'Área/Curso: {texto_area} | Docente a cargo: {texto_prof}')
            
            doc.add_heading('NIVEL 1 (Literal)', level=2)
            doc.add_paragraph('1) ¿Quién es el personaje principal y cuál es su mayor característica?').bold = True
            doc.add_paragraph(f'Respuesta: {q1 if q1.strip() else "[No respondió]"}\n')
            doc.add_paragraph('2) Describe brevemente cómo es El Pueblo de Chepeconde:').bold = True
            doc.add_paragraph(f'Respuesta: {q2 if q2.strip() else "[No respondió]"}\n')
            
            doc.add_heading('NIVEL 2 (Inferencia)', level=2)
            doc.add_paragraph('3) ¿Por qué crees que el protagonista tomó esa decisión difícil? ¿Qué hubieras hecho tú?').bold = True
            doc.add_paragraph(f'Respuesta: {q3 if q3.strip() else "[No respondió]"}\n')
            doc.add_paragraph('4) Identifica el conflicto principal de la historia. ¿Era un problema interno o externo?').bold = True
            doc.add_paragraph(f'Respuesta: {q4 if q4.strip() else "[No respondió]"}\n')
            
            doc.add_heading('NIVEL 3 (Crítico)', level=2)
            doc.add_paragraph('5) ¿Qué enseñanza o valor nos deja la historia de Chepeconde para la sociedad actual?').bold = True
            doc.add_paragraph(f'Respuesta: {q5 if q5.strip() else "[No respondió]"}\n')
            
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
            
            st.download_button(
                label="📥 Generar y Descargar mi Evidencia", 
                data=bio.getvalue(), 
                file_name=f"Chepeconde_{grado}_{seccion}_{nombre.replace(' ', '_')}.docx", 
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                on_click=bloquear_ficha,
                type="primary"
            )
