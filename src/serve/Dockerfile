# 1. Base image
FROM python:3.9-buster

# 2. Specify directory where all subsequent instructions are run
WORKDIR /app

# 3. Copy files
COPY predict.py /app/predict.py
COPY requirements.txt /app/requirements.txt

# 4. Install dependencies
RUN pip install -r /app/requirements.txt

ENV BUCKET=sepsis-prediction-mlops
ENV AIP_HEALTH_ROUTE=/ping
ENV AIP_PREDICT_ROUTE=/predict
ENV AIP_HTTP_PORT=8080

# 5. Sets up the entry point to invoke the trainer.
ENTRYPOINT ["python", "predict.py"]