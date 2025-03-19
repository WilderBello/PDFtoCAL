import os
import json
import pdfplumber
import pandas as pd

# Función para verificar y modificar el formato de las celdas
def modificar_celda(valor):
    if isinstance(valor, str) and '\n' in valor:
        lineas = [x.strip().lower() for x in valor.split('\n')]
        if len(lineas) > 2 and 'fb' in lineas:
            return f'{lineas[1]}-{lineas[lineas.index("fb")]}'
        elif len(lineas) == 2:
            return lineas[1] if 'f' in lineas else f'{lineas[0]}-{lineas[1]}'
    return valor  # Retorna el valor original si no cumple las condiciones

def Procesar_PDF(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        table = pdf.pages[0].extract_table()
    
    # PDF de Noviembre 2024
    # df_plumber = pd.DataFrame(table[1:], columns=table[0]).drop(columns=[table[0][0]])  # Elimina primera columna
    # Fecha en string
    # fecha_str = df_plumber.iloc[0, 0].replace("\n", " ")

    # PDF de Abril 2025
    df_plumber = pd.DataFrame(table[1:], columns=table[0])
    # Eliminando las ultimas 4 columnas
    df_plumber = df_plumber.iloc[:,:-4]
    # Fecha en string
    fecha_str = df_plumber.columns[0].replace("\n", " ")

    # Obtener el mes y año de la primera celda
    fecha = pd.to_datetime(fecha_str, format="%B %Y")
    print(f"Fecha base: {fecha}")
    
    # Limpiar el DataFrame eliminando la primera fila y columna innecesaria ------------ Noviembre 2024
    # df_plumber = df_plumber.iloc[1:, 1:].reset_index(drop=True)

    # Eliminando dos primeras filas ---- Abril 2025
    df_plumber = df_plumber.iloc[:, 2:].reset_index(drop=True)

    # Establecer nombres de columnas y eliminar columnas vacías
    df_plumber.columns = df_plumber.iloc[0]
    df_plumber = df_plumber.loc[:, df_plumber.columns.notna() & (df_plumber.columns != '')]

    # Convertir la primera fila en fechas sin hora
    df_plumber.loc[0, :] = pd.to_datetime([f"{fecha.year}-{fecha.month:02d}-{dia}" for dia in df_plumber.columns]).date

    # Mantener solo las dos primeras filas
    df_plumber = df_plumber.head(2).reset_index(drop=True)

    # Modificando dia 4
    # df_plumber.loc[1, '04'] = 'F \nFB'

    # Verificar si hay saltos de línea antes de aplicar modificaciones
    if df_plumber.map(lambda x: isinstance(x, str) and '\n' in x).any().any():
        df_plumber = df_plumber.map(modificar_celda)

    # Convertir segunda fila a minúsculas
    df_plumber.loc[1, :] = df_plumber.loc[1, :].astype(str).str.lower()

    # Exportar a CSV
    # df_plumber.to_csv("dataframe_completo.csv", index=False)
    
    return df_plumber

def Carga_JSON():
    datos_cargados = {}
    archivos = ["Datos_Evento", "Citas_Paula", "Citas_Wilder"]

    for archivo in archivos:
        archivo_json = f'./json/{archivo}.json'
        if os.path.exists(archivo_json):  # Verifica si el archivo existe antes de abrirlo
            try:
                with open(archivo_json, 'r', encoding='utf-8') as archivo_data:
                    datos_cargados[archivo] = json.load(archivo_data)
            except json.JSONDecodeError:
                print(f"Error al leer {archivo_json}: JSON mal formado.")
    
    return datos_cargados

# Procesar_PDF(pdf_path="GGZ Intranet.pdf")