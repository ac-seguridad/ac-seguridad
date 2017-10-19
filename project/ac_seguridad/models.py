from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime
from django.utils import timezone

#MODELO DE LA BASE DE DATOS. 
#conjunto de tablas, junto con sus atributos y propiedades. 
#las clases son las tablas
#los atributos son las columnas


# https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models 
# Referencia de todos los tipos.
#migracion: actualizas las bases de datos, la forma o atributos, hasta nombres
#usuarios(cédula, nombre, apellido, teléfono, email, contraseña)
class Persona(models.Model):     #crea tabla
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) # Permite el login con usuario/password.
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=25)
    cedula = models.CharField(max_length=20, primary_key=True, verbose_name='cedula', unique=True) #es char porque no voy a hacer operaciones con ese valor
    telefono = models.CharField(max_length=25)
    email = models.EmailField(verbose_name='email address', max_length=255)
    enviar_correo = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.nombre + " " +  self.apellido + " cedula: "+ self.cedula
    
        
#Estacionamiento(RIF, nombre, Numero_de_puestos)        
class Estacionamiento(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) # Permite el login con usuario/password
    rif = models.CharField(max_length=20, primary_key=True, verbose_name='rif', unique=True)
    nombre = models.CharField(max_length=200)
    numero_de_puestos = models.IntegerField(default=1000)
    acceso_restringido = models.BooleanField(default=True)
    email = models.EmailField(verbose_name='email address', max_length=255)
    tarifa_plana = models.BooleanField(default=True)
    monto_tarifa = models.FloatField(default=1000)
    
    def __str__(self):
        return self.rif + " " + self.nombre
        
#vehiculo(Placa,CEDULA,)   
class Vehiculo(models.Model):
    fecha_actual = datetime.datetime.now()
    anos_vehiculos = zip(range(1950,fecha_actual.year+1),range(1950,fecha_actual.year+1))
    dueno = models.ForeignKey(Persona, on_delete=models.CASCADE) 
    placa = models.CharField(max_length=25, primary_key = True)
    marca = models.CharField(max_length=25)
    modelo = models.CharField(max_length=25)
    year = models.PositiveSmallIntegerField(choices=anos_vehiculos, default=2000) 
    
    def __str__(self):
        # return str(self.placa) + " " + str(self.marca) + " " + str(self.modelo) + " " + str(self.year) + " " + str(self.dueno.cedula)
        return str(self.placa)


#Ticket( Placa, RIF,numero,hora_entrada, hora salida, pago)
class Ticket(models.Model):
    placa = models.ForeignKey(Vehiculo, on_delete=models.CASCADE) 
    rif = models.ForeignKey(Estacionamiento, on_delete=models.CASCADE)
    numero_ticket = models.AutoField(primary_key=True)
    hora_entrada =  models.DateTimeField('Hora de entrada')
    hora_salida =  models.DateTimeField('Hora de salida', null=True)
    pagado = models.BooleanField(default=False) # Tiene que añadirse un valor por defecto cuandohay campos booleanos.
    
    def __str__(self):
        return str(self.placa) + " " + str(self.rif) + " " + str(self.numero_ticket) + " " + str(self.hora_entrada) + " " + str(self.hora_salida) + " " + str(self.pagado)

#Ticket no registrados ( Placa, RIF,numero,hora_entrada, hora salida, pago)
class TicketNoRegistrado(models.Model):
    placa =  models.CharField(max_length=25)
    rif = models.ForeignKey(Estacionamiento, on_delete=models.CASCADE)
    numero_ticket = models.AutoField(primary_key=True)
    hora_entrada =  models.DateTimeField('Hora de entrada')
    hora_salida =  models.DateTimeField('Hora de salida', null=True)
    pagado = models.BooleanField(default=False) # Tiene que añadirse un valor por defecto cuandohay campos booleanos.
    
    def __str__(self):
        return str(self.placa) + " " + str(self.rif) + " " + str(self.numero_ticket) + " " + str(self.hora_entrada) + " " + str(self.hora_salida) + " " + str(self.pagado)

# alertas(numero_alertas,usuario,vehiculo,estacionamiento, tipo, fecha)
# Tipos de alertas:
    # -no_coincidencia: Cuando un carro intente salir con un ticket que no le pertenece
    # -Entrada_manual: Opcional, cuando se ingrese la placa manualmente
    # -salida_exitosa: cuando sale un vehiculo exitosamente
    # -entrada_exitosa: cuando entra un vehiculo con reconocimiento de placa
    #- acceso_negado: carro no registrado intenta entrar a un estacionamiento que no permite el acceso.

class Alerta(models.Model):
    numero_alertas = models.AutoField(primary_key = True) # Deberiamos quitar esto o cambiarlo a IntegerField porque aunque se borre la BD igual queda el contador.
    usuario = models.CharField(max_length=50, null = True)
    vehiculo = models.CharField(max_length=25)
    estacionamiento = models.ForeignKey(Estacionamiento, on_delete=models.CASCADE, null=True) #TODO: set null=False
    tipo = models.CharField(max_length=200)
    fecha = models.DateTimeField('fecha de alerta', default=timezone.now)
    
    def __str__(self):
        return self.tipo + " " + str(self.usuario) + " " + str(self.vehiculo) + " " + str(self.estacionamiento) + " " + str(self.fecha)

# actividad(numero_alertas,usuario,vehiculo,estacionamiento,ticket,tipo,fecha)
class Actividad(models.Model):
    """Tabla que representa el historial de cada persona en cada C.C.
    
    Miembros:
        * numero_actividad: se refiere al indice que agrega la BD.
        * usuario: Se refiere a la persona que se le genera la actividad.
        * vehiculo: se refiere al vehiculo al cual se le genera la actividad.
        * estacionamiento: se refiere al estacionamiento donde sucede la actividad.
        * ticket: representa el ticket del usuario al momento de entrar o salir del estacionamiento.
        * tipo: tipo de actividad.
        * fecha: la fecha en la que ocurre la actividad.
    
    tipo: 
        * entrada_estacionamiento, 
        * salida_estacionamiento,
        * comunicacion_enviada,
        * ticket_cambiado,
    """
    numero_actividad = models.AutoField(primary_key = True) 
    usuario = models.ForeignKey(Persona, on_delete=models.CASCADE, null=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=False)
    estacionamiento = models.ForeignKey(Estacionamiento, on_delete=models.CASCADE, null=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
    tipo = models.CharField(max_length=200)
    fecha = models.DateTimeField('fecha de actividad', default=timezone.now)
    
    def __str__(self):
        return self.tipo + " " + str(self.usuario) + " " + str(self.vehiculo) + " " + str(self.estacionamiento) + " " + str(self.fecha)