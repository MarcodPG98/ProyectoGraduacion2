from rest_framework import viewsets
from .models import Usuario, CorreoElectrico, PhishingReporte, ConfiguracionSeguridad
from .serializers import UsuarioSerializer, CorreoElectricoSerializer, PhishingReporteSerializer, ConfiguracionSeguridadSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Usuario
from .serializers import UsuarioSerializer
from django.http import HttpResponse
from django.http import JsonResponse

def usuario_list(request):
    return JsonResponse({"mensaje": "Lista de usuarios (ejemplo)."})

def home(request):
    return HttpResponse("Bienvenido al backend de Phishing Protection.")

class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

class CorreoElectricoViewSet(viewsets.ModelViewSet):
    queryset = CorreoElectrico.objects.all()
    serializer_class = CorreoElectricoSerializer

class PhishingReporteViewSet(viewsets.ModelViewSet):
    queryset = PhishingReporte.objects.all()
    serializer_class = PhishingReporteSerializer

class ConfiguracionSeguridadViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionSeguridad.objects.all()
    serializer_class = ConfiguracionSeguridadSerializer
