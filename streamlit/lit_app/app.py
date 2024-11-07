import streamlit as st
import pandas as pd
import requests



# URLs de FastAPI
url_tasks_done = "http://localhost:80/ready"
url_tasks_in_queques = "http://localhost:80/queue"

st.title("DASHBOARD DE TAREAS KAFKA")


try:
    # Hacer solicitud GET a FastAPI para obtener los datos
    response = requests.get(url_tasks_done)
    response_in_queque = requests.get(url_tasks_in_queques)
    response.raise_for_status()
    data = response.json()
    data2 = response_in_queque.json()

    # Convertir a DataFrames
    df_done = pd.DataFrame(data)
    df_queue = pd.DataFrame(data2)


    # Crear columnas para mostrar los datos
    col1, col2 = st.columns(2)
    with col1:
        st.header("Tareas en Cola")
        st.dataframe(df_queue)


    with col2:
        st.header("Tareas Completadas")
        st.dataframe(df_done)

    # Preparar datos para gráfica de barras agrupada
    df_combined = pd.concat([df_done, df_queue], axis=1)
    df_combined.columns = ['Completadas', 'En Cola']  # Renombrar columnas para claridad


    # Visualizar gráfica de barras agrupada
    st.title("Comparación de Tareas")
    st.bar_chart(df_combined)

except requests.exceptions.RequestException as e:
    st.error(f"Error al obtener datos: {e}")
