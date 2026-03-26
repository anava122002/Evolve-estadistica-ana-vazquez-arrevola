import numpy as np
import pandas as pd

# Función para la media
def media(numbers: list) -> float:

    """Calcula la media de los elementos de una lista."""

    return round(sum(numbers) / len(numbers), 2)


# Función para la mediana
def mediana(numbers: list) -> float:

    """Calcula la mediana de los elementos de una lista."""

    n = len(numbers)

    # Ordenando lista
    sorted_numbers = sorted(numbers)

    # Caluclando mediana según longitud de lista
    if n % 2 == 0:
        return round((sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2, 2)
    else:
        return round(sorted_numbers[n // 2], 2)
    

# Función para la moda
def moda(numbers: list) -> float:

    """Calucla la moda de los elementos de una lista."""

    counts = {}

    # Contando el total de apariciones de cada elemento
    for number in numbers:

        # Revisando que no se haya contado antes
        if number not in counts.keys():
            counts[number] = 0

            # Contandor
            for number2 in numbers:
                if number == number2:
                    counts[number] += 1

    return round(max(counts, key = counts.get), 2)


# Función para los percentiles
def percentil(numbers: list, pct: float) -> float:

    """Calcula el percentil correspondiente al porcentaje dado."""

    n = len(numbers)

    # Ordenando lista
    sorted_numbers = sorted(numbers)
    
    # Calculando posición
    k = round((n - 1) * (pct))

    return sorted_numbers[int(k) - 1]


# Función para rango intercuartílico
def IQR(numbers: list) -> float:

    """Calcula el rango intercuartílico (Q3 - Q1)."""

    # Calculando cuartiles 1 y 3
    q1 = percentil(numbers, 0.25)
    q3 = percentil(numbers, 0.75)

    return q3 - q1


# Función para varianza
def varianza(numbers: list) -> float:

    """Calcula la variabilidad de los elementos de una lista."""

    # Calculando media
    mu = media(numbers)

    return round(sum((x - mu) ** 2 for x in numbers) / len(numbers), 2)


# Función para std
def desviacion_tipica(numbers: list) -> float:

    """Calcula la desviación típica de los elementos de una lista
    a partir de su varianza."""

    return round(varianza(numbers) ** 0.5, 2)


# Función para CV
def cv(numbers: list) -> float:

    """Calcula el coeficiente de variación de los elementos de una lista."""

    # Calculando media
    mu = media(numbers)

    # Calculando desviación típica
    s = desviacion_tipica(numbers)

    return (s/mu) * 100


# Función para calcular asimetría
def skewness(numbers: list):

    """Calcula el coeficiente de asimetría de la distribución 
    correspondiente a los elementos de una lista."""

    n = len(numbers)

    # Caluclando media y std
    mu = media(numbers)
    s = desviacion_tipica(numbers)

    return sum((x - mu) ** 3 for x in numbers) / ((n - 1) * s ** 3)


# Función para calcular curtosis
def kurtosis(numbers:list):

    """ Calcula la curtosis de la distribución correspondiente
    a los elemetos de una lista."""

    n = len(numbers)

    # Caluclando media y std
    mu = media(numbers)
    s = desviacion_tipica(numbers)

    return (sum((x - mu) ** 4 for x in numbers) / (s ** 4)) / n - 3


# Imprimir resultados
def medidas_centralidad(numbers: list):
    print(f"---> Medidas de centralidad:")
    print("Media: ", media(numbers))
    print("Mediana: ", mediana(numbers))
    print("Moda: ", moda(numbers))
    print("Percentil 25: ", percentil(numbers, 0.25))
    print("Percentil 75: ", percentil(numbers, 0.75))
    print("IQR: ", IQR(numbers))

def medidas_dispersión(numbers: list):
    print(f"---> Medidas de dispersión:")
    print("Varianza: ", varianza(numbers))
    print("Desviación típica: ", desviacion_tipica(numbers))
    print("Coeficiente de variación: ", cv(numbers))

def otras_medidas(numbers: list):
    print(f"---> Otras medidas:")
    print("Skewness (simetría): ", skewness(numbers))
    print("Curtosis (concentración): ", kurtosis(numbers))


def prints(data: dict):
    for k, v in data.items():
        print(f"------------ {k.upper()} ------------")
        medidas_centralidad(v)
        medidas_dispersión(v)
        otras_medidas(v)
        print("\n")


if __name__ == "__main__":

    # Definiendo datos
    np.random.seed(42)
    df = pd.DataFrame({     
        'edad': np.random.randint(20, 60, 100),     
        'salario': np.random.normal(45000, 15000, 100),     
        'experiencia': np.random.randint(0, 30, 100) })
    
    # Imprimiendo estadísticos
    prints(df)

    # Comprobación con .describe()
    # print(df.describe())

    

    
    