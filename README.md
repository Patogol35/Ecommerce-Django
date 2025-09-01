🛒 Tienda Backend

Aplicación desarrollada con Django + Django REST Framework que provee el backend de la tienda en línea.

---

✨ Características principales

Autenticación con JWT

- Registro de usuarios.

- Inicio de sesión y generación de tokens de acceso/refresh con SimpleJWT.


Gestión de productos

- CRUD completo para administración de productos.

- Endpoints públicos para consultar catálogo.


Carrito de compras

- API para agregar, listar y eliminar productos del carrito.

- Carrito persistente asociado al usuario.

- Control de Stock de productos.


Gestión de pedidos

- Creación de pedidos a partir del carrito.

- Consultar historial de pedidos por usuario.


Integración con frontend en React + Vite

- Soporte CORS para conexión directa con la aplicación cliente.


---

⚙️ Tecnologías utilizadas 

- Django 4+

- Django REST Framework (DRF)

- Django REST Framework SimpleJWT (autenticación con tokens JWT).

- MySQL (configurable también con SQLite en desarrollo).

- django-cors-headers (para conexión con frontend).

---

Configuración 

📂 Archivos adicionales para Render

Durante la configuración se añadieron/editaron estos archivos del Backend:

render.yaml → define el servicio, comandos de build y variables.

build.sh → script para instalar dependencias y ejecutar migraciones automáticamente antes del deploy.

requirements.txt → actualizado para asegurar que todas las dependencias de Django estén instaladas en Render.

Procfile → (opcional en Render) usado para definir cómo iniciar la app con Gunicorn.


🗄️ Base de datos con Supabase

En este proyecto la base de datos se aloja en Supabase, que provee una URL de conexión al estilo:

postgresql://usuario:contraseña@host:puerto/base_de_datos

Esa URL se copia en la variable DATABASE_URL en Render para que Django pueda conectarse.
q

⚙️ Configuración en Render

1. Web Service en Render
   
Crea tu Web Service en Render (https://render.com):

En Build Command ejecuta este comando:

./build.sh

En Start Command ejecuta este comando:

gunicorn tienda_backend.wsgi:application


2. Variables de Entorno

En el panel de Environment de Render agrega tres variables de entorno:

Name	Value

- DATABASE_URL	postgresql://postgres:TU_PASSWORD@db_xxxxxx.supabase.co:5432/postgres (desde Supabase)

- SECRET_KEY	django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (elige algo fuerte)

- DEBUG	False


🚀 Deploy automático

Cada vez que hagas push a la rama principal en GitHub, Render reconstruirá y desplegará el backend automáticamente.


---

👨‍💻 Autor
Jorge Patricio Santamaría Cherrez

Máster en Ingeniería de Software y Sistemas Informáticos 
