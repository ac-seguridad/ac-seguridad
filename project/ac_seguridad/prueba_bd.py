from ac_seguridad.models import Alerta, Estacionamiento, Persona, Vehiculo
from django.utils import timezone

# Cargar estacionamiento de prueba.
estacionamiento = Estacionamiento.objects.get(rif="J-1231")

# Cargar usuario de prueba.
persona = Persona.objects.get(cedula="C-21312")
anabel = Persona.objects.get(cedula="24944655")

# Cargar vehículos de prueba.
veh1 = Vehiculo.objects.get(placa="AE338FG")
veh2 = Vehiculo.objects.get(placa="AE800MB")
nissan = Vehiculo.objects.get(placa="EAM20Z")

# Definición de ciertas alertas.
timestamp = timezone.now()
alerta_entrada = Alerta(tipo="entrada_estacionamiento",
                        usuario = persona,
                        vehiculo = veh1,
                        estacionamiento = estacionamiento,
                        fecha = timestamp - timezone.timedelta(days=100)
                        )
alerta_salida = Alerta(tipo="salida_estacionamiento",
                       usuario = persona,
                       vehiculo = veh1,
                       estacionamiento = estacionamiento,
                       fecha = timestamp - timezone.timedelta(days=100) + timezone.timedelta(minutes=100)
                       )
alerta_ticket = Alerta(tipo="ticket_asignado",
                       usuario = persona,
                       vehiculo = veh1,
                       estacionamiento = estacionamiento,
                       fecha = timestamp - timezone.timedelta(days=100)
                       )
alerta_ticket_pagado = Alerta(tipo="ticket_pagado",
                              usuario = persona,
                              vehiculo = veh1,
                              estacionamiento = estacionamiento,
                              fecha = timestamp - timezone.timedelta(days=100) + timezone.timedelta(minutes=85)
                              )
alerta_placa_correcta = Alerta(tipo="placa_correcta",
                              usuario = persona,
                              vehiculo = veh1,
                              estacionamiento = estacionamiento,
                              fecha = timestamp - timezone.timedelta(days=100)
                              )
alerta_placa_incorrecta = Alerta(tipo="placa_desconocida",
                                 usuario = None,
                                 vehiculo = None,
                                 estacionamiento = estacionamiento,
                                 fecha = timestamp - timezone.timedelta(days=100)
                                 )

alerta_entrada.save()
alerta_salida.save()
alerta_ticket.save()
alerta_ticket_pagado.save()
alerta_placa_correcta.save()
alerta_placa_incorrecta.save()

alerta_anabel = Alerta(tipo="entrada_estacionamiento",
                       usuario = persona,
                       vehiculo = veh1,
                       estacionamiento = estacionamiento,
                       fecha = timestamp - timezone.timedelta(days=100)
                       )

# # Crear ocurrencias de alertas.
# timestamp = timezone.now()
# ocurrencia_a1 = OcurreA(cedula_usuario=persona,
#                         numero_alertas=alerta_entrada,
#                         fecha_alertas=timestamp - timezone.timedelta(days=100)
#                         )
# ocurrencia_en1 = OcurreEn(rif = estacionamiento,
#                           numero_alertas = alerta_entrada,
#                           fecha_alertas  = timestamp - timezone.timedelta(days=100)
#                           )
                          
# ocurrencia_a1.save()
# ocurrencia_en1.save()


