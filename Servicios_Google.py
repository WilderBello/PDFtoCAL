def Tarea_Calendario(service, data, Fecha):
    task = {
        'title': data['summary'],
        # Fecha de vencimiento en formato ISO 8601
        'due': f'{Fecha}T07:00:00.000Z'
    }

    service.tasks().insert(tasklist='@default', body=task).execute()
    return Fecha

def Evento_Calendario(service, data, Fecha):
    event = {
        'summary': data['summary'],
        'start': {
            'dateTime': f'{Fecha}T{data["hora_start"]}',
            'timeZone': 'Europe/Vienna',
        },
        'end': {
            'dateTime': f'{Fecha}T{data["hora_end"]}',
            'timeZone': 'Europe/Vienna',
        },
        'colorId': data["color"],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 1},
            ],
        },
    }
    
    service.events().insert(calendarId='primary', body=event).execute()
    return Fecha