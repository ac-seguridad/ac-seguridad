# Instalación de dependencias y archivos necesarios para correr el proyecto.

## Instalar Miniconda para Linux.
Con la instalación de Miniconda será posible crear ambientes virtuales y descargar
dependencias necesarias para el proyecto, tales como `Python 3.6`, `Django`, entre
otras. Debemos ejecutar en un terminal: 
* `curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh`
* `bash Miniconda3-latest-Linux-x86_64.sh`
* [Solo para limpieza] `rm Miniconda3-latest-Linux-x86_64.sh`

## Creación de un ambiente virtual.
Nos permite tener todos las dependencias necesarias para nuestro proyecto.
Ejecutar en un terminal:
* `conda create -n acseguridad --file requerimientos.txt`

## Activar nuestro ambiente virtual.
Ejecutar:
* `source activate acseguridad`
* [Desactivar] `source deactivate acseguridad`

## [Si el proyecto no está creado] Crear el proyecto.
Ejecutar: 
* `django-admin startproject project`
* `python manage.py startapp ac_seguridad`

## Creación de la base de datos.
Ejecutar:
[Si psql no funciona]: * sudo -u postgres psql
* `psql`
* `CREATE USER usuario WITH PASSWORD 'contraseña';`
* `CREATE DATABASE "ac_seguridad";`
* `GRANT ALL PRIVILEGES ON DATABASE ac_seguridad to usuario;`;
* `\password postgres;`
* Insertar contraseña aquí, dos veces.
* `python manage.py migrate`

## Ejecutar el servidor de desarrollo.
Ejecutar:
* `python manage.py runserver 0.0.0.0:8080`