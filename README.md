# Actividad de Prediccion de Precios de Vehiculos con AWS

## Descripcion del proyecto

Este proyecto implementa un sistema completo de prediccion de precios de vehiculos a partir de atributos tecnicos y comerciales del automovil. La solucion combina un frontend web en Next.js, un pipeline de entrenamiento en Python con XGBoost y un servicio de inferencia desplegable en AWS Lambda mediante contenedor Docker.

Actualmente, la aplicacion permite:

1. Capturar desde la web las caracteristicas del vehiculo mediante un formulario interactivo.
2. Validar y transformar los datos de entrada al mismo formato numerico esperado por el modelo.
3. Consultar un endpoint HTTP desplegado en AWS para obtener el precio estimado.
4. Entrenar nuevamente el modelo a partir del dataset original.
5. Exportar el modelo entrenado y los catalogos de apoyo en formato JSON para integrarlos con el frontend y la inferencia serverless.

## Objetivo del proyecto

Desarrollar una solucion de inferencia para estimar precios de vehiculos integrando procesamiento de datos, aprendizaje automatico, despliegue cloud y una interfaz web de consulta. El proyecto demuestra el flujo completo desde la preparacion de datos hasta el consumo del modelo desde una aplicacion cliente.

## Funcionalidades principales

- Formulario web con campos para fabricante, modelo, categoria, combustible, transmision, traccion, puertas, volante, color, interior de cuero, turbo, levy, anio, cilindraje, kilometraje, numero de cilindros y airbags.
- Validacion de entradas numericas en el cliente antes de enviar la solicitud.
- Transformacion de variables numericas mediante escalado Min-Max para mantener consistencia con el entrenamiento.
- Mapeo de variables categoricas usando catalogos JSON generados desde el pipeline de preprocesamiento.
- Sugerencias de autocompletado para fabricante y modelo mediante listas derivadas del dataset procesado.
- Consumo de una API HTTP en AWS API Gateway que invoca una funcion Lambda para ejecutar la prediccion.
- Respuesta inmediata en la interfaz con el precio estimado del vehiculo.
- Pipeline de entrenamiento que limpia datos, entrena un modelo XGBoost, selecciona el mejor fold y exporta artefactos reutilizables.
- Generacion de metricas de desempeno sobre conjuntos de entrenamiento, validacion y prueba.

## Arquitectura general

El flujo actual del sistema es el siguiente:

1. El usuario completa el formulario web desde la interfaz construida con Next.js y React.
2. El frontend valida los campos y transforma los valores numericos y categoricos con apoyo de [app/utils.ts](app/utils.ts) y [app/data/JSON/Database.json](app/data/JSON/Database.json).
3. La aplicacion envia la carga util al endpoint HTTP configurado en [app/page.tsx](app/page.tsx).
4. AWS API Gateway redirige la solicitud a la funcion Lambda contenida en [app/preprocessing/Python/AWS/Docker/project/lambda_function.py](app/preprocessing/Python/AWS/Docker/project/lambda_function.py).
5. Lambda carga el modelo XGBoost y devuelve el precio estimado como respuesta JSON.
6. El frontend muestra el resultado final al usuario.

## Entrenamiento y generacion de artefactos

El script [app/preprocessing/Python/main.py](app/preprocessing/Python/main.py) contiene el flujo de entrenamiento del modelo. Entre sus responsabilidades actuales se incluyen:

- Lectura del dataset original de precios de vehiculos.
- Separacion de datos en folds para evaluar distintas particiones.
- Limpieza y transformacion de variables mediante utilidades de preprocesamiento.
- Entrenamiento de un modelo de regresion con XGBoost.
- Seleccion del mejor fold segun su rendimiento.
- Evaluacion con metricas como Spearman, MSE y RMSE.
- Exportacion del modelo entrenado en JSON.
- Generacion de un archivo de apoyo con escalas y valores categoricos para que el frontend replique exactamente las transformaciones de entrenamiento.

Los artefactos relevantes generados por el proceso se almacenan en:

- [app/preprocessing/Python/data/JSON/model.json](app/preprocessing/Python/data/JSON/model.json)
- [app/preprocessing/Python/data/JSON/Database.json](app/preprocessing/Python/data/JSON/Database.json)

## Requisitos tecnicos

### Software base

- Node.js 18 o superior, recomendado Node.js 20+
- npm 9 o superior
- Python 3.12
- Docker Desktop

### Stack del frontend

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS 4

Instalacion de dependencias del frontend:

```bash
npm install
```

### Dependencias de Python

- xgboost
- numpy
- scipy
- scikit-learn
- pandas

Instalacion de dependencias para inferencia en el contenedor de Lambda:

```bash
pip install -r app/preprocessing/Python/AWS/Docker/project/requirements.txt
```

Si se desea ejecutar el pipeline de entrenamiento localmente, se deben instalar tambien las dependencias requeridas por el entorno Python que se utilice para [app/preprocessing/Python/main.py](app/preprocessing/Python/main.py).

### Requisitos de AWS

- Cuenta de AWS activa
- Permisos para usar Amazon ECR, AWS Lambda y Amazon API Gateway
- AWS CLI configurado si se desea desplegar la solucion en la nube

## Ejecucion local

### Frontend

```bash
npm install
npm run dev
```

La aplicacion quedara disponible en el entorno local de Next.js. El formulario enviara solicitudes al endpoint HTTP actualmente configurado en [app/page.tsx](app/page.tsx), por lo que si se despliega una API distinta debe actualizarse esa URL.

### Entrenamiento del modelo

```bash
python app/preprocessing/Python/main.py
```

Al finalizar el proceso se actualizan los artefactos del modelo y de transformacion de datos utilizados por el frontend y por la capa de inferencia.

## Estructura relevante del proyecto

```text
app/
  page.tsx                                # Formulario principal, validacion y llamada a API Gateway
  utils.ts                                # Reglas de validacion y transformaciones numericas
  data/JSON/Database.json                 # Catalogos y escalas consumidos por el frontend
  preprocessing/Python/
    main.py                               # Entrenamiento, evaluacion y exportacion de artefactos
    data/                                 # Dataset original y subconjuntos procesados
    utils/cleansing/DataCleaner.py        # Limpieza y escalado de datos
    utils/JSONBuilder.py                  # Generacion de JSON para frontend y soporte de inferencia
    AWS/Docker/project/
      lambda_function.py                  # Handler de AWS Lambda para prediccion
      Dockerfile                          # Imagen de Lambda basada en Python 3.12
      requirements.txt                    # Dependencias de inferencia
      model.json                          # Modelo utilizado en el entorno serverless
documentation/
  frontend.png                            # Captura de la interfaz
  Reporte.zip                             # Material de apoyo de la actividad
```

## Consideraciones de integracion

- El frontend no envia los valores crudos directamente al modelo; primero aplica las mismas transformaciones definidas por el preprocesamiento.
- Las variables categoricas disponibles en la interfaz dependen de los catalogos generados desde el dataset procesado.
- La inferencia en AWS espera que los campos lleguen en un orden especifico y con valores numericos transformados.
- Si se reentrena el modelo con cambios en preprocesamiento o columnas, deben actualizarse conjuntamente el modelo exportado y el archivo [app/data/JSON/Database.json](app/data/JSON/Database.json).

## Documentacion adicional

El directorio [documentation](documentation) contiene material visual y de apoyo relacionado con la actividad y la presentacion del proyecto.