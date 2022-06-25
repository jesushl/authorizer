FROM python:3.8
LABEL maintainer="Jesus Herrera  <jesushledon@gmail.com>"
LABEL description="Single transacton validation exersice"
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /usr/src/app
COPY . .
RUN echo 'alias operations="./operations.sh"'>> ~/.bashrc
# runnig tests
RUN apt-get update &&\
        python3 -m unittest
RUN pwd 
RUN ls -la
