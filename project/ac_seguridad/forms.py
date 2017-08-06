from django.forms import ModelForm
from django.forms import Form
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Persona

cedulaValidator = RegexValidator(regex=r'^V\-\d{6,8}$', message="Introduzca una cédula del estilo: V-00000000", code=None, inverse_match=None, flags=0)
telefonoValidator = RegexValidator(regex=r'^\+?(58)?\d{9,15}$', message="Introduzca un teléfono del estilo: +58XXXXXXXXXX", code=None, inverse_match=None, flags=0)

class SignUpPersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'cedula', 'telefono', 'email']