from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Bitacora, Ingreso, Usuario


class ApiCrudTests(APITestCase):
	def test_crud_and_related_data_for_all_resources(self):
		funcionario_response = self.client.post(
			'/api/funcionarios/',
			{
				'nombres': 'Ana',
				'apellidos': 'Perez',
				'documento': '100200300',
				'cargo': 'Analista',
				'telefono': '3001234567',
				'correo': 'ana@example.com',
				'estado': True,
			},
			format='json',
		)
		self.assertEqual(funcionario_response.status_code, status.HTTP_201_CREATED)
		funcionario_id = funcionario_response.data['id']

		usuario_response = self.client.post(
			'/api/usuarios/',
			{
				'funcionario': funcionario_id,
				'username': 'ana.perez',
				'password': 'ClaveSegura123!',
				'tipo_usuario': 'FUNCIONARIO',
				'estado': True,
				'permisos': 'consultar',
			},
			format='json',
		)
		self.assertEqual(usuario_response.status_code, status.HTTP_201_CREATED)
		usuario_id = usuario_response.data['id']
		self.assertNotIn('password', usuario_response.data)
		self.assertEqual(
			usuario_response.data['funcionario_detalle']['documento'],
			'100200300',
		)
		self.assertTrue(
			check_password(
				'ClaveSegura123!',
				Usuario.objects.get(pk=usuario_id).password,
			)
		)

		ingreso_response = self.client.post(
			'/api/ingresos/',
			{
				'usuario': usuario_id,
				'fecha_ingreso': '2025-01-01T09:00:00Z',
				'ip': '127.0.0.1',
			},
			format='json',
		)
		self.assertEqual(ingreso_response.status_code, status.HTTP_201_CREATED)
		ingreso_id = ingreso_response.data['id']
		self.assertEqual(
			ingreso_response.data['usuario_detalle']['username'],
			'ana.perez',
		)

		bitacora_response = self.client.post(
			'/api/bitacoras/',
			{
				'usuario': usuario_id,
				'accion': 'CREAR',
				'descripcion': 'Se creó un registro de prueba.',
			},
			format='json',
		)
		self.assertEqual(bitacora_response.status_code, status.HTTP_201_CREATED)
		bitacora_id = bitacora_response.data['id']
		self.assertEqual(
			bitacora_response.data['usuario_detalle']['username'],
			'ana.perez',
		)

		for endpoint, record_id in (
			('funcionarios', funcionario_id),
			('usuarios', usuario_id),
			('ingresos', ingreso_id),
			('bitacoras', bitacora_id),
		):
			with self.subTest(endpoint=endpoint):
				self.assertEqual(
					self.client.get(f'/api/{endpoint}/').status_code,
					status.HTTP_200_OK,
				)
				self.assertEqual(
					self.client.get(f'/api/{endpoint}/{record_id}/').status_code,
					status.HTTP_200_OK,
				)

		update_response = self.client.patch(
			f'/api/funcionarios/{funcionario_id}/',
			{'cargo': 'Coordinadora'},
			format='json',
		)
		self.assertEqual(update_response.status_code, status.HTTP_200_OK)
		self.assertEqual(update_response.data['cargo'], 'Coordinadora')

		usuario_update = self.client.patch(
			f'/api/usuarios/{usuario_id}/',
			{'permisos': 'consultar,crear'},
			format='json',
		)
		self.assertEqual(usuario_update.status_code, status.HTTP_200_OK)
		ingreso_update = self.client.patch(
			f'/api/ingresos/{ingreso_id}/',
			{'fecha_salida': '2025-01-01T17:00:00Z'},
			format='json',
		)
		self.assertEqual(ingreso_update.status_code, status.HTTP_200_OK)
		bitacora_update = self.client.patch(
			f'/api/bitacoras/{bitacora_id}/',
			{'descripcion': 'Descripción actualizada.'},
			format='json',
		)
		self.assertEqual(bitacora_update.status_code, status.HTTP_200_OK)

		for endpoint, record_id in (
			('ingresos', ingreso_id),
			('bitacoras', bitacora_id),
			('usuarios', usuario_id),
			('funcionarios', funcionario_id),
		):
			with self.subTest(deleted_endpoint=endpoint):
				delete_response = self.client.delete(
					f'/api/{endpoint}/{record_id}/'
				)
				self.assertEqual(
					delete_response.status_code,
					status.HTTP_204_NO_CONTENT,
				)
				self.assertEqual(
					self.client.get(f'/api/{endpoint}/{record_id}/').status_code,
					status.HTTP_404_NOT_FOUND,
				)


