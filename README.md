🛒 Tienda Backend

Aplicación desarrollada con Django + Django REST Framework que provee el backend de la tienda en línea.

El frontend se encuentra disponible aquí:

👉 https://github.com/Patogol35/Ecommerce-React

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


Quedaría mucho más claro y ordenado así 👇


---

Deploy en Render con Django + Supabase

Para poner tu backend en producción con Render necesitas algunos archivos clave en la raíz del proyecto y la configuración correcta de variables de entorno.

1. Archivos necesarios en la raíz

render.yaml → define el servicio, comandos de build y variables.

build.sh → script que instala dependencias y ejecuta migraciones automáticamente antes de cada deploy.

requirements.txt → actualizado con todas las dependencias de Django y librerías necesarias.

Procfile (opcional en Render) → especifica cómo iniciar la app con Gunicorn.

2. Base de datos en Supabase

Este proyecto utiliza Supabase como base de datos.
Render necesita la URL de conexión, que debes copiar en la variable de entorno DATABASE_URL.

Formato de ejemplo:

postgresql://postgres.sxnrtomwzoawegjkdzpl:[TU-PASSWORD]@aws-1-us-east-2.pooler.supabase.com:5432/postgres

Reemplaza [TU-PASSWORD] con tu contraseña real de Supabase.


3. Configuración en Render

- Sube tu proyecto a GitHub.

- En Render, crea un nuevo Web Service.

- Conecta tu repositorio de GitHub.

- Configura los comandos:

Build Command:

./build.sh

Start Command:

gunicorn tienda_backend.wsgi:application

- Agrega las variables de entorno en Render:

DATABASE_URL → la URL de tu Supabase

SECRET_KEY → un valor único y seguro

DEBUG → False

4. Deploy automático

Cada vez que hagas push a la rama principal en GitHub, Render:

Instalará dependencias

Ejecutará migraciones

Reconstruirá y desplegará tu backend automáticamente

6. Verificación

Si todo fue correcto, Render te dará una URL pública donde tu backend estará disponible.
Luego podrás conectar tu frontend en Vercel a esta dirección sin problema.

---

👨‍💻 Autor
Jorge Patricio Santamaría Cherrez

Máster en Ingeniería de Software y Sistemas Informáticos 
