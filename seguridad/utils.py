import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pickle,re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import os

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('spanish'))


# Función para obtener datos de entrenamiento desde el archivo CSV
def obtener_datos_entrenamiento():
    # Ruta del archivo CSV
    csv_file_path = os.path.join('data', 'correos.csv')

    # Revisar el archivo manualmente para detectar caracteres no visibles
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            print("Contenido del archivo CSV:")
            print(file.read())  # Muestra el contenido del archivo para depuración
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo CSV en la ruta: {csv_file_path}")

    # Leer el archivo CSV en un DataFrame
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo CSV en la ruta: {csv_file_path}")

    print(f"Número de filas cargadas: {len(df)}")  # Depuración: número de filas cargadas

    # Asegúrate de que la columna 'etiqueta' exista y realiza la transformación
    if 'etiqueta' not in df.columns:
        raise ValueError("La columna 'etiqueta' no existe en los datos obtenidos.")

    # Transformación de la columna 'etiqueta' para que sea binaria (0 o 1)
    df['etiqueta'] = df['etiqueta'].apply(lambda x: 1 if x == 'malicioso' else 0)

    # Depuración: Mostrar las primeras filas del DataFrame
    print(df.head())  # Muestra las primeras filas para verificar

    # Verificar la configuración de pandas sobre el número de filas

    print(f"Max rows pandas display: {pd.options.display.max_rows}")

    # Si es necesario, ajusta el límite de filas mostrado
    pd.options.display.max_rows = 1000  # Ajusta a un número mayor según tus necesidades

    return df

# Preprocesar los datos (Vectorización)
def preprocesar_datos(df):
    """
    Preprocesa los datos para entrenar el modelo.
    Convierte el contenido a minúsculas, elimina caracteres especiales y aplica el vectorizador.
    """
    # Asegúrate de que la columna 'contenido' exista
    if 'contenido' not in df.columns:
        raise ValueError("La columna 'contenido' no existe en el DataFrame.")

    # Limpia y preprocesa cada fila de la columna 'contenido'
    df['contenido'] = df['contenido'].apply(lambda x: limpiar_texto(x))

    # Asegúrate de que la columna 'etiqueta' sea numérica (0 = legítimo, 1 = malicioso)
    if 'etiqueta' not in df.columns:
        raise ValueError("La columna 'etiqueta' no existe en el DataFrame.")

    df['etiqueta'] = df['etiqueta'].apply(lambda x: 1 if x == 'malicioso' else 0)

    # Divide los datos en características (X) y etiquetas (y)
    X = df['contenido']
    y = df['etiqueta']

    # Vectorizar el texto
    vectorizer = CountVectorizer(ngram_range=(1, 2), max_features=5000)
    X_vectorized = vectorizer.fit_transform(X)

    return X_vectorized, y, vectorizer

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúñü\s]', '', texto)  # Eliminar caracteres no deseados
    palabras = texto.split()
    palabras = [lemmatizer.lemmatize(palabra) for palabra in palabras if palabra not in stop_words]
    return ' '.join(palabras)

# Entrenar el modelo
def entrenar_modelo(X, y):
    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear el clasificador (usando Árbol de Decisión)
    model = DecisionTreeClassifier()

    # Entrenar y evaluar
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Evaluar el modelo en los datos de prueba
    accuracy = model.score(X_test, y_test)
    print(f'Precisión del modelo: {accuracy * 100:.2f}%')

    return model

# Guardar el modelo y el vectorizador
def guardar_modelo_y_vectorizador(model, vectorizer):
    # Guardar el modelo entrenado
    with open('seguridad/models/modelo_spam.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)

    # Guardar el vectorizador
    with open('seguridad/models/vectorizer.pkl', 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)

