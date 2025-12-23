FROM python:3.11-slim
RUN groupadd -r customgroup && useradd -r -g customgroup customuser

RUN mkdir -p /app && chown customuser:customgroup /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip -i https://mirror-pypi.runflare.com/simple

COPY --chown=customuser:customgroup requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt -i https://mirror-pypi.runflare.com/simple

COPY --chown=customuser:customgroup . /app/
USER customuser
