FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY streamlit.py /app/streamlit_app.py
COPY requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

# Environment for streamlit app
ENV streamlit_uri=https://sepsis-predict-3wcd2ryf5q-uc.a.run.app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
