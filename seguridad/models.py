from django.db import models
from django.contrib.auth.models import User

# Modelo Usuario
class Usuario(models.Model):
    nombre = models.CharField(max_length=60)
    email = models.CharField(max_length=60, unique=True)  # Añade unique para evitar duplicados
    password = models.CharField(max_length=128)  # Aumenta el tamaño a 128
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

# Modelo Correo_Electrónico actualizado
class CorreoElectronico(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    remitente = models.CharField(max_length=70)
    asunto = models.CharField(max_length=70)
    contenido = models.TextField()
    fecha_recibido = models.DateTimeField(auto_now_add=True)  # Fecha de recepción, se guarda automáticamente

    def __str__(self):
        return f"{self.asunto} - {self.remitente}"

# Modelo Phishing_Reporte actualizado
class PhishingReporte(models.Model):
    correo = models.ForeignKey(CorreoElectronico, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    es_phishing = models.BooleanField(default=False)  # Campo para validar si es phishing el correo electronico

    def __str__(self):
        return f"Reporte - Usuario: {self.usuario.nombre}, Descripcion: {self.descripcion}"

# Modelo Configuracion_Seguridad
class ConfiguracionSeguridad(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nivel_seguridad = models.CharField(max_length=5, choices=[('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')])
    notificacion = models.BooleanField()

    def __str__(self):
        return f"Configuración de {self.usuario.nombre}"