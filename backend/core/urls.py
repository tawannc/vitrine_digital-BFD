from django.urls import path
from .views import RegisterVendedorView, RegisterCompradorView
from .views import LoginView

urlpatterns = [
    path('register/vendedor/', RegisterVendedorView.as_view()),
    path('register/comprador/', RegisterCompradorView.as_view()),
    path('login/', LoginView.as_view()),
]

from .views import MeView

urlpatterns = [
    path('register/vendedor/', RegisterVendedorView.as_view()),
    path('register/comprador/', RegisterCompradorView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
]
