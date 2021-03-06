FROM python:3.9-slim

ARG USER=app
ARG HOST=0.0.0.0
ARG PORT=8010

ENV PYTHONUNBUFFERED 1
ENV HOST=$HOST
ENV PORT=$PORT

COPY ./app/ /home/$USER/app/
COPY ./requirements.txt /etc/

RUN useradd -U -s /bin/bash $USER && \
    chown -R $USER:$USER /home/$USER/

WORKDIR /home/$USER/app

RUN pip install --no-cache-dir -r /etc/requirements.txt

USER $USER

EXPOSE $PORT