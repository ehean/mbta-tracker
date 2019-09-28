FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 
    python3-pip
    python3-requests
    python3-boto3 
    python-flask
    vim

ENTRYPOINT tail -f /dev/null
