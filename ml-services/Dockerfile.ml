# ml-services/Dockerfile.ml
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY setup.py . 

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY ml-services ./ml-services
COPY artifacts ./artifacts

ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 7000

CMD ["python", "ml-services/app.py"]