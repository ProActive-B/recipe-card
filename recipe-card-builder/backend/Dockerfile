FROM ghcr.io/library/python:3.12-slim

ENV POETRY_VERSION=1.6.1

RUN apt-get update && apt-get install -y build-essential libffi-dev libpq-dev libxml2-dev libxslt1-dev libjpeg-dev libpangocairo-1.0-0 libpangoft2-1.0-0 libcairo2 libpango1.0-dev && rm -rf /var/lib/apt/lists/*
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root
RUN python -m spacy download en_core_web_sm
COPY . /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
