from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

cedulaValidator = RegexValidator(regex=r'^V\-\d{6,8}$', message="Introduzca una cédula del estilo: V-00000000", code=None, inverse_match=None, flags=0)
telefonoValidator = RegexValidator(regex=r'^\+?(58)?\d{9,15}$', message="Introduzca un teléfono del estilo: +58XXXXXXXXXX", code=None, inverse_match=None, flags=0)

class SignUpForm(UserCreationForm):
    nombre = forms.CharField(max_length=20) #crea las columnas
    apellido = forms.CharField(max_length=25)
    cedula = forms.CharField(max_length=20) 
    telefono = forms.CharField(max_length=20)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nombre', 'apellido', 'cedula', 'telefono', 'email')