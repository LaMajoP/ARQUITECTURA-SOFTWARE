# Patrones de Resiliencia

## Que es la resiliencia en una arquitectura de servicios

Cuando un sistema depende de servicios externos, siempre existe la posibilidad de que esos servicios fallen, se demoren o no esten disponibles. La resiliencia es la capacidad del sistema de seguir funcionando de forma controlada ante esos escenarios, en lugar de fallar completamente.

## Patrones implementados

### Timeout

Este patron establece un tiempo maximo de espera para cada llamada al servicio externo. Si el Servicio B no responde dentro de 2 segundos, la solicitud se cancela automaticamente. Esto evita que el Servicio Principal quede bloqueado esperando una respuesta que podria no llegar.

### Retry

Si una llamada al Servicio B falla (ya sea por timeout o por un error de conexion), el sistema reintenta la solicitud hasta 3 veces antes de darse por vencido. Entre cada intento se espera 1 segundo. Esto permite recuperarse de fallos temporales como picos de carga o interrupciones breves en la red.

### Fallback

Si despues de los 3 intentos el Servicio B sigue sin responder, el sistema no lanza un error al usuario. En su lugar, devuelve una lista vacia de materias sugeridas y continua con el calculo del promedio normalmente. El usuario recibe su resultado sin interrupciones, aunque sin la informacion complementaria del Servicio B.

## Donde se aplican

Estos tres patrones se aplican en la funcion que conecta al Servicio Principal con el Servicio B, y se evidencian en los dos endpoints que realizan comunicacion entre servicios: `/promedio` y `/promedio-objetivo`. En ambos casos, la llamada al servicio externo pasa por el mismo mecanismo de Timeout, Retry y Fallback.
