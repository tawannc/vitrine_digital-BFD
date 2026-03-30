from django.urls import path
from .views import RegisterVendedorView, RegisterCompradorView

urlpatterns = [
    path('register/vendedor/', RegisterVendedorView.as_view()),
    path('register/comprador/', RegisterCompradorView.as_view()),
]
