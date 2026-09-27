FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install .

COPY entrypoint.sh /usr/local/bin/bakery-entrypoint
RUN chmod +x /usr/local/bin/bakery-entrypoint
COPY . .
RUN chown -R app:app /app

USER app
ENTRYPOINT ["/usr/local/bin/bakery-entrypoint"]

FROM base AS development
USER root
RUN pip install ".[dev]"
USER app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base AS production
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-", "--error-logfile", "-"]

