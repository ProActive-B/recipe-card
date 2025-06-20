from __future__ import annotations

import os
import uuid

from celery import Celery
from youtube_transcript_api import YouTubeTranscriptApi
from langdetect import detect
from transformers import pipeline
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from sqlmodel import Session, create_engine, select

from .models import Job, Recipe
from .extract import parse_transcript

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)

celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)


def translate_text(text: str, src: str, tgt: str) -> str:
    if src == tgt:
        return text
    translator = pipeline("translation", model=f"Helsinki-NLP/opus-mt-{src}-{tgt}")
    return translator(text, max_length=400)[0]["translation_text"]


@celery_app.task()
def process_video(job_id: str) -> None:
    with Session(engine) as session:
        job = session.get(Job, job_id)
        if not job:
            return
        job.status = "in_progress"
        session.add(job)
        session.commit()
        video_id = job.video_url.split("v=")[-1]
        existing = session.exec(select(Recipe).where(Recipe.video_id == video_id)).first()
        if existing:
            job.status = "completed"
            job.recipe_id = existing.id
            session.commit()
            return
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        except Exception:
            job.status = "failed"
            session.commit()
            return
        transcript_text = " ".join(chunk["text"] for chunk in transcript_list)
        src_lang = detect(transcript_text)
        try:
            if src_lang != "en" and job.target_lang != "en":
                text_en = translate_text(transcript_text, src_lang, "en")
                translated = translate_text(text_en, "en", job.target_lang)
            else:
                translated = translate_text(transcript_text, src_lang, job.target_lang)
        except Exception:
            job.status = "failed"
            session.commit()
            return
        recipe_data = parse_transcript(translated)
        recipe = Recipe(
            id=str(uuid.uuid4()),
            video_id=video_id,
            title=recipe_data.get("title", ""),
            ingredients=recipe_data.get("ingredients", "[]"),
            steps=recipe_data.get("steps", "[]"),
            servings=recipe_data.get("servings"),
            cook_time=recipe_data.get("cook_time"),
        )
        session.add(recipe)
        job.status = "completed"
        job.recipe_id = recipe.id
        session.commit()
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
        template = env.get_template("card.html")
        html_str = template.render(recipe=recipe)
        output_dir = os.path.join(os.path.dirname(__file__), "static", "cards")
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = os.path.join(output_dir, f"{recipe.id}.pdf")
        HTML(string=html_str).write_pdf(pdf_path)
