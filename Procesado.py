from __future__ import print_function
from googleapiclient.discovery import build
from Credenciales import Obtener_credenciales
from ETL import Carga_JSON, Procesar_PDF
from datetime import datetime

SCOPES = {
    'calendar': 'https://www.googleapis.com/auth/calendar',
    'tasks': 'https://www.googleapis.com/auth/tasks',
}

# Cargar datos una sola vez
datos_cargados = Carga_JSON()

# Función para obtener credenciales y servicio
def obtener_servicio(usuario, tipo, credencial, version):
    creds = Obtener_credenciales(credencial=credencial, scope=SCOPES[tipo], tipo=tipo, usuario=usuario)
    return build(tipo, version, credentials=creds)

# Función para procesar las citas
def Procesar_Citas(usuario, tipo, credencial, version, Funcion, Mes='03', Anno='2025'):
    print(f'------ Citas {usuario} ------')
    service = obtener_servicio(usuario, tipo, credencial, version)
    
    dias_modificados = []
    
    for dia, horario in datos_cargados[f"Citas_{usuario}"].items():
        data = datos_cargados["Datos_Evento"].get(horario)
        if data:
            if usuario not in data["summary"]:
                data["summary"] = f'{data["summary"]} {usuario}'
            
            if usuario == 'cita45':
                data["color"] = "2"
                hora_mod = data["hora_end"].split(':')
                minutos = str(int(hora_mod[1]) + 15)
                if minutos == "60":
                    hora_mod[0] = str(int(hora_mod[0]) + 1)
                    minutos = "00"
                data["hora_end"] = f"{hora_mod[0]}:{minutos}:{hora_mod[2]}"
            
            fecha = f"{Anno}-{Mes}-{dia}"
            dias_modificados.append(Funcion(service=service, data=data, Fecha=fecha))
            data["summary"] = ''  # Reset summary after processing

    if not dias_modificados:
        print('No se modificaron los días.')
    else:
        print(f"Días Modificados:", *dias_modificados, sep=" ")
    print(f'Tareas creadas: Horario {usuario}')
    return dias_modificados

# Función para procesar el horario (calendario)
def Procesar(usuario, tipo, credencial, version, Funcion):
    print(f'------ Horario {usuario} ------')
    service = obtener_servicio(usuario, tipo, credencial, version)
    
    dias_modificados = []

    # Información extraída del PDF
    datos_pdf = Procesar_PDF()
    
    for (col1, fecha), (col2, hora) in zip(datos_pdf.iloc[0].items(), datos_pdf.iloc[1].items()):
        data = datos_cargados["Datos_Evento"].get(hora)
        if data and data['summary'] not in ['Libre', "Libre (Vacaciones)"]:
            dias_modificados.append(Funcion(service=service, data=data, Fecha=fecha))
    
    if not dias_modificados:
        print('No se modificaron los días.')
    else:
        print(f"Días Modificados:", *dias_modificados, sep=" ")

    print(f'Tareas creadas: Horario {usuario}')
    return dias_modificados
