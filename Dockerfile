FROM python:3.10.12-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.7.1

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . /app

ENTRYPOINT ["uvicorn", "backend_server.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
