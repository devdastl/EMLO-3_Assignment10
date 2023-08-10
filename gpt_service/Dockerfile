FROM python:3.9-slim

WORKDIR /src
COPY requirements.txt /src

RUN pip install -U pip && pip install -r requirements.txt --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu

COPY gpt_service.py gpt.torchscript.pt /src

CMD ["gunicorn", "gpt_service:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]