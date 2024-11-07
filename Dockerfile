# Usa una imagen base de Python
FROM python:3.9-slim
LABEL authors="ernesto"

# Establece el directorio de trabajo
WORKDIR /app

# Copia y instala las dependencias
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copia el resto de los archivos de la aplicación
COPY . /app

# Expone el puerto para FastAPI y Streamlit
EXPOSE 80
EXPOSE 8501

# Usa un script de shell para iniciar ambos servicios en paralelo
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 80 & streamlit run streamlit/lit_app/app.py"]
