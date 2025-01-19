from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UsuarioViewSet, CorreoElectronicoViewSet, PhishingReporteViewSet, ConfiguracionSeguridadViewSet,
                    UsuarioListView)
from . import views

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'correos', CorreoElectronicoViewSet)
router.register(r'reportes', PhishingReporteViewSet)
router.register(r'configuraciones', ConfiguracionSeguridadViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('registrar_correo/', views.registrar_correo, name='registrar_correo'),
    path('listar_usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('verificar_correo/', views.verificar_correo, name='verificar_correo'),
    path('predecir/', views.predecir, name='predecir'),
]
