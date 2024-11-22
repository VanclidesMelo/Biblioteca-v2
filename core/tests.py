from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Colecao, Livro, Categoria, Autor

class PermissaoColecaoTests(APITestCase):

    def setUp(self):
        # Usuários
        self.user = User.objects.create_user(username='user1', password='pass1')
        self.outro_usuario = User.objects.create_user(username='user2', password='pass2')
        self.client.login(username='user1', password='pass1')

        # Dados para teste
        self.categoria = Categoria.objects.create(nome="Ficção Científica")
        self.autor = Autor.objects.create(nome="Isaac Asimov")
        self.livro = Livro.objects.create(
            titulo="Fundação",
            autor=self.autor,
            categoria=self.categoria,
            publicado_em="1951-06-01"
        )
        self.colecao = Colecao.objects.create(
            nome="Minha Coleção",
            descricao="Coleção pessoal",
            colecionador=self.user
        )
        self.url = f'/colecoes/{self.colecao.id}/'

    def test_proprietario_pode_editar_colecao(self):
        data = {
            "nome": "Coleção Atualizada",
            "descricao": "Descrição atualizada",
            "livro_ids": [self.livro.id]
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], "Coleção Atualizada")

    def test_usuario_nao_proprietario_nao_pode_editar_colecao(self):
        self.client.logout()
        self.client.login(username='user2', password='pass2')

        data = {
            "nome": "Tentativa de Atualização",
            "descricao": "Descrição alterada"
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_usuario_nao_proprietario_nao_pode_deletar_colecao(self):
        self.client.logout()
        self.client.login(username='user2', password='pass2')

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Colecao.objects.count(), 1)  # A coleção ainda existe

    def test_usuario_autenticado_pode_listar_suas_colecoes(self):
        response = self.client.get('/colecoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], "Minha Coleção")

    def test_usuario_nao_autenticado_nao_pode_listar_colecoes(self):
        self.client.logout()

        response = self.client.get('/colecoes/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_usuario_autenticado_nao_pode_listar_colecoes_de_outro_usuario(self):
        Colecao.objects.create(
            nome="Coleção de Outro Usuário",
            descricao="Esta não deve aparecer",
            colecionador=self.outro_usuario
        )
        response = self.client.get('/colecoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Apenas as coleções do user1
        self.assertEqual(response.data[0]['nome'], "Minha Coleção")
