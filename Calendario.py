from __future__ import print_function
from Servicios_Google import Tarea_Calendario, Evento_Calendario
from Procesado import Procesar, Procesar_Citas
from ETL import Procesar_PDF, Problema_Fecha

def Horario_p(Selector):
    opciones = {
        Procesar: ("tasks", "v1", Tarea_Calendario),
        Procesar_Citas: ("calendar", "v3", Evento_Calendario)
    }
    
    if Selector in opciones:
        tipo, version, Funcion = opciones[Selector]
        Selector(usuario='p', tipo=tipo, credencial='./credenciales_json/credentials_p.json', version=version, Funcion=Funcion)

def Horario_w(Selector):
    Selector(usuario='w', tipo='calendar',
             credencial='./credenciales_json/credentials_w.json', version='v3', Funcion=Evento_Calendario)

if __name__ == '__main__':
    
    df, fecha = Problema_Fecha(pdf_path="GGZ Intranet.pdf")
    print(fecha)

    print('Datos a procesar: ')
    print(Procesar_PDF())

    corroborar = input('La fecha a procesar es la anterior y los datos a procesar son los mostrados. \nEs correcto? (Y/N): ').strip().lower()

    if corroborar in {'y', 'yes'}:
        Selector = Procesar
        Horario_w(Selector=Selector)
        Horario_p(Selector=Selector)
        print('\nTareas finalizadas correctamente......')

    elif corroborar == 'p':
        print("Zona de Prueba...")
        # Horario_w(Selector=Procesar)
        print(Procesar_PDF())

    else:
        print('Por favor corrobore la fecha a ingresar.')
