
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Customer, Favorite


class CustomerTests(APITestCase):
    def setUp(self):
        # cria um cliente padrão
        User.objects.create_superuser('admin', 'admin@magazineluiza.com.br', 'admin_pass')
        self.customer = Customer.objects.create(name='José da Silva', email='jose@silvacorp.com')

        # gera o token de autenticação utilizado pelos requests
        url = reverse('token_obtain_pair')
        data = {"username": "admin", "password": "admin_pass"}
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_token_invalid_credentials(self):
        url = reverse('token_obtain_pair')
        data = {"username": "admin", "password": "c3po"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_create(self):
        url = reverse('customers-list')
        data = {"name": "José da Silva", "email": "jsilva@jmail.com"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customer_create_duplicated_email(self):
        url = reverse('customers-list')
        data = {"name": "José da Silva", "email": "jose@silvacorp.com"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_details(self):
        url = reverse('customers-detail', kwargs={'pk': self.customer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_details_invalid_uuid(self):
        url = reverse('customers-detail', kwargs={'pk': 'r2d2'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_update(self):
        data = {"name": "José da Silva e Silva", "email": "jose@silvacorp.com"}
        url = reverse('customers-detail', kwargs={'pk': self.customer.id})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_update_invalid_uuid(self):
        data = {"name": "José da Silva e Silva", "email": "jose@silvacorp.com"}
        url = reverse('customers-detail', kwargs={'pk': 'bb8'})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_delete(self):
        url = reverse('customers-detail', kwargs={'pk': self.customer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_customer_delete_invalid_uuid(self):
        url = reverse('customers-detail', kwargs={'pk': 'hal9000'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_favorite_create(self):
        url = reverse('favorites-list')
        data = {"product_id": "a96b5916-9109-5d2e-138a-7b656efe1f92", "customer": self.customer.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_favorite_create_duplicated_product(self):
        Favorite.objects.create(product_id="a96b5916-9109-5d2e-138a-7b656efe1f92", customer=self.customer)
        url = reverse('favorites-list')
        data = {"product_id": "a96b5916-9109-5d2e-138a-7b656efe1f92", "customer": self.customer.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_favorite_create_invalid_product(self):
        url = reverse('favorites-list')
        data = {"product_id": "42", "customer": self.customer.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_favorite_delete(self):
        fav = Favorite.objects.create(product_id="a96b5916-9109-5d2e-138a-7b656efe1f92", customer=self.customer)
        url = reverse('favorites-detail', kwargs={'pk': fav.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_favorite_delete_invalid_uuid(self):
        url = reverse('favorites-detail', kwargs={'pk': 'towel'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_favorites(self):
        url = reverse('customers-favorites', kwargs={'pk': self.customer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_favorites_invalid_customer(self):
        url = reverse('customers-favorites', kwargs={'pk': 'dna'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_favorites_nonexistent_customer(self):
        url = reverse('customers-favorites', kwargs={'pk': 'd705e535-d31a-48b9-9bd7-c193053b5f82'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
