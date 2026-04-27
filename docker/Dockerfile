FROM python:3.11-slim AS builder
WORKDIR /build
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /srv
RUN rm -rf \
    /usr/local/lib/python3.11/site-packages/pip* \
    /usr/local/lib/python3.11/site-packages/setuptools* \
    /usr/local/lib/python3.11/site-packages/wheel* \
    /usr/local/bin/pip* \
    /usr/local/bin/wheel*
COPY --from=builder /install /usr/local
COPY app/ ./app/

RUN useradd --no-create-home --uid 1000 appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
