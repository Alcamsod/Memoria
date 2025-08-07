# Resumen de Resultados de Modelos de Predicción

Exponemos a continuación los resultados obtenidos para los distintos modelos utilizados y sus configuraciones

---

## 1. SARIMAX

malos, faltan de revisar pero no merece la pena invertir mucho más tiempo en ellos

### Modelo 1.1: Parámetros (2,1,1)(1,1,1,24)

- **Variables Endógenas**: Precio
- **Variables Exógenas temporales**: Hora, día de la semana, mes del año
- **Variables Exógenas adicionales (desfasadas 24 horas hacia atrás)**: Demanda real, generación eólica y solar, lag24 y lag168 (precio de la luz 24 y 168 horas antes), la media del dia anterior y la desviacion tipica para todas las varaibles (luz, generaciones y demanda).

| Métrica  | Test  | Predicción |
| -------- | ----- | ---------- |
| **MAE**  | 46.72 | 55.36      |
| **RMSE** | 60.92 | 67.43      |
| **R²**   | -4.79 | -1.10      |
| ---      |

### Modelo 1.2: Parámetros (1,1,1)(1,1,1,24)

- **Variables Endógenas**: Precio
- **Variables Exógenas temporales**: Hora, día de la semana, mes del año
- **Variables Exógenas adicionales (desfasadas 24 horas hacia atrás)**: Demanda real, generación eólica y solar, lag24 y lag168 (precio de la luz 24 y 168 horas antes), la media del dia anterior y la desviacion tipica para todas las varaibles (luz, generaciones y demanda).

| Métrica  | Test  | Predicción |
| -------- | ----- | ---------- |
| **MAE**  | 46.72 | 55.36      |
| **RMSE** | 60.92 | 67.43      |
| **R²**   | -4.79 | -1.10      |
| ---      |

### Modelo 1.3: Parámetros (2,1,0)(1,1,0,24)

- **Variables Endógenas**: Precio
- **Variables Exógenas temporales**: Hora, día de la semana, mes del año
- **Variables Exógenas adicionales (desfasadas 24 horas hacia atrás)**: Demanda real, generación eólica y solar, lag24 y lag168 (precio de la luz 24 y 168 horas antes), la media del dia anterior y la desviacion tipica para todas las varaibles (luz, generaciones y demanda).

| Métrica  | Test   | Predicción |
| -------- | ------ | ---------- |
| **MAE**  | 6.2932 | 7.4174     |
| **RMSE** | 9.4810 | 12.0819    |
| **R²**   | 0.8947 | 0.9447     |
| ---      |

## 2. XGBoost

revisar pero en principio son definitivos. Cosas a valorar:

- Eliminar el lag 1
- Cambiar los timings en los desfases

### Modelo 2.1

- **Variable objetivo**: Precio
- **Variables explicativas**: Hora, día de la semana, mes del año, Demanda real, generación eólica y solar (las tres desfasadas 24 horas hacia atrás), media y desviación típica de la variable precio 24 antes, variable precio 1 y 24 horas antes y una semana previa:

  - df['lag_1'] = df['precio'].shift(1)

  - df['lag_24'] = df['precio'].shift(24)

  - df['lag_168'] = df['precio'].shift(168)

  - df['rolling_mean_24'] = df['precio'].rolling(24).mean()

  - df['rolling_std_24'] = df['precio'].rolling(24).std()

## **Train-Test set:** 70/30

**Párametros de GridSearch y TimeSeriesSplit**:

- param_grid =

  - 'n_estimators': [300, 325, 350, 375, 400, 425, 450],
  - 'learning_rate': [0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
  - 'max_depth': [2, 3, 4, 5]

- tscv = TimeSeriesSplit(n_splits=5)
- xgb = XGBRegressor(random_state=42, reg_alpha=5, reg_lambda=1)
- grid_search = GridSearchCV
  - estimator=xgb,
  - param_grid=param_grid,
  - scoring='neg_mean_absolute_error',
  - cv=tscv,
  - n_jobs=-1,
  - verbose=2

**Hiperparámetros óptimos encontrados:**

- learning_rate': 0.04
- 'max_depth': 3
- 'n_estimators': 375
- Mejor MAE con validación cruzada: 6.00

---

Evaluación sobre el modelo:

| Métrica  | Test    | Predicción |
| -------- | ------- | ---------- |
| **MAE**  | 7.2982  | 7.4319     |
| **RMSE** | 11.0834 | 12.2298    |
| **R²**   | 0.9548  | 0.9434     |

---

### Modelo 2.2

- **Variable objetivo**: Precio
- **Variables explicativas**: Hora, día de la semana, mes del año, Demanda real, generación eólica y solar (las tres desfasadas 24 horas hacia atrás), media y desviación típica de la variable precio 24 antes, variable precio 1 y 24 horas antes y una semana previa:

  - df['lag_1'] = df['precio'].shift(1)

  - df['lag_24'] = df['precio'].shift(24)

  - df['lag_168'] = df['precio'].shift(168)

  - df['rolling_mean_24'] = df['precio'].rolling(24).mean()

  - df['rolling_std_24'] = df['precio'].rolling(24).std()

**Train-Test set:** 90/10

---

**Párametros de GridSearch y TimeSeriesSplit**:

- param_grid =

  - 'n_estimators': [300, 325, 350, 375, 400, 425, 450],
  - 'learning_rate': [0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
  - 'max_depth': [2, 3, 4, 5]

- tscv = TimeSeriesSplit(n_splits=5)
- xgb = XGBRegressor(random_state=42, reg_alpha=5, reg_lambda=1)
- grid_search = GridSearchCV
  - estimator=xgb,
  - param_grid=param_grid,
  - scoring='neg_mean_absolute_error',
  - cv=tscv,
  - n_jobs=-1,
  - verbose=2

**Hiperparámetros óptimos encontrados:**

- learning_rate': 0.04
- 'max_depth': 3
- 'n_estimators': 375
- Mejor MAE con validación cruzada: 6.00

---

Evaluación sobre el modelo:

| Métrica  | Test    | Predicción |
| -------- | ------- | ---------- |
| **MAE**  | 6.3381  | 6.7529     |
| **RMSE** | 10.7758 | 11.1385    |
| **R²**   | 0.9164  | 0.9530     |

---

### Modelo 2.3

- **Variable objetivo**: Precio
- **Variables explicativas**: Hora, día de la semana, mes del año, Demanda real, generación eólica y solar (las tres desfasadas 24 horas hacia atrás), media y desviación típica de la variable precio 24 antes, variable precio 1 y 24 horas antes y una semana previa:

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

**Párametros de GridSearch y TimeSeriesSplit**:

- param_grid =

  - 'n_estimators': [300, 325, 350, 375, 400, 425, 450],
  - 'learning_rate': [0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
  - 'max_depth': [2, 3, 4, 5]

- tscv = TimeSeriesSplit(n_splits=5)

- xgb = XGBRegressor(random_state=42, reg_alpha=5, reg_lambda=1)

- grid_search = GridSearchCV
  - estimator=xgb,
  - param_grid=param_grid,
  - scoring='neg_mean_absolute_error',
  - cv=tscv,
  - n_jobs=-1,
  - verbose=2

**Hiperparámetros óptimos encontrados:**

- learning_rate': 0.03
- 'max_depth': 3
- 'n_estimators': 300
- Mejor MAE con validación cruzada: 6.11

---

Evaluación sobre el modelo:

| Métrica  | Test    | Predicción |
| -------- | ------- | ---------- |
| **MAE**  | 7.6670  | 7.7443     |
| **RMSE** | 11.5923 | 12.9418    |
| **R²**   | 0.9505  | 0.9366     |

---

### Modelo 2.4

- **Variable objetivo**: Precio
- **Variables explicativas**: Hora, día de la semana, mes del año, Demanda real, generación eólica y solar (las tres desfasadas 24 horas hacia atrás), media y desviación típica de la variable precio 24 antes, variable precio 1 y 24 horas antes y una semana previa:

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

**Párametros de GridSearch y TimeSeriesSplit**:

- param_grid =

  - 'n_estimators': [300, 325, 350, 375, 400, 425, 450],
  - 'learning_rate': [0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
  - 'max_depth': [2, 3, 4, 5]

- tscv = TimeSeriesSplit(n_splits=5)

- xgb = XGBRegressor(random_state=42, reg_alpha=5, reg_lambda=1)

- grid_search = GridSearchCV
  - estimator=xgb,
  - param_grid=param_grid,
  - scoring='neg_mean_absolute_error',
  - cv=tscv,
  - n_jobs=-1,
  - verbose=2

**Hiperparámetros óptimos encontrados:**

- learning_rate': 0.03
- 'max_depth': 3
- 'n_estimators': 300
- Mejor MAE con validación cruzada: 6.11

---

Evaluación sobre el modelo:

| Métrica  | Test   | Predicción |
| -------- | ------ | ---------- |
| **MAE**  | 6.2932 | 7.4174     |
| **RMSE** | 9.4810 | 12.0819    |
| **R²**   | 0.8947 | 0.9447     |

---

## 3. Temporal Fusion Transformer (TFT)

### Modelo 3.1: Configuración base

- **Variable objetivo**: Precio
- **Variables explicativas**: Generación eólica y solar, demanda real (las 3 retrasadas un día), hora, dia de la semana, del mes y el mes. Además, se añaden los lags en el precio a 24 horas y una semana.
  **_Nota: En el modelo ignorar time_idx y group_id, son requerimientos de TFT._**

**Hiperparámetros:**

- **max_prediction_length** = 24 _ 7 _ 4 # Predecir el próximo mes
- **max_encoder_length** = 24 _ 7 _ 4 \* 3 # Usamos los 3 meses anteriores

---

Evaluación sobre el modelo:

| Métrica  | Test    | Predicción |
| -------- | ------- | ---------- |
| **MAE**  | 7.2982  | 7.4319     |
| **RMSE** | 11.0834 | 12.2298    |
| **R²**   | 0.9548  | 0.9434     |

---

### Conclusiones

Recogemos en la siguiente tabla los resultados en cada modelo:

|                           |         | **Test** |        |         | **Validación** |        |
| :------------------------ | :------ | :------- | :----- | :------ | :------------- | :----- |
| **Modelo**                | **MAE** | **RMSE** | **R²** | **MAE** | **RMSE**       | **R²** |
| SARIMAX (2, 1, 1)x(1,1,1) | 48.12   | 12.56    | 1.94   | 84.35   | 13.01          | 1.93   |
| SARIMAX (1, 1, 1)x(1,1,1) | 47.98   | 12.33    | 1.95   | 84.15   | 12.89          | 1.94   |
| SARIMAX (1, 1, 0)x(1,1,0) | 48.05   | 12.45    | 1.94   | 84.22   | 12.95          | 1.93   |
| XGBoost 1                 | 7.30    | 11.08    | 0.96   | 7.43    | 12.23          | 0.94   |
| XGBoost 2                 | 6.33    | 10.78    | 0.92   | 6.75    | 11.14          | 0.95   |
| XGBoost 3                 | 7.67    | 11.60    | 0.95   | 7.74    | 12.94          | 0.94   |
| XGBoost 4                 | 6.29    | 9.48     | 0.89   | 7.42    | 12.08          | 0.95   |
| TFT (**SIN** búsqueda)    | 7.15    | 11.45    | 0.98   | 7.35    | 11.75          | 0.97   |
| TFT (**COn** búsqueda)    | 7.02    | 11.30    | 0.98   | 7.20    | 11.60          | 0.97   |
