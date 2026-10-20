from django.test import TestCase
from django.urls import reverse
from datetime import date, time
from django.contrib.auth import get_user_model

from .models import Cita, Mascota
from poblar_datos import generar


class CitasIndexTests(TestCase):
    def setUp(self):
        self.mascota = Mascota.objects.create(
            nombre='Luna',
            especie='Perro',
            raza='Mestiza',
            nombre_dueno='Ana',
        )
        Cita.objects.create(
            mascota=self.mascota,
            fecha=date(2026, 10, 20),
            hora=time(9, 0),
            motivo='Control',
            estado='pendiente',
        )
        Cita.objects.create(
            mascota=self.mascota,
            fecha=date(2026, 10, 20),
            hora=time(10, 0),
            motivo='Vacuna',
            estado='atendida',
        )
        Cita.objects.create(
            mascota=self.mascota,
            fecha=date(2026, 10, 21),
            hora=time(11, 0),
            motivo='Consulta',
            estado='cancelada',
        )

    def test_lists_all_dates_and_states_without_filters(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['citas'].count(), 3)

    def test_filters_by_date_and_state(self):
        response = self.client.get(
            reverse('index'),
            {'fecha': '2026-10-20', 'estado': 'atendida'},
        )

        self.assertEqual(response.status_code, 200)
        citas = response.context['citas']
        self.assertEqual(citas.count(), 1)
        self.assertEqual(citas.first().estado, 'atendida')


class PoblarDatosTests(TestCase):
    def test_generar_is_repeatable_and_keeps_existing_records(self):
        mascota_existente = Mascota.objects.create(
            nombre='Mía',
            especie='Gato',
            raza='Común',
            nombre_dueno='Dueña existente',
        )
        Cita.objects.create(
            mascota=mascota_existente,
            fecha=date(2026, 10, 20),
            hora=time(8, 0),
            motivo='Cita existente',
            estado='pendiente',
        )

        generar()
        generar()

        self.assertEqual(Mascota.objects.count(), 21)
        self.assertEqual(Cita.objects.count(), 21)
        self.assertTrue(Cita.objects.filter(motivo='Cita existente').exists())


class AdminAccessTests(TestCase):
    def setUp(self):
        self.admin_url = reverse('admin:index')
        self.login_url = reverse('admin:login')

    def test_anonymous_user_is_redirected_to_admin_login(self):
        response = self.client.get(self.admin_url)

        self.assertRedirects(
            response,
            f'{self.login_url}?next={self.admin_url}',
        )

    def test_staff_user_cannot_log_in_to_admin(self):
        user = get_user_model().objects.create_user(
            username='staff',
            password='staff-password',
            is_staff=True,
        )

        response = self.client.post(
            self.login_url,
            {'username': user.username, 'password': 'staff-password'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_superuser_can_access_admin(self):
        user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin-password',
        )

        self.client.force_login(user)
        response = self.client.get(self.admin_url)

        self.assertEqual(response.status_code, 200)
