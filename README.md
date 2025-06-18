# Recipe Card Builder

Recipe Card Builder is a monorepo that turns YouTube cooking videos into printable recipe cards.

## Features
- **Backend**: FastAPI application with Celery worker for transcript retrieval, translation and PDF generation.
- **Frontend**: Next.js and Tailwind UI for submitting jobs and editing recipes.
- **Database**: PostgreSQL 15 with SQLModel ORM.
- **Cache/Queue**: Redis 7 for Celery task management.

## Development

The easiest way to run the stack locally is with Docker Compose.

```bash
cd recipe-card-builder
docker-compose up --build
```

The API will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

### Running Tests

Backend tests use PyTest and frontend tests use Jest:

```bash
cd recipe-card-builder/backend
poetry install --no-root
poetry run pytest

cd ../frontend
npm install
npm test
```

## License

This project is licensed under the MIT License.
