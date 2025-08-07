# Predicción del Precio de la Luz con SARIMAX + GARCH

## 📔 Descripción del Proyecto

Este cuaderno de Jupyter implementa un modelo ***SARIMAX*** (Seasonal AutoRegressive Integrated Moving Average with eXogenous variables). Este es un modelo estadístico clásico para la predicción de series temporales. Sus punto fuerte es la capacidad para modelar explícitamente tres componentes clave de la serie:

- **Tendencia** (I - Integrado): Se logra a través de la diferenciación para hacer que la serie sea estacionaria.

- **Estacionalidad** (S - Seasonal): Captura patrones que se repiten en intervalos fijos (por ejemplo, diarios o semanales).

- **Variables Exógenas** (X): Permite incluir variables externas que puedan influir en la objetivo, en este caso, como la demanda o la generación de cierto tipos de energía.

El proceso consiste en:

- **Identificación del Orden:** Se analizan las funciones de Autocorrelación (ACF) y Autocorrelación Parcial (PACF) de la serie de precios para determinar los órdenes (p,d,q) para la parte no estacional y (P,D,Q,s) para la parte estacional.

- **Estimación del Modelo**: Una vez definidos los órdenes, se ajusta el modelo al conjunto de datos de entrenamiento. El modelo aprende los coeficientes que ponderan la importancia de los valores pasados, los errores de pronóstico pasados y las variables exógenas.

La predicción con SARIMAX es un proceso iterativo:

- **Reentrenamiento:** Al igual que con otros modelos, se reentrena un modelo SARIMAX final con su orden óptimo utilizando todos los datos históricos disponibles para maximizar la información aprendida.

- **Predicción Paso a Paso**: Para predecir el horizonte futuro el modelo:

    - Estima el primer paso (t+1) utilizando todos los datos históricos reales.

    - Para predecir el segundo paso (t+2), utiliza los datos históricos y la predicción que acaba de hacer para t+1 como si fuera un dato real.

Este proceso se repite para cada punto en el horizonte de predicción.

Adicionalmente se utiliza la libreria ``arch``, donde se estima la incertidumbre en la predicción a partir de los residuos de la ``SARIMAX``, con el modelo ``GARCH``

## 🎯 Objetivo

- Predecir el precio horario de la electricidad para un conjunto de tiempo deseado, en este caso a un mes vista.

## 📁 Estructura General del Script

1. **Carga de datos** ``CSV`` desde rutas locales.
2. **Preprocesamiento y limpieza** de los datos.
3. **Análisis exploratorio**:
   - Gráficos de tendencias
   - Boxplots por hora/mes
   - Matriz de correlación
   - ``ACF/PACF``
4. **Evaluación de estacionariedad y elección de parámetros**
    - Diferenciaciones de la serie temporal.
    - Análisis de ``ACF/PACF``
    - Test de estacionariedad (``ADF y KPSS``).
5. **Modelado con SARIMAX**:
   - Entrenamiento y evaluación en conjunto de test
6. **Predicción final** para el conjunto elegido.
7. **Modelado de volatilidad** con ``GARCH(1,1)``.
8. **Visualización de errores** y métricas de rendimiento.

---

## 📦 Requisitos

Los paquetes necesarios se encuentran en el requirements.txt. (py 3.11) Para instalarlos:
`pip install -r requirements.txt`

## ✅ Resultados

### Modelo 1.1: Parámetros (2,1,1)(1,1,1,24)

- **Variables Endógenas**: Precio
- **Variables Exógenas temporales**: Hora, día de la semana, mes del año
- **Variables Exógenas adicionales (desfasadas 24 horas hacia atrás)**: Demanda real, generación eólica y solar, lag24 y lag168 (precio de la luz 24 y 168 horas antes), la media del dia anterior y la desviacion tipica para todas las varaibles (luz, generaciones y demanda).


| Métrica | Test | Predicción | 
|---|---|---|
| **MAE** | 46.72 | 55.36 |
| **RMSE** | 60.92 | 67.43 |
| **R²** | -4.79 | -1.10 |
---|


### Modelo 1.2: Parámetros (1,1,1)(1,1,1,24)

- **Variables Endógenas**: Precio
- **Variables Exógenas temporales**: Hora, día de la semana, mes del año
- **Variables Exógenas adicionales (desfasadas 24 horas hacia atrás)**: Demanda real, generación eólica y solar, lag24 y lag168 (precio de la luz 24 y 168 horas antes), la media del dia anterior y la desviacion tipica para todas las varaibles (luz, generaciones y demanda).


| Métrica | Test | Predicción | 
|---|---|---|
| **MAE** | 46.72 | 55.36 |
| **RMSE** | 60.92 | 67.43 |
| **R²** | -4.79 | -1.10 |
---|


### Modelo 1.3: Parámetros (2,1,0)(1,1,0,24)

- **Variables Endógenas**: Precio
- **Variables Exógenas temporales**: Hora, día de la semana, mes del año
- **Variables Exógenas adicionales (desfasadas 24 horas hacia atrás)**: Demanda real, generación eólica y solar, lag24 y lag168 (precio de la luz 24 y 168 horas antes), la media del dia anterior y la desviacion tipica para todas las varaibles (luz, generaciones y demanda).


| Métrica | Test | Predicción | 
|---|---|---|
| **MAE** | 6.2932 | 7.4174 |
| **RMSE** | 9.4810 | 12.0819 |
| **R²** | 0.8947 | 0.9447 |
---|