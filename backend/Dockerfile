FROM python:3.12.10-slim AS builder
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade --root-user-action=ignore \
    --target=/install \
    -r requirements.txt

FROM python:3.12.10-slim
WORKDIR /code
COPY --from=builder /install /usr/local
COPY ./app /code/app

RUN addgroup --gid 1001 appgroup
RUN adduser --disabled-password --gecos "" --uid 1001 --ingroup appgroup appuser

USER appuser

EXPOSE 8000
CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]
