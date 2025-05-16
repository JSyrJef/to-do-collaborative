# API de Tareas Colaborativas

API RESTful para gestionar tareas colaborativas entre usuarios.

## Endpoints disponibles

### Autenticación
- `POST /api/register/`: Registrar nuevo usuario
- `POST /api/login/`: Iniciar sesión (retorna token JWT)
- `POST /api/token/refresh/`: Refrescar token JWT
- `POST /api/token/verify/`: Verificar validez del token

### Tareas
- `GET /api/tasks/`: Listar tareas del usuario (propias y colaborativas, filtro opcional: ?status=<status>)
- `POST /api/tasks/`: Crear nueva tarea
- `GET /api/tasks/{id}/`: Ver detalle de tarea
- `PUT /api/tasks/{id}/`: Actualizar tarea completa
- `PATCH /api/tasks/{id}/`: Actualizar campos específicos de tarea
- `DELETE /api/tasks/{id}/`: Eliminar tarea (solo propietario)

### Colaboración
- `POST /api/tasks/{id}/add_collaborator/`: Añadir colaborador a una tarea (body: `{"username": "nombre_usuario"}`)
- `POST /api/tasks/{id}/remove_collaborator/`: Eliminar colaborador de una tarea (body: `{"username": "nombre_usuario"}`)

## Configuración del proyecto

1. Clonar repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Aplicar migraciones: `python manage.py migrate`
4. Ejecutar servidor: `python manage.py runserver`