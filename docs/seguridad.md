# Seguridad Basica

## Por que es necesaria

En una arquitectura de servicios, los endpoints estan expuestos a cualquier cliente que conozca la URL. Sin un mecanismo de seguridad, cualquier persona podria acceder a los recursos del sistema sin restricciones. La seguridad basica garantiza que solo usuarios autenticados y autorizados puedan consumir los servicios.

## Mecanismo implementado: JWT

El sistema utiliza JSON Web Tokens (JWT) para la autenticacion y el control de acceso. JWT es un estandar que permite generar tokens firmados digitalmente que contienen informacion del usuario (nombre y rol) y tienen un tiempo de expiracion.

## Flujo de autenticacion

1. El usuario envia sus credenciales (usuario y contrasena) al endpoint `/login`.
2. Si las credenciales son validas, el sistema genera un token JWT con el nombre de usuario, su rol y una expiracion de 30 minutos.
3. El usuario incluye ese token en el encabezado de autorizacion de sus siguientes solicitudes.
4. El sistema valida el token en cada solicitud: verifica que no haya expirado y que la firma sea correcta.

## Control de acceso por roles

El sistema maneja dos roles: `student` y `admin`. El endpoint `/promedio` permite el acceso a cualquier usuario autenticado, sin importar su rol. El endpoint `/promedio-objetivo` solo permite el acceso a usuarios con rol `admin`. Si un usuario con rol `student` intenta acceder a este endpoint, recibe un error 403 (acceso denegado).

## Donde se aplica

La seguridad esta aplicada en los dos endpoints principales del Servicio Principal: `/promedio` (requiere autenticacion) y `/promedio-objetivo` (requiere autenticacion y rol admin). El endpoint `/login` es publico, ya que es el punto de entrada para obtener el token.
