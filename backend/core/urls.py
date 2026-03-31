from django.urls import path
from .views import PasswordResetConfirmView, PasswordResetRequestView, RegisterVendedorView, RegisterCompradorView
from .views import LoginView
from .views import MeView

urlpatterns = [
    path('register/vendedor/', RegisterVendedorView.as_view()),
    path('register/comprador/', RegisterCompradorView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
    path('password-reset/', PasswordResetRequestView.as_view()),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view()),

]
