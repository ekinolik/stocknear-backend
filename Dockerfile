FROM ubuntu:24.04

WORKDIR /opt

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && \
    apt-get -y install python3 python3-pip git

WORKDIR /opt/stocknear-backend

ARG API_PORT=8000  # Declare ARG
ENV API_PORT=${API_PORT}
ENV USER_API_KEY="test"

# add local repo stuff so we can test any local modifications
COPY ./fastify /opt/stocknear-backend/fastify
COPY ./app /opt/stocknear-backend/app
COPY ./app/backup_db/* /opt/stocknear-backend/
COPY ./app/json/ /opt/stocknear-backend/json/
COPY ./requirements.txt /opt/stocknear-backend/requirements.txt

# looks like it doesnt let us install things if not in a python virtual environment...
# which is a good thing, since it can break things. but we are in a container so we dont care
# add the --break-system-packages flag to ignore the warning
RUN python3 -m pip install -r requirements.txt --break-system-packages

EXPOSE 8000
ENTRYPOINT ["python3", "app/main.py"]
