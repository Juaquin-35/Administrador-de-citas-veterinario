import os
import django
from datetime import date, timedelta, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from citas.models import Mascota, Cita

def generar():
    nombres = [
        "Toby", "Luna", "Max", "Bella", "Rocky", "Coco", "Thor", "Simba",
        "Milo", "Nala", "Kira", "Bobi", "Zeus", "Lola", "Bruno", "Maya",
        "Luffy", "Sasha", "Oliver", "Cleo",
    ]
    especies = {
        'Perro': ['Labrador', 'Poodle', 'Bulldog'],
        'Gato': ['Siamés', 'Persa', 'Mestizo'],
        'Ave': ['Canario', 'Perico'],
    }
    duenos = [
        "Carlos Mendoza", "María Silva", "Andrés Gómez",
        "Valentina Rojas", "Javier López",
    ]
    motivos = [
        "Vacunación", "Control de peso", "Desparasitación",
        "Revisión general", "Limpieza dental",
    ]
    estados = [estado for estado, _ in Cita.ESTADO_CHOICES]

    for i, nombre in enumerate(nombres):
        especie = list(especies)[i % len(especies)]
        dueno = f"Demo - {duenos[i % len(duenos)]}"
        mascota, _ = Mascota.objects.get_or_create(
            nombre=nombre,
            nombre_dueno=dueno,
            defaults={
                'especie': especie,
                'raza': especies[especie][i % len(especies[especie])],
                'telefono_dueno': f"+569{10000000 + i:08d}",
            },
        )
        Cita.objects.update_or_create(
            mascota=mascota,
            motivo=f"[DEMO {i + 1:02d}] {motivos[i % len(motivos)]}",
            defaults={
                'fecha': date.today() + timedelta(days=(i % 5) - 1),
                'hora': time(hour=9 + (i % 9), minute=30 if i % 2 else 0),
                'estado': estados[i % len(estados)],
            },
        )

    print("Carga completada: 20 mascotas y citas de ejemplo (sin borrar datos existentes).")

if __name__ == '__main__':
    generar()