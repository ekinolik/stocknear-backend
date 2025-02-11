FROM ubuntu:24.04

WORKDIR /opt

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && \
    apt-get -y install python3 python3-pip git

WORKDIR /opt/stocknear-backend

# add local repo stuff so we can test any local modifications
COPY ./fastify /opt/stocknear-backend/fastify
COPY ./app /opt/stocknear-backend/app
COPY ./requirements.txt /opt/stocknear-backend/requirements.txt

# looks like it doesnt let us install things if not in a python virtual environment...
# which is a good thing, since it can break things. but we are in a container so we dont care
# add the --break-system-packages flag to ignore the warning
RUN python3 -m pip install -r requirements.txt --break-system-packages

ENTRYPOINT ["python3", "app/main.py"]
