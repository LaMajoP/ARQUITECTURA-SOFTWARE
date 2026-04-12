# Arquitectura del Sistema

## Descripcion del sistema

El sistema es una calculadora de promedios ponderados para programas de ingenieria de una universidad. Permite a los estudiantes calcular su promedio academico, aplicar filtros sobre las materias y determinar que nota necesitan para alcanzar un promedio objetivo.

## Arquitectura inicial

En el primer corte, el sistema funcionaba como una aplicacion de consola (CLI) con una estructura basada en capas:

- **domain/**: entidades del negocio como Materia, MallaCurricular y CalculadoraPromedio.
- **infrastructure/**: carga de datos desde archivos JSON mediante el patron Factory Method.
- **strategy/**: filtros intercambiables aplicados antes del calculo, usando el patron Strategy.

Todo se ejecutaba desde un unico punto de entrada (`main.py`) sin comunicacion con servicios externos.

## Arquitectura evolucionada (SOA)

En el segundo corte, el sistema evoluciono hacia una Arquitectura Orientada a Servicios (SOA) con dos servicios REST independientes:

- **Servicio Principal** (puerto 8000): expone los endpoints `/promedio` y `/promedio-objetivo`. Recibe las solicitudes del cliente, ejecuta la logica de negocio y consume al Servicio B para obtener informacion adicional.
- **Servicio B** (puerto 8001): actua como servicio proveedor. Expone el endpoint `/materias-extra` y retorna sugerencias de materias complementarias.

Ambos servicios se comunican mediante HTTP REST. El Servicio Principal actua como consumidor y el Servicio B como proveedor, cumpliendo el modelo clasico de una arquitectura orientada a servicios.

Ademas, se incorporaron mecanismos de resiliencia en la comunicacion entre servicios, seguridad basada en JWT para proteger los endpoints, y herramientas de observabilidad (Prometheus, Grafana y Jaeger) para monitorear el comportamiento del sistema en tiempo de ejecucion.
