from .models import Livro, Categoria, Autor, Colecao
from .serializers import LivroSerializer, AutorSerializer, CategoriaSerializer, ColecaoSerializer
from rest_framework import generics, permissions
from .filters import LivroFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import ScopedRateThrottle


class LivroList(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    filterset_class = LivroFilter
    search_fields = ("^titulo",)
    ordering_fields = ["titulo", "autor", "categoria", "publicado_em"]
    name = "livro-list"
    throttle_scope = "livro"
    throttle_classes = (ScopedRateThrottle,)


class LivroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-detail"
    throttle_scope = "livro"
    throttle_classes = (ScopedRateThrottle,)


class AutorList(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-list"
    throttle_scope = "autor"
    throttle_classes = (ScopedRateThrottle,)


class AutorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-detail"
    throttle_scope = "autor"
    throttle_classes = (ScopedRateThrottle,)


class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    throttle_scope = "cagegoria"
    throttle_classes = (ScopedRateThrottle,)

    search_fields = ("^name",)
    ordering_fields = ["name"]
    name = "categotia-list"


class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-detail"
    throttle_scope = "categoria"
    throttle_classes = (ScopedRateThrottle,)

# Listar e criar coleções


class ColecaoListCreate(generics.ListCreateAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = [permissions.IsAuthenticated]
    name = "colecao-list"
    throttle_scope = "colecoes"
    throttle_classes = (ScopedRateThrottle,)

    def get_queryset(self):

        return Colecao.objects.filter(colecionador=self.request.user)

    def perform_create(self, serializer):

        serializer.save(colecionador=self.request.user)


class ColecaoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = [permissions.IsAuthenticated]
    name = "colecao-datail"
    throttle_scope = "colecoes"
    throttle_classes = (ScopedRateThrottle,)

    def get_queryset(self):
        # Apenas coleções do usuário autenticado
        return Colecao.objects.filter(colecionador=self.request.user)
