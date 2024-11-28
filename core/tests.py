from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
# Ajuste o nome da app e modelo de usuário conforme necessário
from .models import Colecao, Usuario


class ColecaoTests(APITestCase):
    def setUp(self):
        """
        Configuração inicial para os testes.
        """
        # Criação de dois usuários para testar permissões
        self.user1 = Usuario.objects.create_user(
            username="user1", password="senha123")
        self.user2 = Usuario.objects.create_user(
            username="user2", password="senha456")

        # Tokens de autenticação
        self.token_user1 = Token.objects.create(user=self.user1)
        self.token_user2 = Token.objects.create(user=self.user2)

        # Endpoint base para coleções
        self.colecao_list_url = reverse("colecao-list")

    def test_criar_colecao_usuario_autenticado(self):
        """
        Teste para criação de uma coleção por um usuário autenticado.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {
                                self.token_user1.key}")
        data = {"nome": "Minha Coleção de Livros"}
        response = self.client.post(self.colecao_list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Colecao.objects.count(), 1)
        self.assertEqual(Colecao.objects.get().colecionador, self.user1)

    def test_nao_autenticado_nao_pode_criar(self):
        """
        Teste para garantir que usuários não autenticados não possam criar coleções.
        """
        data = {"nome": "Coleção de Livros"}
        response = self.client.post(self.colecao_list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Colecao.objects.count(), 0)

    def test_apenas_colecionador_pode_editar(self):
        """
        Teste para garantir que apenas o colecionador pode editar sua coleção.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {
                                self.token_user1.key}")
        colecao = Colecao.objects.create(
            nome="Coleção do User1", colecionador=self.user1)

        # User1 tenta editar sua própria coleção
        edit_url = reverse("colecao-detail", kwargs={"pk": colecao.pk})
        data = {"nome": "Coleção Editada"}
        response = self.client.put(edit_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Colecao.objects.get(
            pk=colecao.pk).nome, "Coleção Editada")

        # User2 tenta editar a coleção de User1
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {
                                self.token_user2.key}")
        data = {"nome": "Tentativa de Edição"}
        response = self.client.put(edit_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Colecao.objects.get(
            pk=colecao.pk).nome, "Tentativa de Edição")

    def test_apenas_colecionador_pode_deletar(self):
        """
        Teste para garantir que apenas o colecionador pode deletar sua coleção.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {
                                self.token_user1.key}")
        colecao = Colecao.objects.create(
            nome="Coleção do User1", colecionador=self.user1)

        # User1 tenta deletar sua própria coleção
        delete_url = reverse("colecao-detail", kwargs={"pk": colecao.pk})
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Colecao.objects.count(), 0)

        # User2 tenta deletar a coleção de User1
        colecao = Colecao.objects.create(
            nome="Nova Coleção", colecionador=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {
                                self.token_user2.key}")
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Colecao.objects.count(), 1)

    def test_listar_colecoes_usuario_autenticado(self):
        """
        Teste para garantir que um usuário autenticado veja apenas suas coleções.
        """
        # Criar coleções para dois usuários
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {
                                self.token_user1.key}")
        Colecao.objects.create(nome="Coleção User1", colecionador=self.user1)
        Colecao.objects.create(nome="Outra Coleção User1",
                               colecionador=self.user1)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {
                                self.token_user2.key}")
        Colecao.objects.create(nome="Coleção User2", colecionador=self.user2)

        # User1 verifica suas coleções
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {
                                self.token_user1.key}")
        response = self.client.get(self.colecao_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Apenas coleções de User1

        # User2 verifica suas coleções
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {
                                self.token_user2.key}")
        response = self.client.get(self.colecao_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Apenas coleções de User2
