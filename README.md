🛒 Tienda Backend

Aplicación desarrollada con Django + Django REST Framework que provee el backend de la tienda en línea.

El frontend se encuentra disponible aquí:

👉 https://github.com/Patogol35/Tienda-Frontend-React

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

📦 Instalación y configuración

1. Clona el repositorio

git clone https://github.com/Patogol35/Tienda-Backend-Django


2. Ingresa a la carpeta del proyecto
   
cd Tienda-Backend-Django

3. Crea el entorno virtual

python -m venv venv

Linux/Mac: source venv/bin/activate

Windows: venv\Scripts\activate


4. Instala las dependencias

pip install -r requirements.txt

⚠️ Si mysqlclient da problemas, instálalo manualmente según tu sistema:

pip install mysqlclient

o

pip install PyMySQL


5. Crea la base de datos en MySQL

CREATE DATABASE tienda_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

En settings.py verifica:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tienda_db',
        'USER': 'root',
        'PASSWORD': 'tu_clave',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


6. Aplica las migraciones

python manage.py makemigrations

python manage.py migrate


7. Crea el superusuario

python manage.py createsuperuser


8. Ejecuta el servidor

python manage.py runserver


---

🔗 Endpoints principales

Autenticación (JWT)

POST /api/register/ → Registrar usuario

POST /api/token/ → Obtener token de acceso

POST /api/token/refresh/ → Refrescar token


Ejemplo:

POST /api/register/
{
  "username": "juan",
  "email": "juan@mail.com",
  "password": "123456"
}


---

Productos

GET /api/productos/ → Listar productos

POST /api/productos/ → Crear producto (admin)

PUT /api/productos/{id}/ → Editar producto

DELETE /api/productos/{id}/ → Eliminar producto


Ejemplo respuesta:

[
  {
    "id": 1,
    "nombre": "Camiseta",
    "descripcion": "Camiseta de algodón",
    "precio": "19.99",
    "stock": 10
  }
]


---

Carrito

GET /api/carrito/ → Ver carrito del usuario

POST /api/carrito/agregar/ → Agregar producto al carrito


Ejemplo:

POST /api/carrito/agregar/
{
  "producto_id": 1,
  "cantidad": 2
}


---

Pedidos

POST /api/pedido/crear/ → Crear pedido desde carrito

GET /api/pedidos/ → Listar pedidos del usuario


Ejemplo respuesta:

{
  "id": 3,
  "usuario": 1,
  "fecha": "2025-08-26T10:00:00Z",
  "total": "39.98",
  "items": [
    {
      "producto": { "id": 1, "nombre": "Camiseta" },
      "cantidad": 2,
      "precio_unitario": "19.99",
      "subtotal": "39.98"
    }
  ]
}


---

📸 Panel de administración

Accede a:
👉 http://127.0.0.1:8000/admin/

Podrás gestionar productos, carritos, pedidos y usuarios.


---

Próximos pasos / Mejoras

[ ] Documentación de la API con Swagger o ReDoc

[ ] Tests automatizados


[ ] Manejo de pagos y envíos



---

👨‍💻 Autor

Jorge Patricio Santamaría Cherrez

Máster en Ingeniería de Software y Sistemas Informáticos

