import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phishing_protection.settings')  # Reemplaza con tu configuración
django.setup()

# Importar funciones de utils.py
from seguridad.utils import obtener_datos_entrenamiento, preprocesar_datos, entrenar_modelo, guardar_modelo_y_vectorizador

# Flujo de entrenamiento
def main():
    print("Obteniendo datos de entrenamiento desde la base de datos...")
    df = obtener_datos_entrenamiento()

    print("Preprocesando los datos...")
    X, y, vectorizer = preprocesar_datos(df)

    print("Entrenando el modelo...")
    modelo = entrenar_modelo(X, y)

    print("Guardando el modelo y el vectorizador...")
    guardar_modelo_y_vectorizador(modelo, vectorizer)

    print("¡Entrenamiento y guardado completados con éxito!")

if __name__ == "__main__":
    main()
