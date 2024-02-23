FROM python:3.11-slim

WORKDIR /workspace

COPY ./requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /workspace/requirements.txt

COPY ./app /workspace/app

# CMD ["python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8100"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8100"]
