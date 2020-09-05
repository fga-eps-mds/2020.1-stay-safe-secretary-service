FROM python:3.6
ADD . /stay-safe
WORKDIR /stay-safe
RUN pip install -r requirements.txt