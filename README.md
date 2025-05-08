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



3. Objetivo 3: 50% Realizar una reingeniería de la app BookStore Monolitica, para que sea dividida en
3 microservicios coordinador:
o Microservicio 1: Autenticación: gestionará register, login, logout.
o Microservicio 2: Catalogo: permitirá visualizar la oferta de libros en la plataforma.
o Microservicio 3: Compra, Pago y Entrega de libros que se venden por la plataforma.


