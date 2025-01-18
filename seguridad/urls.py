from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UsuarioViewSet, CorreoElectricoViewSet, PhishingReporteViewSet, ConfiguracionSeguridadViewSet,
                    UsuarioListView)
from . import views

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'correos', CorreoElectricoViewSet)
router.register(r'reportes', PhishingReporteViewSet)
router.register(r'configuraciones', ConfiguracionSeguridadViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('verificar_correo/', views.verificar_correo, name='verificar_correo'),
    path('predecir/', views.predecir, name='predecir'),
]
