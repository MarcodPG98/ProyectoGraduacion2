import os

import pandas as pd
from seguridad.utils import preprocesar_datos, entrenar_modelo, guardar_modelo_y_vectorizador, \
    obtener_datos_entrenamiento


def main():

    # Cargar los datos desde el archivo CSV
    print("Cargando datos desde el archivo CSV...")
    df = obtener_datos_entrenamiento()

    # Mostrar una vista previa de los datos cargados
    print(df.head())

    # Preprocesar los datos
    print("Preprocesando datos...")
    X, y, vectorizer = preprocesar_datos(df)

    # Entrenar el modelo
    print("Entrenando el modelo...")
    modelo = entrenar_modelo(X, y)

    # Guardar el modelo y el vectorizador
    print("Guardando el modelo y el vectorizador...")
    guardar_modelo_y_vectorizador(modelo, vectorizer)

    print("Entrenamiento completado y modelo guardado con éxito.")

if __name__ == '__main__':
    main()