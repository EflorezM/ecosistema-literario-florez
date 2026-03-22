import streamlit as st

st.set_page_config(page_title="Ecosistema Literario", page_icon="📚", layout="wide")

# --- ENCABEZADO PRINCIPAL ---
st.title("📚 Bienvenidos al Ecosistema Literario Transmedia")
st.subheader("El futuro del Plan Lector ha llegado a tu colegio.")
st.markdown("---")

# --- MENSAJE DE BIENVENIDA Y ENGANCHE ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 🚀 Más que un libro, una experiencia inmersiva
    Estimados directores, docentes y estudiantes:
    
    Leer ya no es una actividad de una sola vía. El **Ecosistema Literario de ICREA EDITORES** transforma el Plan Lector tradicional en una aventura gamificada, diseñada para conectar con las nuevas generaciones y facilitar el trabajo en el aula.
    
    Aquí, la literatura se encuentra con la tecnología. Nuestros libros impresos y digitales son la puerta de entrada a esta plataforma exclusiva donde evaluamos la comprensión, fomentamos el pensamiento crítico y construimos valores.
    """)

with col2:
    st.info("""
    **👨‍🏫 Autor y Director:**
    Eduardo Florez Montero
    
    **📖 Catálogo Actual:**
    Más de 20 obras literarias divididas en 4 niveles (Desde Primeros Lectores hasta Jóvenes Adultos).
    """)

st.markdown("---")

# --- VENTAJAS (EL ARGUMENTO DE VENTA PARA EL COLEGIO) ---
st.markdown("### 🎯 ¿Por qué elegir nuestro Ecosistema?")

col_v1, col_v2, col_v3 = st.columns(3)

with col_v1:
    st.success("**⏱️ Cero carga para el Docente**")
    st.write("Olvídate de redactar y calificar exámenes a mano. El sistema evalúa automáticamente mediante rúbricas y entrega la evidencia lista en formato Word.")

with col_v2:
    st.warning("**🧠 Evaluación DUA (3 Niveles)**")
    st.write("Nuestras fichas incluyen nivel Literal, Inferencial y Crítico, adaptándose a los diferentes ritmos de aprendizaje de los estudiantes.")

with col_v3:
    st.error("**🔒 Seguridad Anti-copia**")
    st.write("Con candados por contraseñas de colegio, cronómetros de tiempo y preguntas de argumentación personal que bloquean el plagio.")

st.markdown("---")

# --- INSTRUCCIONES PARA EL ESTUDIANTE ---
st.markdown("### 🛠️ Instrucciones de uso para el Estudiante")
st.markdown("""
1. 👈 **Busca tu libro:** Abre el menú lateral a la izquierda y selecciona la obra que estás leyendo.
2. 🔑 **Ingresa tu Clave:** Escribe la contraseña secreta que te entregó tu profesor (o que viene en tu libro).
3. 🎬 **Disfruta el viaje:** Mira el booktrailer exclusivo, activa el reloj y responde los retos con tus propias palabras.
4. 📥 **Descarga y entrega:** Haz clic en "Generar Evidencia", descarga tu documento Word y envíaselo a tu maestro. ¡Así de fácil!
""")

st.markdown("---")
st.caption("© 2026 Ecosistema Literario Transmedia - Todos los derechos reservados. El uso de esta plataforma es exclusivo para instituciones afiliadas a nuestro Plan Lector.")
