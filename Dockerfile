FROM ubuntu:20.04 
ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y && apt upgrade -y && apt install -y python3-pip

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /code

EXPOSE 8000

ENTRYPOINT ["/bin/bash","run.sh"]