import numpy as np
import pandas as pd

# Función para la media
def media(numbers: list) -> float:
    return round(sum(numbers) / len(numbers), 2)


# Función para la mediana
def mediana(numbers: list) -> float:
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
def percentil(numbers: list, percent: float) -> float:
    n = len(numbers)

    # Ordenando lista
    sorted_numbers = sorted(numbers)
    
    # Calculando posición
    k = (n - 1) * (percent)
    f = int(k)      
    c = k - f

    # Calculando percentil
    if f + 1 < n:   
        return round(sorted_numbers[f] + c * (sorted_numbers[f + 1] - sorted_numbers[f]), 2)
    else:
        return round(sorted_numbers[f], 2)


# Función para rango intercuartílico
def IQR(numbers: list) -> float:

    # Calculando cuartiles 1 y 3
    q1 = percentil(numbers, 0.25)
    q3 = percentil(numbers, 0.75)

    return q3 - q1


# Función para varianza
def varianza(numbers: list) -> float:

    # Calculando media
    mean = media(numbers)

    return round(sum((x - mean) ** 2 for x in numbers) / len(numbers), 2)


# Función para std
def desviacion_tipica(numbers: list) -> float:
    return round(varianza(numbers) ** 0.5, 2)


# Imprimir resultados
def prints(data: dict) -> None:
    for k, v in data.items():
        print(f"------------ {k} ------------")
        print("Media: ", media(v))
        print("Mediana: ", mediana(v))
        print("Moda: ", moda(v))
        print("Percentil 25: ", percentil(v, 0.25))
        print("Percentil 75: ", percentil(v, 0.75))
        print("IQR: ", IQR(v))
        print("Varianza: ", varianza(v))
        print("Desviación típica: ", desviacion_tipica(v))
        print("\n")


if __name__ == "__main__":

    np.random.seed(42) 
    edad =  np.random.randint(20, 60, 100),     
    salario =  np.random.normal(45000, 15000, 100),     
    experiencia = np.random.randint(0, 30, 100)
    
    # Definiendo datos
    np.random.seed(42)
    df = pd.DataFrame({     
        'edad': np.random.randint(20, 60, 100),     
        'salario': np.random.normal(45000, 15000, 100),     
        'experiencia': np.random.randint(0, 30, 100) })
    
    # Imprimiendo estadísticos
    prints(df)

    

    
    