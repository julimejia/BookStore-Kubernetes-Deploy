para iniciar la base de datos y crear las tablas:

flask shell
>>> from extensions import db
>>> db.create_all()




1. Objetivo 1: 20% Desplegar la aplicación BookStore Monolítica en una Máquina Virtual en AWS, con
un dominio propio, certificado SSL y Proxy inverso en NGINX. 20%

## Creación y configuración de la instancia AWS EC2

### 1. Crear una instancia EC2

1. Inicia sesión en la consola de AWS
2. Selecciona Ubuntu Server 22.04 LTS como sistema operativo
3. Elige un tipo de instancia t2.micro (suficiente para este proyecto)
4. Configura las opciones de red y almacenamiento (8GB es suficiente)
5. Configura el grupo de seguridad con los siguientes puertos:
   - SSH (22)
   - HTTP (80)
   - HTTPS (443)
8. Lanza la instancia y guarda el par de claves

### 2. Conectarse a la instancia EC2

```bash
ssh -i "mi-clave.pem" ubuntu@[dirección-ip-pública]
```

## Instalación de Docker y Docker Compose

Docker y Docker Compose son necesarios para ejecutar la aplicación BookStore, que está contenerizada para facilitar su despliegue.

```bash
# Actualizar paquetes
sudo apt update
sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Actualizar paquetes e instalar Docker
sudo apt update
sudo apt install -y docker-ce

# Añadir usuario al grupo docker (evita usar sudo cada vez)
sudo usermod -aG docker ubuntu
newgrp docker

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose

# Verificar instalaciones
docker --version
docker-compose --version
```

## Despliegue de la aplicación BookStore

### 1. Clonar el repositorio de la aplicación

```bash
# Crear directorio para la aplicación
mkdir -p ~/bookstore
cd ~/bookstore

# Transferir archivos de la aplicación a la instancia EC2
# (Puedes usar Git para esta tarea)
```

### 2. Levantar la aplicación con Docker Compose

```bash
# Construir y levantar los contenedores
docker-compose up -d

# Verificar que los contenedores estén corriendo
docker-compose ps
```

Los contenedores `bookstore_db_1` y `bookstore_flaskapp_1` deberían mostrarse como "Up".

## Configuración del dominio

Para este proyecto, utilizamos el dominio `proyecto2.online` adquirido a través de GoDaddy.

### 1. Configurar registros DNS

Accede al panel de control de DNS de tu proveedor de dominio y configura los siguientes registros:

- **Registro A para el dominio raíz**:
  - Tipo: A
  - Nombre: @ (o deja en blanco, según el proveedor)
  - Valor: [Dirección IP pública de la instancia EC2]
  - TTL: 600 segundos (o el valor predeterminado)

- **Registro A para el subdominio www**:
  - Tipo: A
  - Nombre: www
  - Valor: [Dirección IP pública de la instancia EC2]
  - TTL: 600 segundos (o el valor predeterminado)

### 2. Verificar la propagación DNS

La propagación DNS puede tardar entre 15 minutos y 48 horas. Para verificar si la configuración se ha propagado, utiliza:

```bash
dig proyecto2.online
dig www.proyecto2.online
```

## Instalación y configuración de NGINX

NGINX actúa como proxy inverso, dirigiendo el tráfico desde el dominio a la aplicación Flask que se ejecuta en Docker.

### 1. Instalar NGINX

```bash
sudo apt update
sudo apt install nginx -y
```

### 2. Configurar NGINX como proxy inverso

```bash
sudo nano /etc/nginx/sites-available/bookstore
```

Añade la siguiente configuración básica:

```nginx
server {
    listen 80;
    server_name proyecto2.online www.proyecto2.online;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Activar la configuración y reiniciar NGINX

```bash
sudo ln -s /etc/nginx/sites-available/bookstore /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Configuración de SSL con Let's Encrypt

Let's Encrypt proporciona certificados SSL gratuitos, lo que permite servir la aplicación de forma segura mediante HTTPS.

### 1. Instalar Certbot

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
```

### 2. Obtener un certificado SSL (método de validación HTTP)

En nuestro caso, tuvimos problemas con la validación HTTP, así que utilizamos el método de validación DNS:

```bash
sudo certbot certonly --manual --preferred-challenges dns -d proyecto2.online -d www.proyecto2.online
```

Este método requirió la creación de registros TXT en la configuración DNS para verificar la propiedad del dominio.

### 3. Configurar NGINX para usar SSL

Una vez obtenido el certificado, actualizamos la configuración de NGINX:

```bash
sudo nano /etc/nginx/sites-available/bookstore
```

Reemplazo de la configuración con:

```nginx
server {
    listen 80;
    server_name proyecto2.online www.proyecto2.online;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name proyecto2.online www.proyecto2.online;

    ssl_certificate /etc/letsencrypt/live/proyecto2.online/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/proyecto2.online/privkey.pem;

    # Configuración SSL optimizada
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;

    # Headers de seguridad
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. Verificar y reiniciar NGINX

```bash
sudo nginx -t
sudo systemctl restart nginx
```

## Configuración del inicio automático de servicios

Para asegurar que la aplicación esté disponible después de reinicios, configuramos los servicios para iniciar automáticamente.

### 1. Configurar NGINX para iniciar automáticamente

```bash
sudo systemctl enable nginx
```

### 2. Crear un servicio systemd para Docker Compose

```bash
sudo nano /etc/systemd/system/bookstore.service
```

Contenido del archivo:

```
[Unit]
Description=BookStore Application
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/bookstore
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down

[Install]
WantedBy=multi-user.target
```

### 3. Activar el servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable bookstore.service
sudo systemctl start bookstore.service
```

## Gestión de cambios de IP con IP Elástica

Para evitar problemas con cambios de IP cuando se reinicia la instancia EC2, implementamos una IP Elástica.

### 2. Actualizar registros DNS si es necesario

Si la IP Elástica es diferente de la IP original, actualiza los registros DNS para que apunten a la nueva IP.

Y listo, la aplicación BookStore Monolithic ya debe poder ser accesible mediante HTTPS con la url www.proyecto2.online

##

2. Objetivo 2: 30% Realizar el escalamiento en nube de la aplicación monolítica, siguiente algún patrón
de arquitectura de escalamiento de apps monolíticas en AWS. La aplicación debe ser escalada
utilizando Máquinas Virtuales (VM) con autoescalamiento, base de datos aparte Administrada o si
es implementada con VM con Alta Disponibilidad, y Archivos compartidos vía NFS (como un servicio
o una VM con NFS con Alta Disponibilidad).

1 AMI app monolitica

   1 Creacion
     - Cree una instancia EC2 t2 micro 8 de almacenamiento, con al vpc por default o la que vaya a contener todo el proyecto,  y con el grupo de reglas default o el que vaya a usar todo el proyecto
     
   2 Clonacion y funcionamiento
     - clone el repositorio de github dentro de la consola de la instancia
     - Actualice la instancia, upgradee la instancia
     - instale python en la instancia
     - entre en la carpeta del repositorio
     - cree un entorno virtual de python
     - Ingrese al mismo
     - Instale dependencias
     - corra el proyecto
     
2 Auto Scaling group
  
  1 Creacion de la plantilla del auto scaling group
   - Vaya a EC2
   - Click en Auto scaling en el side bar de la izquierda
   - Grupos de AutoScaling
   - y click en crear una configuracion
   - Luego siga los pasos del siguiente tutorial para la plantilla : https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-your-first-auto-scaling-group.html
  
     
  2 Crear el auto scaling
    - Seleccionar la plantilla 
    - Escoja la vpc que desee, si no tiene la default
    - Use almenos 2 zonas de disponibilidad 
    - Todo lo demas dejelo por default
    - Cree el grupo
  3 Lanzamiento
    - Dentro de la consola EC2 vaya a auto scaling group
    - vaya a la parte de lanzar uno nuevo.
    - seleccione la plantilla ya creada
  
2 Load balancer 
   1 Creacion del load balancer 
    - Dentro de la consola EC2 vaya a load balancer
    - Cree un grupo (Las instancias que va a balancear)
    - Vaya al apartado de creacion
    - Seleccione HTTP/HTTPS
    - Seleccione las mismas zonas de disponibilidad del autoscaling group
    - todo lo demas en default
    - cree la instancia
    
  2 Añadir la instancia al AutoScaling group
    - Vaya al autoScaling group que ya creo 
    - Vaya al apartado de editar
    - vaya al apartado balanceador de carga
    - Seleccione grupos destino
    - Seleccione el grupo que ha creado
3 Base de datos
  1 Cree un EC2 para almacenar la base de datos
  



3. Objetivo 3: 50% Realizar una reingeniería de la app BookStore Monolitica, para que sea dividida en
3 microservicios coordinador:
o Microservicio 1: Autenticación: gestionará register, login, logout.
o Microservicio 2: Catalogo: permitirá visualizar la oferta de libros en la plataforma.
o Microservicio 3: Compra, Pago y Entrega de libros que se venden por la plataforma.
   
   Para la creacion de los microservicios se decidio usar FastApi en lugar de Flask, continuamos con REST para la comunicacion, y se utiliza una persistencia de datos en Postgresql.
   Cada microservicio maneja una arquitectura por capas, endpoint - logica - entidad. Para el microservicios de books se utiliza un repositorio para las actividades de CRUD ya que en este microservicio son las
   mas recurrentes. El microservicio de Sales (Encargado de las ventas) se comunica con el microservicio de Books para la consulta de material y la actualizacion del mismo. 
   Para el Apigateway se tuvo en cuenta la observacion del proyecto pasado, siendo este mas "generico" para la facil actualizacion (Solo se debe agregar la ruta a la cual se quiere redireccionar). 
   Cada microservicio maneja su propia persistencia de datos. 
   Para el manejo de la sesion se utiliza un JWT que carga con el correo y el id del usuario. Este es necesario para crear libros entre otras actividades. (Hay endpoints que en el front no se utilizan pero se
   desarrollaron con el fin de hacer debug).
   En el frontend (Cliente) se utiliza HTML + js.   

   ![image](https://github.com/user-attachments/assets/980e5547-69df-450a-9479-5972f685a7d6)




