from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Reserva(models.Model):
    ESTADOS_RESERVA = [
        ('RESERVADO', 'Reservado'),
        ('COMPLETADA', 'Completada'),
        ('ANULADA', 'Anulada'),
        ('NO_ASISTEN', 'No Asisten'),
    ]

    nombre_persona = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    fecha_reserva = models.DateField()
    hora = models.TimeField()
    cantidad_personas = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(15)])
    estado = models.CharField(max_length=20, choices=ESTADOS_RESERVA)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva - {self.nombre_persona} - {self.fecha_reserva}"

