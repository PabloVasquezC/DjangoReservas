from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre_persona', 'telefono', 'fecha_reserva', 'hora', 'cantidad_personas', 'estado', 'observacion']
