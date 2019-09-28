FROM ubuntu:latest

RUN echo "set tabstop=2 shiftwidth=2 expandtab" > ~/.vimrc 

RUN apt-get update && apt-get install -y \
    python3.7 \
    python3-pip \
    python3-requests \
    python3-flask \
    vim 
#    python3-boto3 \

COPY getNextDeparture.py /apps/getNextDeparture.py

ENTRYPOINT tail -f /dev/null
