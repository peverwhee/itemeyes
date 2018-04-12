FROM python:2

WORKDIR .

COPY itemeyes.py .

COPY requirements.txt ./

COPY assets/scripts /assets/scripts

COPY *.html ./

COPY __init__.py .

COPY assets/__init__.py /assets/

COPY assets/css /assets/css

RUN pip install mysqlclient

ENTRYPOINT python itemeyes.py 127.0.0.1