from rest_framework import viewsets
from .models import Usuario, CorreoElectrico, PhishingReporte, ConfiguracionSeguridad
from .serializers import UsuarioSerializer, CorreoElectricoSerializer, PhishingReporteSerializer, ConfiguracionSeguridadSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pickle,json
from .predictor import predecir_spam

def usuario_list(request):
    return JsonResponse({"mensaje": "Lista de usuarios (ejemplo)."})

def home(request):
    return HttpResponse("Bienvenido al backend de Phishing Protection.")

class UsuarioListView(APIView):
    permission_classes = [IsAuthenticated]

    # Manejar solicitudes GET (obtener usuarios)
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    # Manejar solicitudes POST (crear un usuario)
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

# Vista para recibir correo y devolver la predicción
@csrf_exempt
def predecir(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                # Leer los datos JSON del cuerpo de la solicitud
                data = json.loads(request.body)
                correo_texto = data.get('contenido')

                if correo_texto:
                    resultado = predecir_spam(correo_texto)
                    return JsonResponse({'resultado': resultado})
                else:
                    return JsonResponse({'error': 'No se proporcionó contenido en el correo'}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Error al procesar el JSON'}, status=400)
        else:
            return JsonResponse({'error': 'Tipo de contenido no permitido. Usa application/json.'}, status=415)

    return JsonResponse({'error': 'Método no permitido'}, status=405)