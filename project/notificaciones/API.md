# API.

## Enviar correo de entrada automaticamente.
```
url = /notificaciones/enviar_correo_entrada
método = POST
datos =
{
  rif: rif del centro comercial
  nombre_estacionamiento: nombre del centro comercial
  monto_tarifa: trarifa del estacionamiento
  tipo_tarifa: "tarifa plana " if estacionamiento.tarifa_plana else "tafifa por horas"

  ticket: ticket asignado al momento de la entrada
  hora_entrada: hora de entrada del vehiculo
  <!-- hora_salida: Hora de egreso vehicular -->

  placa: carro en gestión
  email: email del dueno del carro a contactar
  nombre_dueno: dueno del vehiculo.
  apellido_dueno: Apellido del dueno del vehiculo

  }
```
