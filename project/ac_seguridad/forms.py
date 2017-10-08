from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Persona, Estacionamiento, Vehiculo

cedulaValidator = RegexValidator(regex=r'^V\-\d{6,8}$', message="Introduzca una cédula del estilo: V-00000000", code=None, inverse_match=None, flags=0)
telefonoValidator = RegexValidator(regex=r'^\+?(58)?\d{9,15}$', message="Introduzca un teléfono del estilo: +58XXXXXXXXXX", code=None, inverse_match=None, flags=0)

class SignUpPersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'cedula', 'telefono', 'email']
        
class SignUpEstacionamientoForm(ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ['rif', 'nombre', 'numero_de_puestos', 'acceso_restringido', 'email']
        
class VehiculoForm(ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'marca','modelo','year']
        
class PagoEstacionamientoForm(forms.Form):
    numero_ticket = forms.IntegerField(label="Número de ticket",
                                       min_value=0)
    registrado_ticket = forms.BooleanField(label="¿El ticket está registrado?",
                                           required=False)
    
    
        