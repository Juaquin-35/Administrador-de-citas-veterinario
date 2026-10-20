from django.shortcuts import render, redirect, get_object_or_404
from .models import Cita
from .forms import MascotaForm, CitaForm

def index(request):
    fecha_filtro = request.GET.get('fecha', '')
    estado_filtro = request.GET.get('estado', '')
    citas = Cita.objects.all()
    if fecha_filtro:
        citas = citas.filter(fecha=fecha_filtro)
    if estado_filtro:
        citas = citas.filter(estado=estado_filtro)
    citas = citas.order_by('fecha', 'hora')
    return render(request, 'index.html', {
        'citas': citas,
        'fecha_filtro': fecha_filtro,
        'estado_filtro': estado_filtro,
        'estados': Cita.ESTADO_CHOICES,
    })

def registrar_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_cita')
    else:
        form = MascotaForm()
    return render(request, 'mascota.html', {'form': form})

def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CitaForm()
    return render(request, 'crear.html', {'form': form})

def cambiar_estado_cita(request, cita_id, nuevo_estado):
    cita = get_object_or_404(Cita, id=cita_id)
    if nuevo_estado in ['pendiente', 'atendida', 'cancelada']:
        cita.estado = nuevo_estado
        cita.save()
    return redirect('index')