import pickle

# Cargar el modelo y el vectorizador
with open('models/modelo_spam.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('models/vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Función para predecir si un correo es spam o no
def predecir_spam(correo_texto):
    correo_transformado = vectorizer.transform([correo_texto])
    prediccion = model.predict(correo_transformado)
    return "Malicioso" if prediccion[0] == 1 else "Legítimo"
