from rest_framework import serializers
from .models import Usuario, CorreoElectrico, PhishingReporte, ConfiguracionSeguridad

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class CorreoElectricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorreoElectrico
        fields = '__all__'

class PhishingReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhishingReporte
        fields = '__all__'

class ConfiguracionSeguridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionSeguridad
        fields = '__all__'
