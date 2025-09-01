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

- Supabase (PostgreSQL) 

- django-cors-headers (para conexión con frontend).

---

Configuración 

El backend se desplegó en Render con base de datos alojada en Supabase.


📂 Archivos adicionales para Render

Durante la configuración se añadieron/editaron estos archivos del Backend:

render.yaml → define el servicio, comandos de build y variables.

build.sh → script para instalar dependencias y ejecutar migraciones automáticamente antes del deploy.

requirements.txt → actualizado para asegurar que todas las dependencias de Django estén instaladas en Render.

Procfile → (opcional en Render) usado para definir cómo iniciar la app con Gunicorn.


🗄️ Base de datos con Supabase

En este proyecto la base de datos se aloja en Supabase, que provee una URL, esa URL se copia en la variable DATABASE_URL en Render para que Django pueda conectarse.


⚙️ Configuración en Render

1. Sube tu proyecto a GitHub.

2. En Render crea un nuevo Web Service.

3. Conecta el repositorio a Render

4. Configura:

Build Command: ./build.sh

Start Command: gunicorn tienda_backend.wsgi:application

5. En Environment variables de Render agrega tres variables de entorno:

DATABASE_URL → tu URL de Supabase

SECRET_KEY → un valor fuerte

DEBUG → False

5. Haz deploy, se ejecutarán automaticamente las migraciones y se creará tu admin.

Cada vez que hagas push a la rama principal en GitHub, Render reconstruirá y desplegará el backend automáticamente.

6. Si el deploy se realizó con éxito podras accder a la direccion que te asigna Render y te podrás conectar con el Frontend en Vercel.

---

👨‍💻 Autor
Jorge Patricio Santamaría Cherrez

Máster en Ingeniería de Software y Sistemas Informáticos 
