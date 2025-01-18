import joblib

# Cargar el modelo y el vectorizador
modelo = joblib.load('seguridad/models/modelo_spam.pkl')
vectorizador = joblib.load('seguridad/models/vectorizer.pkl')

# Probar el modelo con ejemplos controlados
correos_prueba = [
    "Este es un correo de prueba para ganar dinero fácil.",
    "¡Gran oferta! Compra ahora y ahorra dinero..."
]

for correo in correos_prueba:
    correo_vectorizado = vectorizador.transform([correo])
    prediccion = modelo.predict(correo_vectorizado)[0]
    print(f"Correo: {correo}")
    print(f"Predicción: {'Malicioso' if prediccion == 1 else 'Legítimo'}")
