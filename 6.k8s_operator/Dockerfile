FROM python:3-buster

RUN pip install kubernetes kopf

ENV PYTHONPATH=/app/lib

COPY main.py /app/lib/k8soperator/main.py
COPY envs /app/lib/k8soperator/envs

WORKDIR /app/lib

ENTRYPOINT kopf run --standalone k8soperator/main.py -m k8soperator.envs