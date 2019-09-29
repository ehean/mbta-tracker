FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3.7 \
    python3-requests 
#    python3-boto3 \
#    python3-flask \
#    python3-pip \

COPY getNextDeparture.py /apps/getNextDeparture.py
COPY constants.py /apps/constants.py

ENTRYPOINT python3.7 getNextDeparture.py
