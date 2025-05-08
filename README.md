para iniciar la base de datos y crear las tablas:

flask shell
>>> from extensions import db
>>> db.create_all()




1. Objetivo 1: 20% Desplegar la aplicación BookStore Monolítica en una Máquina Virtual en AWS, con
un dominio propio, certificado SSL y Proxy inverso en NGINX. 20%




2. Objetivo 2: 30% Realizar el escalamiento en nube de la aplicación monolítica, siguiente algún patrón
de arquitectura de escalamiento de apps monolíticas en AWS. La aplicación debe ser escalada
utilizando Máquinas Virtuales (VM) con autoescalamiento, base de datos aparte Administrada o si
es implementada con VM con Alta Disponibilidad, y Archivos compartidos vía NFS (como un servicio
o una VM con NFS con Alta Disponibilidad).

1 Auto Scaling group
  
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
2 Load balancer 

  



3. Objetivo 3: 50% Realizar una reingeniería de la app BookStore Monolitica, para que sea dividida en
3 microservicios coordinador:
o Microservicio 1: Autenticación: gestionará register, login, logout.
o Microservicio 2: Catalogo: permitirá visualizar la oferta de libros en la plataforma.
o Microservicio 3: Compra, Pago y Entrega de libros que se venden por la plataforma.


