# Observabilidad del Sistema

## Que es la observabilidad

La observabilidad permite entender que esta pasando dentro de un sistema en tiempo de ejecucion. En una arquitectura de servicios, donde multiples componentes se comunican entre si, es fundamental poder monitorear el estado de cada servicio, detectar problemas y analizar el rendimiento.

## Herramientas integradas

### Prometheus (recoleccion de metricas)

Prometheus se conecta a ambos servicios y recolecta metricas cada 15 segundos desde el endpoint `/metrics` que cada servicio expone automaticamente. Las metricas incluyen la cantidad de requests recibidos, la latencia de cada endpoint y los codigos de respuesta HTTP. Prometheus se ejecuta como un contenedor Docker en el puerto 9090.

### Grafana (visualizacion de metricas)

Grafana toma los datos recolectados por Prometheus y los presenta en un dashboard visual. El dashboard del proyecto muestra 6 paneles: requests totales, latencia promedio y distribucion de codigos de respuesta, tanto para el Servicio Principal como para el Servicio B. Grafana se ejecuta en el puerto 3000 con las credenciales admin/admin.

### Jaeger (tracing distribuido)

Jaeger permite rastrear el recorrido completo de una solicitud a traves de los servicios. Cuando un cliente hace una peticion a `/promedio`, Jaeger registra un trace que muestra cuanto tardo el Servicio Principal, cuanto tardo la llamada al Servicio B y como se relacionan ambas operaciones. Esto es util para identificar cuellos de botella. Los servicios envian los traces a Jaeger mediante el protocolo OTLP en el puerto 4318, y la interfaz web de Jaeger se encuentra en el puerto 16686.

## Como levantar el stack de observabilidad

Es necesario tener Docker instalado. Todos los servicios de monitoreo se levantan con un solo comando desde la raiz del proyecto: `docker-compose up -d`. Esto inicia Prometheus, Grafana y Jaeger simultaneamente. Los dos servicios de la aplicacion (puertos 8000 y 8001) se levantan aparte con uvicorn.

## Donde se evidencia

La observabilidad esta aplicada sobre todos los endpoints de ambos servicios de forma automatica. Se puede verificar en `/metrics` de cada servicio, en el dashboard de Grafana y en los traces de Jaeger.
