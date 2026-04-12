# Respuestas — Práctica Final: Análisis y Modelado de Datos

> Rellena cada pregunta con tu respuesta. Cuando se pida un valor numérico, incluye también una breve explicación de lo que significa.

---

## Ejercicio 1 — Análisis Estadístico Descriptivo
---
Añade aqui tu descripción y analisis:

---

**Pregunta 1.1** — ¿De qué fuente proviene el dataset y cuál es la variable objetivo (target)? ¿Por qué tiene sentido hacer regresión sobre ella?

Los datos son parte del National Library of Medicine, concretamente del [**Dataset on anthropometric measurements of the adult population in Slovakia**](https://pmc.ncbi.nlm.nih.gov/articles/PMC11214164/).

Ya tomé este dataset con anterioridad para estudiar estadísticamente la veracidad de las proporciones del hombre de Vitruvio con datos antropométricos reales. En este contexto tiene sentido, tomando la altura como variable objetivo, hacer una regresión lineal usando como variables independientes la envergadura o la longitud de las piernas, torso y cabeza para determinar su proporción en la altura total del cuerpo (los coeficientes *b_i* deberían ser las proporciones dadas por Vitruvio y Da Vinci, forzando *b_0* = 0, si es que interpretamos dichas proporciones como ecuaciones de la recta).

Tendría más sentido tomar el peso como variable objetivo y determinarlo según la altura, género... pero se necesitarían otras tantas variables que son determinantes pero no tienen que ver con la antropometría y por tanto faltan en el dataset.

**Pregunta 1.2** — ¿Qué distribución tienen las principales variables numéricas y has encontrado outliers? Indica en qué variables y qué has decidido hacer con ellos.

Las variables numéricas siguen todas una distribución normal excepto la edad pues los datos recogidos son mayoritariamente de jóvenes entre 18 y 25 años (en el link anterior se especifica que los datos se centran en estudiantes, así que era esperable). Los outliers eran principalmente valores irreales, probablemente mal introducidos, de modo que ajustando el coeficiente del método IQR de 1.5 a 2 son fácilmente aislables. 

Un buen ejemplo son los outliers de la variable 'height'. Tomando el método IQR con un coeficiente igual a 1.5 resultaban los outliers 18cm, 1975cm y 205cm. Cambiando el coeficiente a 2 quedaron solo 18cm y 1975cm.

Puesto que eran pocos se consideró sustituirlos por las medias de altura en base a la envergadura (variable *arms_reach*) o eliminarlos. Como se tienen suficientes datos para la regresión y para evitar crear sesgos, finalmente se eliminaron.

**Pregunta 1.3** — ¿Qué tres variables numéricas tienen mayor correlación (en valor absoluto) con la variable objetivo? Indica los coeficientes.

Las variables con mayor correlación con *height* son *shoulder_height*, *arms_reach* y *gender* con coeficientes de correlación iguales a 0.91, 0.84 y -0.73 respectivamente. 

El hecho de que el coeficiente de correlación entre *height* y *shoulder_height* sea tan alto es simple: la altura de los hombros constituye una fracción importante de la altura total (más de 3/4 de la altura total según Vitruvio). Para *height* y *arms_reach* es similar. En relación a la variable *gender*, en el análisis descriptivo se observa que los hombres son de media entre 10 y 15cm más altos que las mujeres, por lo que el género determina notablemente la altura del individuo.

**Pregunta 1.4** — ¿Hay valores nulos en el dataset? ¿Qué porcentaje representan y cómo los has tratado?

La mayoría de columnas del dataset tienen más del 50% de sus datos nulos. Puesto que interpolar tantos datos podría crear sesgos en los resultados y aún eliminando estas filas se siguen conservando casi 5000 elementos en la muestra (suficientes para la regresión), se ha decidido eliminarlos. 

---

## Ejercicio 2 — Inferencia con Scikit-Learn

---
Puesto que es difícil evitar la multicolinealidad en datos antropométricos, en este caso se hará una regresión sobre las variables *gender*, *weight*, *arms_reach*, pues no están tan directamente relacionadas (independientemente de su coeficiente de correlación) con la variable objetivo *height* como, por ejemplo, *shoulder_height* o *leg_length*. 

Para empezar, se binariza la variable *gender* y se toman solo las columnas del dataset que van a ser usadas, dividiéndolas en dos grupos para entrenar y testear. La recta de regresión resultante tiene la siguiente forma: 

        y = 89.806 - 4.61373969 * X_{gender} + 0.12753115 * X_{weight} + 0.45162687 * X_{arms_reach}

* La variable *gender* es la que tiene mayor peso en la regresión. Concretamente, el modelo estima que las mujeres (1) miden de media 4.6cm menos que los hombres (0). Es un resultado biológicamente coherente.

* La variable *weight* parece no ser especialmente determinante. La altura aumenta 0.13cm por kg lo que, aunque indique una relación débil, también tiene sentido biológico.

* La variable *arms_reach*, correspondiente a la envergadura, es ligeramente más influyente que el peso pero tampoco demasiado. El modelo estima que la altura aumenta 0.45cm por cada cm de envergadura. Una persona alta tiene los brazos más largos de media que una persona baja, por lo que tiene sentido.

* El intercepto indica que, si el resto de variables son cero, la persona seguirá midiendo aprox. 90cm. En este contexto no tiene mucho valor.

El coeficiente de determinación es 0.774, de modo que el modelo explica el 77.4% de la variación de la altura, lo cual indica un buen ajuste. Si lo comparamos con el resultante para los valores del test (0.73), vemos que el modelo generaliza bien y no hay overfitting.

Pasando a los errores, vemos que el MAE es de 3.356cm y el RMSE de 4.387cm. Son relativamente grande teniendo en cuenta que estamos tratando de predecir datos antropométricos, pero no excesivos. Que se diferencien en poco más de 1cm indica que no hay errores muy grandes que estén inflando el RMSE (el modelo comete errores homogéneos).

Finalmente, la gráfica de residuos muestra una nube de puntos sin patrón aparente lo que significa que siguen una distribución normal, condición necesaria para validar el modelo. A modo de confirmación se ha graficado también el Q-Q plot con resultados similares:

<figure>
  <img src="data/otros/qq_plot.png" width="400" height="300" alt="Descripción de la imagen">
</figure>

---

**Pregunta 2.1** — Indica los valores de MAE, RMSE y R² de la regresión lineal sobre el test set. ¿El modelo funciona bien? ¿Por qué?

* MAE: 3.356
* RMSE: 4.387
* R²: 0.774

El modelo funciona razonablemente bien. El coeficiente de determinación es lo suficientemente alto (> 0.7) como para asumir que la regresión tiene un buen ajuste. Además, que el error absoluto y cuadrático solo se diferencien en 1cm es indicativo de que no hay outliers con una gran penalización por parte del RMSE. Otro indicativo de esto mismo es la normalidad de los residuos.

Aún así, al tratarse de datos antropométricos, un error de entre 3 y 4cm se puede considerar alto y puede crear una dispersión notoria en los resultados. Esto se ve en la siguiente imagen:

<figure>
  <img src="data/otros/dispersion_regresion.png" width="400" height="300" alt="Descripción de la imagen">
</figure>

---

## Ejercicio 3 — Regresión Lineal Múltiple en NumPy

---
Añade aqui tu descripción y analisis:

---

**Pregunta 3.1** — Explica en tus propias palabras qué hace la fórmula β = (XᵀX)⁻¹ Xᵀy y por qué es necesario añadir una columna de unos a la matriz X.

> _Escribe aquí tu respuesta_

**Pregunta 3.2** — Copia aquí los cuatro coeficientes ajustados por tu función y compáralos con los valores de referencia del enunciado.

| Parametro | Valor real | Valor ajustado |
|-----------|-----------|----------------|
| β₀        | 5.0       |                |
| β₁        | 2.0       |                |
| β₂        | -1.0      |                |
| β₃        | 0.5       |                |

> _Escribe aquí tu respuesta_

**Pregunta 3.3** — ¿Qué valores de MAE, RMSE y R² has obtenido? ¿Se aproximan a los de referencia?

> _Escribe aquí tu respuesta_

**Pregunta 3.4* — Compara los resultados con la reacción logística anterior para tu dataset y comprueba si el resultado es parecido. Explica qué ha sucedido. 

> _Escribe aquí tu respuesta_

---

## Ejercicio 4 — Series Temporales
---
Añade aqui tu descripción y analisis:

---

**Pregunta 4.1** — ¿La serie presenta tendencia? Descríbela brevemente (tipo, dirección, magnitud aproximada).

> _Escribe aquí tu respuesta_

**Pregunta 4.2** — ¿Hay estacionalidad? Indica el periodo aproximado en días y la amplitud del patrón estacional.

> _Escribe aquí tu respuesta_

**Pregunta 4.3** — ¿Se aprecian ciclos de largo plazo en la serie? ¿Cómo los diferencias de la tendencia?

> _Escribe aquí tu respuesta_

**Pregunta 4.4** — ¿El residuo se ajusta a un ruido ideal? Indica la media, la desviación típica y el resultado del test de normalidad (p-value) para justificar tu respuesta.

> _Escribe aquí tu respuesta_

---

*Fin del documento de respuestas*
