FROM ubuntu:latest
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    python3.7 \
    python3-requests \
    python3-dateutil \
    python3-pip

RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python3.7 /usr/bin/python3
RUN pip3 install pyyaml flask flask_restful circuitbreaker

RUN mkdir /apps
COPY src/main.py /apps/main.py
COPY src/constants.py /apps/constants.py
COPY src/predictionClass.py /apps/predictionClass.py
COPY src/streamData.py /apps/streamData.py
COPY src/clientApiHandler.py /apps/clientApiHandler.py
COPY src/readinessCheck.py /apps/readinessCheck.py
COPY src/log.py /apps/log.py

EXPOSE 443
EXPOSE 5000

WORKDIR /apps
ENTRYPOINT ["python3.7", "main.py"]
