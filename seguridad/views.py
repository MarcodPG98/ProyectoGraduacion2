from rest_framework import viewsets
from .models import ConfiguracionSeguridad
from .serializers import UsuarioSerializer, CorreoElectricoSerializer, PhishingReporteSerializer, ConfiguracionSeguridadSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json, joblib, os, logging
from django.views.decorators.csrf import csrf_exempt
from .models import PhishingReporte, CorreoElectronico, Usuario
from django.contrib.auth.hashers import make_password

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

class CorreoElectronicoViewSet(viewsets.ModelViewSet):
    queryset = CorreoElectronico.objects.all()
    serializer_class = CorreoElectricoSerializer

class PhishingReporteViewSet(viewsets.ModelViewSet):
    queryset = PhishingReporte.objects.all()
    serializer_class = PhishingReporteSerializer

class ConfiguracionSeguridadViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionSeguridad.objects.all()
    serializer_class = ConfiguracionSeguridadSerializer
# Vista para registrar los usuarios en la aplicación móvil
@csrf_exempt
def registrar_usuario(request):
    if request.method == 'POST':
        try:
            # Obtener los datos de la solicitud
            data = json.loads(request.body)
            nombre = data.get('nombre')
            email = data.get('email')
            password = data.get('password')

            # Validaciones básicas
            if not nombre or not email or not password:
                return JsonResponse({'error': 'Todos los campos (nombre, email, password) son obligatorios.'}, status=400)

            if Usuario.objects.filter(email=email).exists():
                return JsonResponse({'error': 'El email ya está registrado.'}, status=400)

            # Crear el usuario
            usuario = Usuario.objects.create(
                nombre=nombre,
                email=email,
                password=make_password(password)  # Encriptar el password
            )

            return JsonResponse({
                'mensaje': 'Usuario registrado con éxito.',
                'usuario': {
                    'id': usuario.id,
                    'nombre': usuario.nombre,
                    'email': usuario.email,
                    'fecha_registro': usuario.fecha_registro,
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Solicitud no válida. Asegúrate de enviar un JSON válido.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido. Usa POST.'}, status=405)

# Vista registrar correo electrónico por medio de validaciones
@csrf_exempt
def registrar_correo(request):
    if request.method == 'POST':
        try:
            # Leer datos del cuerpo de la solicitud
            data = json.loads(request.body)
            remitente = data.get('remitente')
            destinatario = data.get('destinatario')  # El correo del destinatario
            asunto = data.get('asunto')
            contenido = data.get('contenido')

            # Validar los datos
            if not remitente or not destinatario or not asunto or not contenido:
                return JsonResponse({'error': 'Faltan datos obligatorios.'}, status=400)

            # Verificar si el destinatario coincide con un usuario registrado
            try:
                usuario = Usuario.objects.get(email=destinatario)
            except Usuario.DoesNotExist:
                return JsonResponse({'error': f'El destinatario {destinatario} no está registrado en el sistema.'}, status=404)

            # Registrar el correo en la base de datos
            correo = CorreoElectronico.objects.create(
                usuario=usuario,
                remitente=remitente,
                asunto=asunto,
                contenido=contenido
            )

            return JsonResponse({
                'message': 'Correo registrado exitosamente.',
                'correo': {
                    'id': correo.id,
                    'usuario_id': usuario.id,
                    'remitente': remitente,
                    'destinatario': destinatario,
                    'asunto': asunto,
                    'contenido': contenido,
                    'fecha_recibido': correo.fecha_recibido.strftime('%Y-%m-%d %H:%M:%S')
                }
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

# Vista para recibir correo electrónico y verificar con el si es malicioso o legitimo
@csrf_exempt
def verificar_correo(request):
    if request.method == 'POST':
        try:
            # Obtener el contenido del correo, el usuario_id, el remitente y el asunto desde la solicitud
            data = json.loads(request.body)
            contenido = data.get('contenido')
            usuario_id = data.get('usuario_id')
            remitente = data.get('remitente')
            asunto = data.get('asunto')

            logging.basicConfig(level=logging.DEBUG)

            # Registro de datos recibidos
            logging.debug(f'Datos recibidos: {data}')

            if not contenido or not usuario_id or not remitente or not asunto:
                return JsonResponse({'error': 'Faltan datos (contenido, usuario_id, remitente o asunto).'}, status=400)

            # Verificar si el usuario existe en la base de datos
            try:
                usuario = Usuario.objects.get(id=usuario_id)
            except Usuario.DoesNotExist:
                return JsonResponse({'error': f'No se encontró un usuario con ID {usuario_id}.'}, status=404)

            # Cargar el modelo y el vectorizador
            modelo_path = os.path.join('seguridad', 'models', 'modelo_spam.pkl')
            vectorizador_path = os.path.join('seguridad', 'models', 'vectorizer.pkl')

            # Validar que los archivos existan
            if not os.path.exists(modelo_path) or not os.path.exists(vectorizador_path):
                return JsonResponse({'error': 'El modelo o vectorizador no se encuentran en la carpeta especificada.'}, status=500)

            modelo = joblib.load(modelo_path)
            vectorizador = joblib.load(vectorizador_path)

            # Preprocesar el contenido del correo y hacer la predicción
            correo_vectorizado = vectorizador.transform([contenido])
            logging.debug(f'Vectorización del contenido: {correo_vectorizado}')

            prediccion = modelo.predict(correo_vectorizado)[0]  # 1: malicioso, 0: legítimo
            logging.debug(f'Resultado de la predicción: {prediccion}')

            # Asignar la etiqueta basada en la predicción
            etiqueta = 'malicioso' if prediccion == 1 else 'legítimo'

            # Guardar la información en la tabla CorreoElectronico
            CorreoElectronico.objects.create(
                usuario=usuario,
                contenido=contenido,
                es_phishing=prediccion,  # Guardamos el valor exacto de la predicción
                remitente=remitente,
                asunto=asunto,
                etiqueta=etiqueta  # Asegúrate de guardar la etiqueta aquí
            )

            # Responder con la predicción y el estado del correo
            return JsonResponse({
                'usuario_id': usuario_id,
                'contenido': contenido,
                'es_phishing': bool(prediccion),  # 1: malicioso, 0: legítimo
                'remitente': remitente,
                'asunto': asunto,
                'etiqueta': etiqueta,  # Incluir la etiqueta en la respuesta
                'descripcion': 'Correo malicioso' if prediccion == 1 else 'Correo legítimo'
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Vista para verificar el contenido del correo y devolver la predicción
@csrf_exempt
def predecir(request):
    if request.method == 'POST':
        try:
            # Obtener el usuario_id desde la solicitud
            data = json.loads(request.body)
            usuario_id = data.get('usuario_id')

            if not usuario_id:
                return JsonResponse({'error': 'Falta el usuario_id.'}, status=400)

            # Verificar si el usuario existe en la tabla CorreoElectrico
            correo = CorreoElectronico.objects.filter(
                usuario_id=usuario_id).first()  # Obtener el primer correo asociado al usuario

            if not correo:
                return JsonResponse({'error': f'No se encontró ningún correo asociado al usuario con ID {usuario_id}.'},
                                    status=404)

            # Obtener el valor de es_phishing
            es_phishing = correo.es_phishing  # 1: malicioso, 0: legítimo

            # Crear un informe en la tabla PhishingReporte
            descripcion = 'Correo legítimo' if es_phishing == 0 else 'Correo malicioso'
            phishing_reporte = PhishingReporte.objects.create(
                correo=correo,  # Relacionar con el correo
                usuario=correo.usuario,  # Relacionar con el usuario que posee el correo
                descripcion=descripcion,  # Descripción basada en la predicción
            )

            # Responder con la predicción y la descripción
            return JsonResponse({
                'usuario_id': usuario_id,
                'correo_id': correo.id,
                'es_phishing': es_phishing,
                'descripcion': descripcion
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
