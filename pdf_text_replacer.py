import fitz  # PyMuPDF

def buscar_palabra_exacta(texto, palabra, ignorar_mayusculas):
    """
    Busca una palabra en el texto respetando si es palabra completa.
    Devuelve una lista de tuplas con las posiciones (inicio, fin).
    """
    resultados = []
    inicio = 0
    
    while True:
        if ignorar_mayusculas:
            pos = texto.lower().find(palabra.lower(), inicio)
        else:
            pos = texto.find(palabra, inicio)
            
        if pos == -1:
            break
            
        # Verificar que es una palabra completa
        antes = pos == 0 or not texto[pos-1].isalnum()
        despues = pos + len(palabra) >= len(texto) or not texto[pos + len(palabra)].isalnum()
        
        if antes and despues:
            # Si no ignoramos mayúsculas, verificar que coincide exactamente
            if not ignorar_mayusculas:
                if texto[pos:pos + len(palabra)] != palabra:
                    inicio = pos + 1
                    continue
            resultados.append((pos, pos + len(palabra)))
        
        inicio = pos + 1
        
    return resultados

def reemplazar_texto_pdf(ruta_entrada, ruta_salida, palabra_buscar, palabra_reemplazar, ignorar_mayusculas=False):
    """
    Busca y reemplaza texto en un archivo PDF manteniendo el formato original.
    
    Args:
        ruta_entrada (str): Ruta del archivo PDF original
        ruta_salida (str): Ruta donde guardar el nuevo PDF
        palabra_buscar (str): Palabra a buscar
        palabra_reemplazar (str): Palabra con la que reemplazar
        ignorar_mayusculas (bool): Si True, ignora mayúsculas/minúsculas en la búsqueda
    """
    try:
        # Abrir el documento
        doc = fitz.open(ruta_entrada)
        
        # Contador para el número de reemplazos
        total_reemplazos = 0
        
        # Procesar cada página
        for pagina in doc:
            # Obtener el texto completo de la página
            texto_pagina = pagina.get_text()
            
            # Encontrar todas las posiciones de la palabra
            posiciones = buscar_palabra_exacta(texto_pagina, palabra_buscar, ignorar_mayusculas)
            
            # Para cada posición encontrada
            for inicio, fin in posiciones:
                # Obtener el texto exacto que coincidió
                texto_encontrado = texto_pagina[inicio:fin]
                
                # Buscar esta ocurrencia específica en la página
                instances = pagina.search_for(texto_encontrado)
                
                # Procesar cada instancia encontrada
                for inst in instances:
                    # Verificar el texto exacto en esta posición
                    rect_texto = pagina.get_text("text", clip=inst)
                    if rect_texto.strip() == texto_encontrado:
                        # Crear un rectángulo blanco sobre el texto original
                        pagina.draw_rect(inst, color=(1, 1, 1), fill=(1, 1, 1))
                        
                        # Calcular la posición vertical correcta
                        baseline = inst.y1 - (inst.height * 0.2)
                        
                        # Insertar el nuevo texto
                        fontsize = inst.height * 0.85
                        text_point = fitz.Point(inst.x0, baseline)
                        pagina.insert_text(
                            text_point,
                            palabra_reemplazar,
                            fontsize=fontsize,
                            color=(0, 0, 0)
                        )
                        total_reemplazos += 1
        
        # Guardar el documento modificado
        doc.save(ruta_salida)
        doc.close()
        
        return total_reemplazos
    
    except Exception as e:
        raise Exception(f"Error al procesar el PDF: {str(e)}")

if __name__ == "__main__":
    try:
        ruta_entrada = input("Introduce la ruta del PDF original: ")
        ruta_salida = input("Introduce la ruta donde guardar el nuevo PDF: ")
        palabra_buscar = input("Introduce la palabra a buscar: ")
        palabra_reemplazar = input("Introduce la palabra de reemplazo: ")
        ignorar_mayusculas = input("¿Ignorar mayúsculas/minúsculas? (s/n): ").lower() == 's'
        
        total = reemplazar_texto_pdf(ruta_entrada, ruta_salida, palabra_buscar, palabra_reemplazar, ignorar_mayusculas)
        print(f"Proceso completado. Se realizaron {total} reemplazos.")
        print(f"PDF guardado en: {ruta_salida}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
