# Actividad de Prediccion de Precios de Vehiculos con AWS

## Descripcion del proyecto

Este proyecto se basa en una actividad sobre prediccion de precios de vehiculos usando un modelo de Machine Learning entrenado en Python y publicado en la nube con servicios de AWS. La aplicacion web (Next.js + React) permite capturar caracteristicas del vehiculo, transformarlas al formato esperado por el modelo y consultar una API desplegada en AWS para obtener el precio estimado.

El flujo general es:

1. Preprocesamiento y entrenamiento del modelo con Python.
2. Exportacion del modelo y tablas de apoyo en formato JSON.
3. Empaquetado del predictor en contenedor de Docker para AWS Lambda.
4. Exposicion del endpoint mediante API Gateway.
5. Consumo del endpoint desde el frontend web.

## Objetivo de la actividad

Desarrollar y desplegar un sistema de inferencia para estimar precios de vehiculos, integrando herramientas de ciencia de datos y cloud computing:

- Python para limpieza de datos, transformacion de variables y entrenamiento del modelo (XGBoost).
- Docker para empaquetar la funcion de inferencia con sus dependencias.
- AWS Lambda para ejecutar la prediccion de forma serverless.
- API Gateway para publicar un endpoint HTTP consumible desde la web.
- Next.js/React para construir una interfaz de captura y consulta de prediccion.

## Requisitos tecnicos

### Software base

- Node.js 18+ (recomendado 20+)
- npm 9+
- Python 3.12
- Docker Desktop

### Dependencias del frontend

- Next.js 16
- React 19
- TypeScript

Instalacion:

```bash
npm install
```

### Dependencias de Python (entrenamiento/inferencia)

- xgboost
- numpy
- scipy
- scikit-learn
- pandas

Instalación local:

```bash
cd app/preprocessing/Python/AWS/Docker/project
pip install -r "app/preprocessing/Python/AWS/Docker/project/requirements.txt"
```

### Requisitos de AWS

- Cuenta de AWS activa
- Permisos para usar:
	- Amazon ECR
	- AWS Lambda
	- Amazon API Gateway
- AWS CLI configurado


## Estructura relevante del proyecto

```text
app/
	page.tsx                                # Formulario y llamada a API Gateway
	utils.ts                                # Transformaciones numericas de entrada
	data/JSON/Database.json                 # Diccionarios de categorias/valores escalados
	preprocessing/Python/
		main.py                               # Entrenamiento del modelo
		utils/cleansing/DataCleaner.py        # Limpieza y escalado
		utils/JSONBuilder.py                  # Generacion de JSON para frontend
		AWS/Docker/project/
			lambda_function.py                  # Handler de AWS Lambda
			Dockerfile                          # Imagen de Lambda (Python 3.12)
			requirements.txt                    # Dependencias de inferencia
			model.json                          # Modelo usado por Lambda
```

## Documentación
Para más información sobre la actividad, consultar el archivo "Documentación.PDF" dentro de "documentation".