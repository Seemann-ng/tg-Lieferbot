FROM python:3.12
LABEL authors="Seemann-ng"

COPY ../requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY customer_bot /app
COPY ../tools /app/tools

WORKDIR /app

ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]