from .models import CorreoElectrico
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pickle

def obtener_datos_entrenamiento():
    from .models import CorreoElectrico
    import pandas as pd

    # Obtén los datos desde la base de datos
    correos = CorreoElectrico.objects.all().values('contenido', 'etiqueta')
    df = pd.DataFrame(correos)

    # Imprime el contenido del DataFrame para depuración
    print("Contenido del DataFrame:")
    print(df.head())  # Muestra las primeras filas del DataFrame

    # Asegúrate de que la columna 'etiqueta' exista y realiza la transformación
    if 'etiqueta' not in df.columns:
        raise ValueError("La columna 'etiqueta' no existe en los datos obtenidos.")
    df['etiqueta'] = df['etiqueta'].apply(lambda x: 1 if x == 'malicioso' else 0)

    return df


# Preprocesar los datos (Vectorización)
def preprocesar_datos(df):
    # Inicializar el vectorizador TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')

    # Ajustamos el vectorizador a los datos
    X = vectorizer.fit_transform(df['contenido'])

    # Etiquetas (si el correo es legítimo o malicioso)
    y = df['etiqueta']

    return X, y, vectorizer


# Entrenar el modelo
def entrenar_modelo(X, y):
    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear el clasificador (usando Árbol de Decisión)
    model = DecisionTreeClassifier()

    # Entrenar el modelo
    model.fit(X_train, y_train)

    # Evaluar el modelo en los datos de prueba
    accuracy = model.score(X_test, y_test)
    print(f'Precisión del modelo: {accuracy * 100:.2f}%')

    return model

# Guardar el modelo y el vectorizador
def guardar_modelo_y_vectorizador(model, vectorizer):
    # Guardar el modelo entrenado
    with open('models/modelo_spam.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)

    # Guardar el vectorizador
    with open('models/vectorizer.pkl', 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)