from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    RegisterUserSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from .serializers import RegisterUserSerializer
from .models import User
from .serializers import LoginSerializer
from rest_framework import generics, permissions
from core.models import Vendedor
from core.serializers import VendedorSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from core.models import Vendedor, Produto, ImagemProduto
from core.serializers import (
    VendedorSerializer,
    ProdutoSerializer,
    ProdutoCreateUpdateSerializer,
    ImagemProdutoSerializer
)

class RegisterVendedorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tipo_usuario='VENDEDOR')
            return Response(
                {"message": "Vendedor cadastrado com sucesso"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterCompradorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tipo_usuario='COMPRADOR')
            return Response(
                {"message": "Comprador cadastrado com sucesso"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class IsVendedor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'vendedor')
        )

class PerfilLojaView(generics.RetrieveUpdateAPIView):
    serializer_class = VendedorSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendedor]

    def get_object(self):
        return self.request.user.vendedor

class ProdutoListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsVendedor]

    def get_queryset(self):
        return Produto.objects.filter(vendedor=self.request.user.vendedor)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProdutoCreateUpdateSerializer
        return ProdutoSerializer

    def perform_create(self, serializer):
        serializer.save(vendedor=self.request.user.vendedor)

class ProdutoDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsVendedor]
    lookup_url_kwarg = 'produto_id'

    def get_queryset(self):
        return Produto.objects.filter(vendedor=self.request.user.vendedor)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProdutoCreateUpdateSerializer
        return ProdutoSerializer

class UploadImagemProdutoView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsVendedor]

    def post(self, request, produto_id):
        try:
            produto = Produto.objects.get(
                id=produto_id,
                vendedor=request.user.vendedor
            )
        except Produto.DoesNotExist:
            return Response(
                {"detail": "Produto não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        arquivos = request.FILES.getlist('imagens')
        imagens_criadas = []

        for arquivo in arquivos:
            img = ImagemProduto.objects.create(
                produto=produto,
                imagem=arquivo
            )
            imagens_criadas.append(img)

        serializer = ImagemProdutoSerializer(imagens_criadas, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VitrineProdutoListView(generics.ListAPIView):
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        queryset = Produto.objects.all()

        categoria = self.request.query_params.get('categoria')
        nome = self.request.query_params.get('nome')

        if categoria:
            queryset = queryset.filter(categoria__icontains=categoria)
        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        return queryset


class VitrineProdutoDetailView(generics.RetrieveAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    lookup_url_kwarg = 'produto_id'

from rest_framework.permissions import IsAuthenticated


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "email": user.email,
            "nome": user.nome,
            "tipo_usuario": user.tipo_usuario
        })

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response({
            "message": "Token de recuperação gerado.",
            "token": token
        })


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Senha redefinida com sucesso."})

class IsVendedor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'vendedor')
        )

class PerfilLojaView(generics.RetrieveUpdateAPIView):
    serializer_class = VendedorSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendedor]

    def get_object(self):
        return self.request.user.vendedor
    
from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(vendedor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(vendedor=self.request.user)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(vendedor=self.request.user)

class VariationCreateView(generics.CreateAPIView):
    serializer_class = VariationSerializer
    permission_classes = [permissions.IsAuthenticated]

class VariationListView(generics.ListAPIView):
    serializer_class = VariationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        produto_id = self.kwargs["produto_id"]
        return Variation.objects.filter(produto_id=produto_id)

class VariationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VariationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Variation.objects.all()
