import os
import json
import pdfplumber
import pandas as pd

# Traduccion de aleman a ingles para la fecha en pandas.
def traducir_mes_aleman(mes_str):
    traducciones = {
        "Januar": "January",
        "Februar": "February",
        "März": "March",
        "April": "April",
        "Mai": "May",
        "Juni": "June",
        "Juli": "July",
        "August": "August",
        "September": "September",
        "Oktober": "October",
        "November": "November",
        "Dezember": "December"
    }

    for aleman, ingles in traducciones.items():
        if aleman in mes_str:
            return mes_str.replace(aleman, ingles)
    
    return mes_str

# Función para verificar y modificar el formato de las celdas
def modificar_celda(valor):
    if isinstance(valor, str) and '\n' in valor:
        lineas = [x.strip().lower() for x in valor.split('\n')]
        if len(lineas) > 2 and 'fb' in lineas:
            return f'{lineas[1]}-{lineas[lineas.index("fb")]}'
        elif len(lineas) == 2:
            return lineas[1] if 'f' in lineas else f'{lineas[0]}-{lineas[1]}'
    return valor  # Retorna el valor original si no cumple las condiciones

def Problema_Fecha(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        table = pdf.pages[0].extract_table()
    
    try:
        # print("Formato Noviembre de 2024")
        # PDF de Noviembre 2024
        df_plumber = pd.DataFrame(table[1:], columns=table[0]).drop(columns=[table[0][0]])  # Elimina primera columna
        # Fecha en string
        fecha_str = df_plumber.iloc[0, 0].replace("\n", " ")
        # Limpiar el DataFrame eliminando la primera fila y columna innecesaria
        df_plumber = df_plumber.iloc[1:, 1:].reset_index(drop=True)

    except Exception as e:
        # print("Error con formato de Noviembre, usando formato alternativo:", e)
        # PDF de Abril 2025
        df_plumber = pd.DataFrame(table[1:], columns=table[0])
        # Eliminando las ultimas 4 columnas
        df_plumber = df_plumber.iloc[:,:-4]
        # Fecha en string
        fecha_str = df_plumber.columns[0].replace("\n", " ")
        # Eliminando dos primeras filas
        df_plumber = df_plumber.iloc[:, 2:].reset_index(drop=True)

    # Traducir mes si está en alemán
    fecha_str = traducir_mes_aleman(fecha_str)

    # Pasar el dataframe a excel en formato csv.
    # df_plumber.to_csv("dataframe_completo.csv", index=False)
    
    return df_plumber, fecha_str

def Procesar_PDF():
    df_plumber, fecha_str = Problema_Fecha(pdf_path="GGZ Intranet.pdf")

    # print(fecha_str)

    # Obtener el mes y año de la primera celda
    fecha = pd.to_datetime(fecha_str, format="%B %Y")
    print(f"Fecha base: {fecha}")

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
    df_plumber.to_csv("Horario_en_excel.csv", index=False)
    
    return df_plumber

def Carga_JSON():
    datos_cargados = {}
    archivos = ["Datos_Evento"]

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