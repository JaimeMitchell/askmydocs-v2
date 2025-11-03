
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y git build-essential && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --upgrade pip

# Use venv inside container (production parity)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
