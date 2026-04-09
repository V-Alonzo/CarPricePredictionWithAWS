FROM public.ecr.aws/lambda/python:3.12

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install -r requirements.txt

# Copiar código y modelo
COPY lambda_function.py .
COPY model2.json .

# Handler
CMD ["lambda_function.lambda_handler"]
