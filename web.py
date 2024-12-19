def application (environ, start_response):
    headers = [('Content-type', 'text/html; charset=utf-8')]
    if environ ['PATH_INFO'] == "/" :
        respuesta = "<p>Pagina Principal</p>"
    elif environ ['PATH_INFO'] == "/bienvenida" :
        respuesta = "<p>Pagina Bienvenida</p>"
    #Suma
    elif environ ['PATH_INFO'] == "/suma" :
        param = environ ['QUERY_STRING'].split('&')
        respuesta=""
        suma = 0
        for param in param:
            respuesta += '<p>Me has pasado el siguiente valor:' + param[0] + '</p>'	
            suma += int(param)
        respuesta += '<p>La suma total es: ' + str(suma) + '</p>'
    #Resta
    elif environ ['PATH_INFO'] == "/resta" :
        param = environ ['QUERY_STRING'].split('&')
        respuesta=""
        resta = int(param[0])
        respuesta += '<p>Me has pasado el siguiente valor:' + param[0] + '</p>'
        for param in param[1:]:
            respuesta += '<p>Me has pasado el siguiente valor:' + param + '</p>'	
            resta -= int(param)
        respuesta += '<p>La resta total es: ' + str(resta) + '</p>'
    #Multiplicacion
    elif environ ['PATH_INFO'] == "/multi" :
        param = environ ['QUERY_STRING'].split('&')
        respuesta=""
        multiplicacion = 1
        for param in param:
            respuesta += '<p>Me has pasado el siguiente valor:' + param + '</p>'	
            multiplicacion *= int(param)
        respuesta += '<p>La multiplicacion total es: ' + str(multiplicacion) + '</p>'
    #Division
    elif environ ['PATH_INFO'] == "/divi" :
        param = environ ['QUERY_STRING'].split('&')
        respuesta=""
        division = int(param[0])
        respuesta += '<p>Me has pasado el siguiente valor:' + param[0] + '</p>'
        for param in param[1]:
            respuesta += '<p>Me has pasado el siguiente valor:' + param + '</p>'	
            division /= int(param)
        respuesta += '<p>La division total es: ' + str(division) + '</p>'
    else:
        respuesta = "<p>No hay ninguna pagina</p>"
    start_response('200 OK', headers)
    return [respuesta.encode('utf-8')]

from wsgiref.simple_server import make_server

server = make_server('localhost', 9000, application)
server.serve_forever()

