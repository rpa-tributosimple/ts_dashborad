import logging
from fastapi import FastAPI, Depends, HTTPException, status, Query, Request
from models.models import (JobAfip, JobAfccma, JobAfsales, JobAfddjj,
                           JobAfpurchases, JobAfconst, JobAgip, JobArba)
from db.db import db_dependency
from util.constants import JOBS_STATE
import traceback
from logging_config import setup_logging
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from enum import Enum

setup_logging()


app = FastAPI()


log_prod = logging.getLogger("Dash")

# Configura el directorio de plantillas
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class = HTMLResponse)
async def home(db: db_dependency, request: Request):
    try:
        # Lista de modelos y nombres correspondientes
        job_models = [
            ("afip", JobAfip),
            ("afccma", JobAfccma),
            ("afsales", JobAfsales),
            ("afddjj", JobAfddjj),
            ("afpurch", JobAfpurchases),
            ("afconst", JobAfconst),
            ("agip", JobAgip),
            ("arba", JobArba),
        ]

        # Diccionario para almacenar los conteos individuales
        tareas = {}
        tareas_queue = {}
        total_count = 0
        total_count_queues = 0

        # Realiza la consulta y cuenta para cada modelo
        for name, model in job_models:
            count = db.query(model).filter(model.state == JOBS_STATE.FINISHED).count()
            tareas[name] = count
            total_count += count  # Acumula el conteo total

        tareas["totals"] = total_count

        tareas_df = pd.DataFrame([tareas])

        for name, model in job_models:
            count_queues = db.query(model).filter(model.state == JOBS_STATE.PENDING).count()
            tareas_queue[name] = count_queues
            total_count_queues += count_queues  # Acumula el conteo total

        tareas_queue["totals"] = total_count_queues

        tareas_queue_df = pd.DataFrame([tareas_queue])


        return templates.TemplateResponse("dashboard.html", { "request": request,
                                                              "columns": tareas_df.columns,
                                                              "rows": tareas_df.to_dict(orient="records"),
                                                              "columns1": tareas_queue_df.columns,
                                                              "rows1": tareas_queue_df.to_dict(orient="records")

                                                              })


    except Exception as e:
        trace = traceback.format_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ERROR AL BUSCAR DATOS: {trace}"
        )


@app.get("/all")
def get_all(db: db_dependency, skip: int = 0, limit: int = 10, ):
    tasks = db.query(JobAfip).filter(JobAfip.state == 1).offset(skip).limit(limit).all()
    return tasks


@app.get("/ready")
async def ready_tasks(db: db_dependency):
    try:
        # Lista de modelos y nombres correspondientes
        job_models = [
            ("afip", JobAfip),
            ("afccma", JobAfccma),
            ("afsales", JobAfsales),
            ("afddjj", JobAfddjj),
            ("afpurch", JobAfpurchases),
            ("afconst", JobAfconst),
            ("agip", JobAgip),
            ("arba", JobArba),
        ]

        # Diccionario para almacenar los conteos individuales
        tareas = {}
        total_count = 0

        # Realiza la consulta y cuenta para cada modelo
        for name, model in job_models:
            count = db.query(model).filter(model.state == JOBS_STATE.FINISHED).count()
            tareas[name] = count
            total_count += count  # Acumula el conteo total

        tareas["totals"] = total_count

        return {
            #"status": 200,
            #"total_queue_tasks": total_count,
            "individuals_tasks_done": tareas
        }

    except Exception as e:
        trace = traceback.format_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ERROR AL BUSCAR DATOS: {trace}"
        )


@app.get("/queue")
async def in_queue_tasks(db: db_dependency):
    try:
        # Lista de modelos y nombres correspondientes
        job_models = [
            ("afip", JobAfip),
            ("afccma", JobAfccma),
            ("afsales", JobAfsales),
            ("afddjj", JobAfddjj),
            ("afpurch", JobAfpurchases),
            ("afconst", JobAfconst),
            ("agip", JobAgip),
            ("arba", JobArba),
        ]

        # Diccionario para almacenar los conteos individuales
        tareas = {}
        total_count = 0

        # Realiza la consulta y cuenta para cada modelo
        for name, model in job_models:
            count = db.query(model).filter(model.state == JOBS_STATE.PENDING).count()
            tareas[name] = count
            total_count += count  # Acumula el conteo total

        tareas["totals"] = total_count

        return {
            #"status": 200,
            #"total_queue_tasks": total_count,
            "individuals_queques_tasks": tareas
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ERROR AL BUSCAR DATOS"
        )



@app.get("/get_task")
async def get_task_by_id(db: db_dependency, id: str):
    try:
        # Lista de modelos y nombres correspondientes
        job_models = [
            ("afip", JobAfip),
            ("afccma", JobAfccma),
            ("afsales", JobAfsales),
            ("afddjj", JobAfddjj),
            ("afpurch", JobAfpurchases),
            ("afconst", JobAfconst),
            ("agip", JobAgip),
            ("arba", JobArba),
        ]

        # Diccionario para almacenar los conteos individuales
        tareas = {}
        total_count = 0

        # Realiza la consulta y cuenta para cada modelo
        for name, model in job_models:
            job = db.query(model).filter(model.msg_id == id).first()

            if job is not None:
                count = db.query(model).filter(model.state == JOBS_STATE.FINISHED).count()
                posicion = job.id - count

                if job.state == 0:
                    return {
                        "msg": "RELAJATE Y PEINATE TODAVIA FALTAN TAREAS!!!",
                        "Pendind": posicion
                    }
                else:
                    return {
                        "Task": job
                    }


    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ERROR AL BUSCAR DATOS"
        )


class TipoService(str, Enum):
    afip_get_sales = "get_sales"
    sales2 = "sales2"
    get_purchases = "purchases"
    purchases2 = "purchases2"
    ccma = "ccma"
    ccma2 = "ccma2"
    ddjj = "ddjj"
    ddjj2 = "ddjj2"
    get_category = "get_category"
    alta_monotributo = "alta_monotributo"
    get_image = "get_image"
    siper = "siper"


@app.get("/get_totals_by")
async def get_total_tasks_by(db: db_dependency, instancia, servirce: TipoService):
    count = 0
    models = [
                ("afip", JobAfip),
                ("afccma", JobAfccma),
                ("afsales", JobAfsales),
                ("afddjj", JobAfddjj),
                ("afpurchases", JobAfpurchases),
                ("afconst", JobAfconst),
                ("agip", JobAgip),
                ("arba", JobArba),

        ]

    insta = ["afip", "afccma", "afsales", "afddjj", "afpurchases", "const"]

    if instancia not in insta:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                            detail=f"No existe la instancia #### {instancia} ####\n"
                                   f"instancias disponibles:\n"
                                   f"afip,\n"
                                   f"sales,\n"
                                   f"purchases,\n"
                                   f"ccma,\n"
                                   f"ddjj,\n"
                                   f"const,")


    for servicio, tabla in models:
        if instancia == servicio:

            is_service = db.query(tabla).filter(tabla.service == servirce).first()

            if not is_service:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service not found in table")

            count = db.query(tabla).filter(tabla.service == servirce).count()

    return count


@app.post("/get_cuit")
async def get_user_cuit(q: str = Query()):
    return q