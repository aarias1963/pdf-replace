import streamlit as st
import fitz  # PyMuPDF
import io
import tempfile
import os

# Importar las funciones del script original
from pdf_text_replacer import buscar_palabra_exacta, reemplazar_texto_pdf

def main():
    st.title("Reemplazador de Texto en PDF")

    # Subir archivo PDF
    uploaded_file = st.file_uploader("Sube tu archivo PDF", type="pdf", label="Seleccionar PDF")

    if uploaded_file is not None:
        # Crear un archivo temporal para guardar el PDF subido
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        # Campos de entrada
        palabra_buscar = st.text_input("Palabra a buscar:")
        palabra_reemplazar = st.text_input("Palabra de reemplazo:")
        ignorar_mayusculas = st.checkbox("Ignorar mayúsculas/minúsculas")

        if st.button("Procesar PDF"):
            try:
                # Crear un archivo temporal para el PDF de salida
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_output_file:
                    output_path = tmp_output_file.name

                # Ejecutar la función de reemplazo
                total_reemplazos = reemplazar_texto_pdf(
                    tmp_file_path, output_path, palabra_buscar, palabra_reemplazar, ignorar_mayusculas
                )

                st.success(f"Proceso completado. Se realizaron {total_reemplazos} reemplazos.")

                # Leer el archivo PDF modificado
                with open(output_path, "rb") as file:
                    btn = st.download_button(
                        label="Descargar PDF modificado",
                        data=file,
                        file_name="pdf_modificado.pdf",
                        mime="application/pdf"
                    )

            except Exception as e:
                st.error(f"Error al procesar el PDF: {str(e)}")

            finally:
                # Limpiar archivos temporales
                os.unlink(tmp_file_path)
                if 'output_path' in locals():
                    os.unlink(output_path)

if __name__ == "__main__":
    main()
