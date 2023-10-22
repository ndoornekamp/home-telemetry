FROM python:3.12-slim

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt --no-cache-dir

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

WORKDIR /app
COPY home_telemetry /app/home_telemetry

CMD ["python", "-m", "home_telemetry"]
