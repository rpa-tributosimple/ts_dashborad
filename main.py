from fastapi import FastAPI, Depends, HTTPException, status
from models.models import (JobAfip, JobAfccma, JobAfsales, JobAfddjj,
                           JobAfpurchases, JobAfconst, JobAgip, JobArba)
from db.db import db_dependency
from util.constants import JOBS_STATE

app = FastAPI()


@app.get("/all")
def get_all(db: db_dependency, skip: int = 0, limit: int = 10, ):
    tasks = db.query(JobAfip).filter(JobAfip.state == 1).offset(skip).limit(limit).all()
    return tasks


@app.get("/ready")
async def ready_tasks(db: db_dependency):
    try:
        # Lista de modelos y nombres correspondientes
        job_models = [
            ("count_afip", JobAfip),
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

        tareas["totals"]= total_count

        return {
            #"status": 200,
            #"total_queue_tasks": total_count,
            "individuals_tasks_done": tareas
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ERROR AL BUSCAR DATOS"
        )


@app.get("/queue")
async def in_queue_tasks(db: db_dependency):
    try:
        # Lista de modelos y nombres correspondientes
        job_models = [
            ("count_afip", JobAfip),
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
            ("count_afip", JobAfip),
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
