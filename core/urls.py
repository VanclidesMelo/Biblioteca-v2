from django.urls import path
from .import views

urlpatterns = [
    path("livros/", views.LivroList.as_view(), name="livro-list"),
    path("livros/<int:pk>/", views.LivroDetail.as_view(), name="livro-detail"),

    path("autores/", views.AutorList.as_view(), name="autor-list"),
    path("autores/<int:pk>/", views.AutorDetail.as_view(), name="autor-detail"),

    path("categorias/", views.CategoriaList.as_view(), name="categoria-list"),
    path("categorias/<int:pk>/", views.CategoriaDetail.as_view(),
         name="categoria-detail")
]
