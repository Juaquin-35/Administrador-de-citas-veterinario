from django.db import models

# Create your models here.
class Mascota(models.Model):
    ESPECIE_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Ave', 'Ave'),
        ('Otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Mascota")
    especie = models.CharField(max_length=50, choices=ESPECIE_CHOICES, verbose_name="Especie")
    raza = models.CharField(max_length=100, verbose_name="Raza")
    nombre_dueno = models.CharField(max_length=150, verbose_name="Nombre del Dueño")
    telefono_dueno = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono del Dueño")

    def __str__(self):
        return f"{self.nombre} ({self.especie}) - Dueño: {self.nombre_dueno}"

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('atendida', 'Atendida'),
        ('cancelada', 'Cancelada'),
    ]

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas', verbose_name="Mascota")
    fecha = models.DateField(verbose_name="Fecha de la Cita")
    hora = models.TimeField(verbose_name="Hora de la Cita")
    motivo = models.TextField(verbose_name="Motivo de Consulta")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name="Estado")

    def __str__(self):
        return f"Cita {self.mascota.nombre} - {self.fecha} {self.hora} [{self.get_estado_display()}]"