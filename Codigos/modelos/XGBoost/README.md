# Predicción del Precio de la Luz con XGBoost

## 📔 Descripción del Proyecto

Este cuaderno de Jupyter implementa un modelo ***XGBoost*** (eXtreme Gradient Boosting). Este es un algoritmo de machine learning basado en árboles de decisión optimizado para velocidad y rendimiento. Este modelo tiene como características principales:

- **Modelado No Lineal:** Permite modelar interacciones complejas y patrones no lineales en los datos.

- **Importancia de Variables:** Proporciona métricas para evaluar la relevancia de cada predictor.

- **Regularización:** Incorpora técnicas para evitar el sobreajuste y mejorar la generalización.

El proceso consiste en:

- **Obtención de Variables Temporales:** Como XGBoost no modela explícitamente la temporalidad, es fundamental construir características que representen la dinámica de la serie, tales como rezagos (lags), medias móviles o variables estacionales (día de la semana, hora del día).

- **Búsqueda de Hiperparámetros (GridSearch):** Se implementa una búsqueda sistemática (GridSearchCV) para encontrar la mejor combinación de parámetros como número de árboles, profundidad máxima, tasa de aprendizaje, y regularización.

- **Validación Cruzada Temporal (TimeSeriesSplit)**: Se usa TimeSeriesSplit para respetar el orden cronológico de los datos, asegurando que el modelo se valide con datos posteriores a los que usó para entrenar.

- **Ajuste del Modelo:** Con los hiperparámetros óptimos, se entrena el modelo final sobre el conjunto de entrenamiento.

La predicción con XGBoost se realiza de forma recursiva:

- **Reentrenamiento:** Se reentrena el modelo final con todos los datos históricos disponibles para aprovechar toda la información.

- **Predicción Paso a Paso:** Para predecir el horizonte futuro el modelo:

    - Predice el primer paso (t+1) usando los datos históricos reales y las variables derivadas.

    - Para predecir el segundo paso (t+2), utiliza los datos históricos y la predicción previa para t+1 como si fuera un dato real, actualizando las variables temporales en cada paso.

Este método permite a XGBoost adaptarse a la predicción de series temporales, siempre que las características temporales estén bien diseñadas.

## 🎯 Objetivo

- Predecir el precio horario de la electricidad para un conjunto de tiempo deseado, en este caso a un mes vista.

## 📁 Estructura del Script

1. **Carga de datos** ``CSV`` desde rutas locales.
2. **Preprocesamiento**:
   - Conversión temporal
   - Alineación por hora
   - Eliminación de valores nulos
3. **Creación de características**:
   - Lags (t-1, t-24, t-168)
   - Estadísticas móviles (media y desviación)
   - Variables temporales (hora, día de la semana, mes)
4. **División del dataset**:
   - Entrenamiento, validación y predicción final
5. **Análisis Exploratorio**:
   - Gráficos temporales
   - Boxplots por hora y mes
   - Matriz de correlación
6. **Entrenamiento del modelo**:
   - Ajuste directo o mediante ``GridSearchCV``
7. **Evaluación del rendimiento**:
   - ``MAE`` y ``RMSE``
   - Importancia de variables
   - Visualización comparativa real vs. predicción
8. **Predicción final y visualización** para un periodo objetivo
9. **Análisis de errores**:
   - Distribución
   - Q-Q plots
   - Boxplots
   - Normalidad de residuos

---

## 📊 Variables Consideradas

- `precio`: variable objetivo
- `generacion_eolica`: variable exógena (lag 24h)
- `generacion_solar`: variable exógena (lag 24h)
- `demanda_real`: variable exógena (lag 24h)
- `lag_1`, `lag_24`, `lag_168`: precios pasados
- `rolling_mean_24`, `rolling_std_24`: media y desviación móviles
- `hora`, `dia_semana`, `mes`: variables temporales


## 📦 Requisitos

Los paquetes utilizados se incluyen en el requirements (py 3.10):

``pip install -r requirements.txt``

## ✅ Resultados

### Modelo 2.1

   - df['lag_1'] = df['precio'].shift(1)
   - df['lag_24'] = df['precio'].shift(24)
   - df['lag_168'] = df['precio'].shift(168)
   - df['rolling_mean_24'] = df['precio'].rolling(24).mean()
   - df['rolling_std_24'] = df['precio'].rolling(24).std()

**Train-Test set:** 70/30

---

**Hiperparámetros óptimos encontrados:**
- learning_rate': 0.04
- 'max_depth': 3
- 'n_estimators': 375
- Mejor MAE con validación cruzada: 6.00
---
Evaluación sobre el modelo:

| Métrica | Test | Predicción | 
|---|---|---|
| **MAE** | 7.2982 | 7.4319 |
| **RMSE** | 11.0834 | 12.2298 |
| **R²** | 0.9548 | 0.9434 |
---
### Modelo 2.2

- df['lag_1'] = df['precio'].shift(1)
- df['lag_24'] = df['precio'].shift(24)
- df['lag_168'] = df['precio'].shift(168)
- df['rolling_mean_24'] = df['precio'].rolling(24).mean()
- df['rolling_std_24'] = df['precio'].rolling(24).std()


**Train-Test set:** 90/10

---

**Hiperparámetros óptimos encontrados:**
- learning_rate': 0.04
- 'max_depth': 3
- 'n_estimators': 375
- Mejor MAE con validación cruzada: 6.00
---
Evaluación sobre el modelo:

| Métrica | Test | Predicción | 
|---|---|---|
| **MAE** | 6.3381 | 6.7529 |
| **RMSE** | 10.7758 | 11.1385 |
| **R²** | 0.9164 | 0.9530 |
---
### Modelo 2.3

   - df['lag_1'] = df['precio'].shift(1)
   - df['lag_24'] = df['precio'].shift(24)
   - df['lag_168'] = df['precio'].shift(168)
   - df['rolling_mean_24'] = df['precio'].rolling(24).mean()
   - df['rolling_std_24'] = df['precio'].rolling(24).std()
   - df['rolling_mean_24_eolica'] = df['generacion_eolica'].rolling(24).mean()
   - df['rolling_std_24_eolica'] = df['generacion_eolica'].rolling(24).std()
   - df['rolling_mean_24_solar'] = df['generacion_solar'].rolling(24).mean()
   - df['rolling_std_24_solar'] = df['generacion_solar'].rolling(24).std()
   - df['rolling_mean_24_demanda'] = df['demanda_real'].rolling(24).mean()
   - df['rolling_std_24_demanda'] = df['demanda_real'].rolling(24).std()

**Train-Test set:** 90/10

---

**Hiperparámetros óptimos encontrados:**
- learning_rate': 0.03
- 'max_depth': 3
- 'n_estimators': 300
- Mejor MAE con validación cruzada: 6.11


---
Evaluación sobre el modelo:

| Métrica | Test | Predicción | 
|---|---|---|
| **MAE** | 7.6670 | 7.7443 |
| **RMSE** | 11.5923 | 12.9418 |
| **R²** | 0.9505 | 0.9366 |
---
### Modelo 2.3

   - df['lag_1'] = df['precio'].shift(1)
   - df['lag_24'] = df['precio'].shift(24)
   - df['lag_168'] = df['precio'].shift(168)
   - df['rolling_mean_24'] = df['precio'].rolling(24).mean()
   - df['rolling_std_24'] = df['precio'].rolling(24).std()
   - df['rolling_mean_24_eolica'] = df['generacion_eolica'].rolling(24).mean()
   - df['rolling_std_24_eolica'] = df['generacion_eolica'].rolling(24).std()
   - df['rolling_mean_24_solar'] = df['generacion_solar'].rolling(24).mean()
   - df['rolling_std_24_solar'] = df['generacion_solar'].rolling(24).std()
   - df['rolling_mean_24_demanda'] = df['demanda_real'].rolling(24).mean()
   - df['rolling_std_24_demanda'] = df['demanda_real'].rolling(24).std()

**Train-Test set:** 90/10

---
**Hiperparámetros óptimos encontrados:**
- learning_rate': 0.03
- 'max_depth': 3
- 'n_estimators': 300
- Mejor MAE con validación cruzada: 6.11

---

Evaluación sobre el modelo:

| Métrica | Test | Predicción | 
|---|---|---|
| **MAE** | 6.2932 | 7.4174 |
| **RMSE** | 9.4810 | 12.0819 |
| **R²** | 0.8947 | 0.9447 |
---