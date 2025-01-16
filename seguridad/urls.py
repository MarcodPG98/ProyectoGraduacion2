from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, CorreoElectricoViewSet, PhishingReporteViewSet, ConfiguracionSeguridadViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'correos', CorreoElectricoViewSet)
router.register(r'reportes', PhishingReporteViewSet)
router.register(r'configuraciones', ConfiguracionSeguridadViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
