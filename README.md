Nota: 
* Es necesario el entorno pipenv.
* Selectores: Se manejan 2 selectores por el momento, Procesar es para cargar pdf a Calendar y Procesar_Citas es para establecer eventos con solo fecha y hora.

Estructura general:
* Calendario: Es el archivo principal a ejecutar.
* Credenciales: Maneja la obtencion de credenciales.
* ETL: Extrae, Transforma y Carga los datos del PDF y los json.
* Procesado: Procesa cada uno de los eventos o tareas, de acuerdo con lo que se desea.
* Servicios_Google: Rellena los espacios generales y envia el evento o tarea al calendario.

La estructura contiene las siguientes carpetas adicionales:
* credenciales_json: Aloja las credenciales de los usuarios, asi como los token que se obtienen.
* json: Se almacenan todos los datos en formato json con la estructura:
  {
    "evento": {
        "summary": "Nombre evento",
        "hora_start": "07:00:00", # Hora de inicio
        "hora_end": "07:30:00", # Hora de finalizacion
        "color": "5" # color del evento en Calendar
    },
  }
