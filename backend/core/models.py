from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
from django.db import models
from django.utils import timezone
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('VENDEDOR', 'Vendedor'),
        ('COMPRADOR', 'Comprador'),
    )

    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=150)
    tipo_usuario = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    aceita_termos = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    data_criacao = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'tipo_usuario']

    def __str__(self):
        return self.email
    
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)
    reset_password_expires = models.DateTimeField(blank=True, null=True)

class Produto(models.Model):
    vendedor = models.ForeignKey(
        'Vendedor',
        on_delete=models.CASCADE,
        related_name='produtos'
    )
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    estoque = models.PositiveIntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class ImagemProduto(models.Model):
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='imagens'
    )
    imagem = models.ImageField(upload_to='produtos/')
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagem de {self.produto.nome}"
    
class Vendedor(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendedor'
    )
    nome_loja = models.CharField(max_length=255, blank=True, null=True)
    descricao_loja = models.TextField(blank=True, null=True)
    foto_perfil_loja = models.ImageField(
        upload_to='lojas/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome_loja or self.usuario.nome

class Category(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
