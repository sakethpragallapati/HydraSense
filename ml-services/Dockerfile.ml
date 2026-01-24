# ml-services/Dockerfile.ml
FROM python:3.9-slim

# 1. Setup HF User (Security Requirement)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# 2. Permissions fix: Copy files and give ownership to 'user'
COPY --chown=user requirements.txt .
COPY --chown=user setup.py . 

# 3. Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 4. Copy source code
COPY --chown=user src ./src
COPY --chown=user ml-services ./ml-services
COPY --chown=user artifacts ./artifacts

ENV PYTHONPATH="${PYTHONPATH}:/app"

# 5. HF Spaces REQUIRES port 7860
EXPOSE 7860

# 6. Run command binding to 0.0.0.0:7860
CMD ["python", "ml-services/app.py"]