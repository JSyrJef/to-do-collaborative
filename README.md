# 📝 TaskTogether - To-Do Colaborativo

Aplicación de gestión de tareas colaborativas construida con Angular 18 (TailwindCSS) para el frontend y Django (REST Framework) para el backend.


## Arquitectura

**TaskTogether** es una aplicación de gestión de tareas colaborativa con una arquitectura cliente-servidor que consta de dos componentes principales:

### 1. Frontend (Angular)

El frontend está desarrollado con **Angular 18** y utiliza:

- **Angular Material** para componentes de UI

- **Servicios HTTP** para comunicarse con el backend

- **Tailwind CSS** para estilos

### 2. Backend (Django)

El backend está construido con **Django** y **Django REST Framework**:

- **Django 5.2.1** como framework principal

- **Django REST Framework** para la API RESTful

- **JWT** para autenticación

- **SQLite/PostgreSQL** como motores de base de datos


# Pasos para Probar la Aplicación

## 1. Requisitos Previos

Asegúrate de tener instalado:

- Node.js (v18.19.1 o superior)  
- npm (v8.0.0 o superior)  
- Python (v3.8 o superior)  
- pip (última versión)  
- Git

## 2. Clonar el Repositorio

```bash
git clone https://github.com/JSyrJef/to-do-collaborative.git  
cd to-do-collaborative
```

## 3. Configurar el Backend

### Crear un entorno virtual:

```bash
cd backend  
python -m venv venv  
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### Instalar dependencias:

```bash
pip install -r requirements.txt
```

### Crear un archivo `.env` en el directorio `backend`:

```env
SECRET_KEY=your-secret-key-for-dev  
DEBUG=True  
ALLOWED_HOSTS=localhost,127.0.0.1  
CORS_ALLOWED_ORIGINS=http://localhost:4200
```

### Configurar la base de datos:

```bash
python manage.py migrate
```

### Crear un superusuario (opcional):

```bash
python manage.py createsuperuser
```

### Iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

El backend estará disponible en `http://localhost:8000`.

## 4. Configurar el Frontend

### Instalar dependencias:

```bash
cd ../frontend  
npm install
```

### Iniciar el servidor de desarrollo:

```bash
npm start
# o
ng serve
```

El frontend estará disponible en `http://localhost:4200`.

## 5. Probar la Aplicación

- **Registrarse:** Crea una cuenta desde la página de registro.  
- **Iniciar sesión:** Accede con tus credenciales.  
- **Crear tareas:** Añade tareas con título, descripción y estado.  
- **Gestionar colaboradores:** En modo edición de una tarea, añade colaboradores por nombre de usuario
- **Cambiar estados:** Marca tareas como completadas o reabrirlas
- **Filtrar tareas:** Filtra por estado (pendientes, completadas, etc.)

## 6. Flujo de Autenticación

La app usa **JWT**:

- Al iniciar sesión, recibes tokens de acceso y actualización.
- El token de acceso dura **24 horas**
- El token de actualización dura **7 días**

## 7. Permisos y Autorización

Roles y permisos:

- **Propietario de tarea:** acceso completo (ver, editar, eliminar)
- **Colaborador:** puede ver y editar, pero no eliminar

## Modelo de Datos

Modelo principal: **Task**

- Título y descripción  
- Estado (pendiente, en progreso, completado, etc.)  
- Propietario (usuario creador)  
- Colaboradores (usuarios que pueden ver/editar)

## API REST

La app expone endpoints para:

- Gestión de tareas (CRUD)  
- Gestión de colaboradores  
- Autenticación de usuarios  

## Notas

- Despliegue: **Netlify** (frontend) y **Render** (backend)  
- Límite de solicitudes:  
  - 100/día para usuarios anónimos  
  - 1000/día para usuarios autenticados  
