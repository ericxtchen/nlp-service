FROM pytorch/pytorch:2.8.0-cuda12.9-cudnn9-runtime

# Set working dir
WORKDIR /app

RUN apt-get update && apt-get install -y \
    git curl vim build-essential netcat \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-u", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]