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


# 🏗️ Proyecto AWS - Despliegue App Monolítica

---

## 1. AMI App Monolítica

### 1.1 Creación de la instancia base

- Crear una **instancia EC2 t2.micro** con:
  - **8 GB de almacenamiento**
  - **VPC por defecto** o una personalizada para el proyecto
  - **Grupo de seguridad** por defecto o uno propio para el proyecto

### 1.2 Clonación y configuración del entorno

```bash
# Conectarse a la instancia
ssh -i "clave.pem" ec2-user@<IP_PUBLICA>

# Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>

# Actualizar paquetes
sudo apt update && sudo apt upgrade -y

# Instalar Python
sudo apt install python3 python3-venv python3-pip -y

# Entrar en la carpeta del proyecto
cd nombre-del-repositorio

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Correr el proyecto (ejemplo con Flask)
python app.py
```

---

## 2. Auto Scaling Group

### 2.1 Crear una plantilla de lanzamiento

1. Ir a **EC2 > Auto Scaling > Configuraciones de lanzamiento**
2. Clic en **Crear configuración**
3. Seguir el tutorial oficial:  
   🔗 [Guía oficial AWS Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-your-first-auto-scaling-group.html)

### 2.2 Crear el Auto Scaling Group

- Seleccionar la **plantilla de lanzamiento**
- Elegir la **VPC deseada**
- Usar **al menos 2 zonas de disponibilidad (AZs)**
- Mantener el resto de opciones por defecto
- Crear el grupo

- Cabe recalcar que se tiene que poner un USERDATA que setee las instancias que van a funcionar

```bash
  #!/bin/bash

sudo rm /usr/lib/python3.*/EXTERNALLY-MANAGED
# Actualizar el sistema
sudo apt-get update -y
sudo apt-get upgrade -y

# Instalar Python 3, pip, venv y Git si no estÃ¡n instalados
sudo apt-get install -y python3 python3-pip python3-venv git

# Clonar el repositorio si no existe
if [ ! -d "BookStore-Kubernetes-Deploy" ]; then
  git clone https://github.com/julimejia/BookStore-Kubernetes-Deploy.git
fi

# Cambiar permisos del repositorio
sudo chown -R $USER:$USER BookStore-Kubernetes-Deploy

sudo apt-get install nfs-common -y

sudo mkdir efs

sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-0bbf30e00ec2f106a.efs.us-east-1.amazonaws.com:/ efs

cd BookStore-Kubernetes-Deploy

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

sudo chown -R ubuntu:ubuntu venv

pip install -r requirements.txt

python app.py
```

### 2.3 Lanzamiento

- Ir a **EC2 > Auto Scaling Groups**
- Seleccionar el grupo y lanzar una nueva instancia con la plantilla creada

---

## 3. Load Balancer

### 3.1 Crear el Load Balancer

1. Ir a **EC2 > Load Balancers**
2. Crear un grupo de destino con las instancias que se balancearán
3. Crear un nuevo Load Balancer:
   - Tipo: **HTTP/HTTPS**
   - AZs: las mismas del Auto Scaling Group
   - Otras configuraciones: por defecto

### 3.2 Vincular al Auto Scaling Group

1. Ir al **Auto Scaling Group**
2. Editar configuraciones
3. En **Balanceador de carga > Grupo de destino**
   - Seleccionar el grupo de destino creado previamente

---

## 4. Base de Datos (con Master-Slave)

### 4.1 Instancia Master

1. Crear una **instancia EC2** para la base de datos
2. Instalar Docker:

```bash
sudo apt update && sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

3. Crear una imagen de Docker para la base de datos o usar una existente:

```bash
docker run --name mysql-master -e MYSQL_ROOT_PASSWORD=admin -d mysql:latest
```

### 4.2 Instancia Slave

1. Repetir los pasos 1 a 3 en una nueva instancia
2. Configurar replicación:
   - Crear usuario **replica** en el master
   - Obtener información binlog del master (`SHOW MASTER STATUS`)
   - En el slave, configurar `CHANGE MASTER TO` y ejecutar `START SLAVE`

---

## 5. EFS (NFS)

### 5.1 Crear EFS

1. Ir a **EFS > Crear sistema de archivos**
2. Configurar:
   - Usar una **VPC existente**
   - Crear un nuevo **grupo de seguridad** con permisos adecuados para NFS (puerto TCP 2049)
   - Asociarlo con los grupos de seguridad ya usados por las instancias EC2

### 5.2 Conectar EFS a una instancia EC2

```bash
# Crear directorio para montar
sudo mkdir /mnt/efs

# Instalar NFS (si no está instalado)
sudo apt install nfs-common -y

# Montar el EFS (reemplazar fs-12345678 con tu ID)
sudo mount -t nfs4 -o nfsvers=4.1 fs-12345678.efs.us-east-1.amazonaws.com:/ /mnt/efs
```

> 📌 **Tip:** Para montarlo automáticamente al iniciar, agrega al `/etc/fstab`:
```bash
fs-12345678.efs.us-east-1.amazonaws.com:/ /mnt/efs nfs4 defaults,_netdev 0 0
```

  
  



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




