FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# workflows / data はマウント前提
ENV NAT_CONFIG=/app/workflows/workflow.yml

ENTRYPOINT ["nat"]
CMD ["run", "--config_file", "/app/workflows/workflow.yml"]
