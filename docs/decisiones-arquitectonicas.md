# Decisiones Arquitectonicas (ADR)

Un ADR (Architecture Decision Record) es un registro corto de una decision importante: el
contexto que la motivo, que se decidio, por que y que consecuencias trae. A continuacion se
documentan las decisiones de seguridad y de escalabilidad del proyecto.

---

## Decisiones de Seguridad

### ADR-1: Autenticacion con JWT

- **Contexto:** Los endpoints estan expuestos por HTTP y cualquiera que conozca la URL podria llamarlos.
- **Decision:** Usar tokens JWT firmados (`api/auth.py`) en lugar de sesiones guardadas en el servidor.
- **Por que:** El token viaja con cada peticion y se valida sin guardar estado, lo que encaja con servicios independientes.
- **Consecuencias:** Los servicios no necesitan compartir memoria de sesiones; a cambio, hay que proteger la clave de firma y manejar la expiracion del token.

### ADR-2: Control de acceso por roles

- **Contexto:** No todos los usuarios deben poder usar todas las funciones.
- **Decision:** Definir dos roles (`student` y `admin`); `/promedio-objetivo` solo lo usa `admin` mediante la dependencia `require_role`.
- **Por que:** Separa lo que puede hacer cada tipo de usuario con poco codigo.
- **Consecuencias:** Un `student` que intente entrar a un endpoint de admin recibe un error 403; agregar mas roles es sencillo.

### ADR-3: Seguridad automatizada en el CI (DevSecOps)

- **Contexto:** Los problemas de seguridad son mas costosos si se detectan tarde.
- **Decision:** Incluir en el pipeline Gitleaks (credenciales expuestas), SonarCloud (calidad), Trivy (imagen Docker) y OWASP Dependency-Check (dependencias).
- **Por que:** Revisa cada cambio de forma automatica antes de integrarlo.
- **Consecuencias:** Se detectan riesgos en cada push; a cambio, el pipeline tarda mas en ejecutarse.

---

## Decisiones de Escalabilidad

### ADR-4: Separacion en servicios (SOA)

- **Contexto:** Una sola aplicacion monolitica es mas dificil de escalar y mantener por partes.
- **Decision:** Dividir el sistema en Servicio Principal y Servicio B, comunicados por HTTP.
- **Por que:** Cada servicio se puede desplegar, actualizar y escalar de forma independiente.
- **Consecuencias:** Mas flexibilidad; a cambio, hay que manejar la comunicacion y los fallos entre servicios.

### ADR-5: Resiliencia en la comunicacion (Timeout, Retry, Fallback)

- **Contexto:** El Servicio B puede demorarse o fallar, sobre todo bajo carga.
- **Decision:** Aplicar Timeout (2 s), Retry (hasta 3 intentos) y Fallback (lista vacia) al llamar al Servicio B (`api/main.py`).
- **Por que:** Evita que un fallo del Servicio B bloquee o tumbe al Servicio Principal.
- **Consecuencias:** El sistema sigue respondiendo aunque el Servicio B no este disponible, con informacion reducida.

### ADR-6: Servicios sin estado (stateless)

- **Contexto:** Para escalar horizontalmente se necesita poder correr varias copias de un servicio.
- **Decision:** Mantener los servicios sin estado; la autenticacion viaja en el token JWT, no en sesiones de servidor.
- **Por que:** Permite levantar varias replicas detras de un balanceador sin compartir memoria.
- **Consecuencias:** Habilita el escalado horizontal a futuro sin cambios mayores.

### ADR-7: Contenedorizacion con Docker y despliegue continuo

- **Contexto:** El despliegue manual es propenso a errores y dificil de repetir.
- **Decision:** Empaquetar cada servicio en una imagen Docker (`Dockerfile`, `Dockerfile.service_b`) y publicarlas via CD (`cd.yml`).
- **Por que:** Garantiza un despliegue reproducible y prepara el sistema para orquestadores.
- **Consecuencias:** Mismo entorno en cualquier maquina; base lista para escalar con herramientas de orquestacion.

### ADR-8: Observabilidad antes de escalar

- **Contexto:** No se puede escalar bien lo que no se mide.
- **Decision:** Integrar Prometheus (metricas), Grafana (visualizacion) y Jaeger (trazas).
- **Por que:** Permite ver la carga real y detectar cuellos de botella antes de agregar recursos.
- **Consecuencias:** Decisiones de escalado basadas en datos; a cambio, se suma el stack de monitoreo a la operacion.
