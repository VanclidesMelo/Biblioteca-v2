from django.urls import path
from .import views

urlpatterns = [
    path("livro/", views.LivroList.as_view(), name="livro-list"),
    path("livro/<int:pk>/", views.LivroDetail.as_view(), name="livro-detail"),

    path("autores/", views.AutorList.as_view(), name="autor-list"),
    path("autores/<int:pk>/", views.AutorDetail.as_view(), name="autor-detail"),

    path("categorias/", views.CategoriaList.as_view(), name="categoria-list"),
    path("categorias/<int:pk>/", views.CategoriaDetail.as_view(), name="categoria-detail"),

    path("colecoes/", views.ColecaoListCreate.as_view(), name='colecao-list'),
    path("colecoes/<int:pk>/", views.ColecaoDetail.as_view(), name='colecao-detail'),
]
