# syntax=docker/dockerfile:1
FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . /app/
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["/bin/bash", "-c", "python3 task_1.py && python3 task_2.py"]
