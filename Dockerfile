FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3.7 \
    python3-requests \
    python3-dateutil \
    python3-pip
#    python3-boto3 \
RUN pip3 install pyyaml

RUN mkdir /apps
COPY main.py /apps/main.py
COPY constants.py /apps/constants.py
COPY predictionClass.py /apps/predictionClass.py
COPY streamData.py /apps/streamData.py
COPY sendToClient.py /apps/sendToClient.py

WORKDIR /apps
ENTRYPOINT ["python3.7", "main.py"]
