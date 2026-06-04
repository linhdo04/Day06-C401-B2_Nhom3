FROM python:3.12.10-slim

RUN addgroup --gid 1001 appgroup && \
    adduser --disabled-password --gecos "" --uid 1001 --ingroup appgroup appuser

WORKDIR /code/backend

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup . ./

USER appuser

WORKDIR /code

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
