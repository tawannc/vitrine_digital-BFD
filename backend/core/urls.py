from django.urls import path
from .views import PasswordResetConfirmView, PasswordResetRequestView, RegisterVendedorView, RegisterCompradorView
from .views import LoginView
from .views import MeView
from core.views import (
    PerfilLojaView,
    ProdutoListCreateView,
    ProdutoDetailView,
    UploadImagemProdutoView,
    VitrineProdutoListView,
    VitrineProdutoDetailView
)
from .views import CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path('register/vendedor/', RegisterVendedorView.as_view()),
    path('register/comprador/', RegisterCompradorView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
    path('password-reset/', PasswordResetRequestView.as_view()),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view()),
    path('loja/', PerfilLojaView.as_view()),
    path('produtos/', ProdutoListCreateView.as_view()),
    path('produtos/<int:produto_id>/', ProdutoDetailView.as_view()),
    path('produtos/<int:produto_id>/imagens/', UploadImagemProdutoView.as_view()),
    path('vitrine/produtos/', VitrineProdutoListView.as_view()),
    path('vitrine/produtos/<int:produto_id>/', VitrineProdutoDetailView.as_view()),
    path("categorias/", CategoryListCreateView.as_view()),
    path("categorias/<int:pk>/", CategoryDetailView.as_view()),
]
