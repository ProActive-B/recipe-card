from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, create_engine, Session, select

from .models import Job, Recipe
from .tasks import process_video

import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)

router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/job")
def create_job(url: str, target_lang: str, session: Session = Depends(get_session)) -> dict:
    job = Job(id=str(uuid.uuid4()), video_url=url, target_lang=target_lang, status="pending")
    session.add(job)
    session.commit()
    process_video.delay(job.id)
    return {"job_id": job.id}


@router.get("/job/{job_id}")
def get_job(job_id: str, session: Session = Depends(get_session)) -> dict:
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    data = {"status": job.status}
    if job.status == "completed":
        data.update({"download_url": f"/static/cards/{job.recipe_id}.pdf", "recipe_id": job.recipe_id})
    return data


@router.get("/recipe/{recipe_id}")
def get_recipe(recipe_id: str, session: Session = Depends(get_session)) -> Optional[Recipe]:
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
