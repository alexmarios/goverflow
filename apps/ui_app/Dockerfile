FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends openssh-client \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt watchfiles \
 && sed -i 's/LC_REVIVER = Reviver()/LC_REVIVER = Reviver(allowed_objects="core")/' \
    /usr/local/lib/python3.11/site-packages/langgraph/checkpoint/serde/jsonplus.py

# Source code is bind-mounted at runtime for live reload.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010", "--reload"]
