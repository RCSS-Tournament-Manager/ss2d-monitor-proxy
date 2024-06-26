FROM python:3.12-bookworm

WORKDIR /app

RUN pip install pipenv && \
    pip install --upgrade pip


COPY ["Pipfile", "Pipfile.lock", "/app/"]

RUN pipenv install --system --deploy

COPY monitor_proxy.py /app/monitor_proxy.py
COPY ./src /app/src

CMD [ "python", "monitor_proxy.py"]