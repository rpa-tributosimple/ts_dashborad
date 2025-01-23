import streamlit as st
import pandas as pd
import requests
#
# DEV = True
#
# if not DEV:
#     # URLs de FastAPI
#     url_tasks_done = "http://localhost:80/ready"
#     url_tasks_queues = "http://localhost:80/queue"
# else:
#     # URLs de FastAPI
#     url_tasks_all = "http://localhost:8000/all"
#     url_tasks_done = "http://localhost:8000/ready"
#     url_tasks_queues = "http://localhost:8000/queue"

url_tasks_done = "http://localhost:80/ready"
url_tasks_queues = "http://localhost:80/queue"



st.title("DASHBOARD DE TAREAS KAFKA")

# st.title("Búsqueda con Query en URL")

# Input de texto
query = st.text_input("Introduce tu consulta:", placeholder="identificador ...")

# Botón para ejecutar la búsqueda
if st.button("Realizar búsqueda"):
    if query:
        # Crear la URL con el query
        # base_url = "http://localhost:8000/get_task"
        base_url = "http://localhost:80/get_task"
        full_url = f"{base_url}?id={query}"

        # Mostrar la URL generada
        st.write("URL generada:")
        st.write(full_url)

        # (Opcional) Realizar una consulta HTTP
        try:
            response = requests.get(full_url)
            if response.status_code == 200:
                st.success("Consulta realizada exitosamente!")
                st.json(response.json())  # Mostrar el JSON de la respuesta si aplica
            else:
                st.error(f"Error en la consulta: {response.status_code}")
        except Exception as e:
            st.error(f"Error al realizar la consulta: {e}")
    else:
        st.warning("Por favor, introduce un texto para la búsqueda.")



try:
    # Hacer solicitud GET a FastAPI para obtener los datos
    response = requests.get(url_tasks_done)
    response_in_queque = requests.get(url_tasks_queues)

    response.raise_for_status()
    data = response.json()
    data2 = response_in_queque.json()

    # Convertir a DataFrames
    # print(data)
    # print(data2)
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

