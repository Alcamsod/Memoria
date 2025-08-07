# Predicción de Consumo de Luz con Modelos de Machine Learning

Este repositorio contiene los códigos para la implementación de modelos de predicción para la **_predicción del precio de luz_**. Adicionalmente, se realiza el despligue en **_GCS_** de una función con la que realizar la extracción de datos vía API de ESIOS-REE. Los archivos de datos históricos, descargados manualmente se encuentran en **_Google Drive_**.

---

## 📁 Estructura del Proyecto

```bash

├── Deploy
│   ├── data-extraction-api-esios.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── Modelos
│   │
│   ├── SARIMAX
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── SARIMAX.ipynb
│   │
│   ├── TFT
│   │   ├── checkpoints_tft_sinbusqueda
│   │   ├── checkpoints_tft_conbusqueda
│   │   ├── lightning_logs
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── TFT.ipynb
│   │
│   └── XGBoost
│       ├── README.md
│       ├── requirements.txt
│       └── XGBoost.ipynb
│
├── data-extraction-api-esios.py
│   ├── Dockerfile
│   └── requirements.txt
│
└──README.md
```

## Modelos Incluidos

- **SARIMAX**  
  Modelo estadístico tradicional para series de tiempo.

- **TFT (Temporal Fusion Transformer)**  
  Modelo de deep learning avanzado diseñado para series de tiempo multivariadas. Útil para capturar relaciones complejas y hacer predicciones con alta precisión.

- **XGBoost**  
  Algoritmo de gradient boosting eficiente y escalable.

---

## Despliegue

El despliegue de la función para la extracción de datos se realiza a traves de una **_cloud function_**, la carpeta contiene:

- **data-extraction-api-esios.py**: Código listo para ser desplegado.
- **Dockerfile**: Imagen base para ejecutar el servicio en un contenedor.
- **requirements.txt**: Lista de dependencias necesarias para el entorno.

---
