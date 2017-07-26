FROM ubuntu:latest
LABEL com.yaronp.version="0.0.1-poc"
LABEL com.example.release-date="2017-07"
LABEL com.example.version.is-production="no"
EXPOSE 5000
MAINTAINER Yaeon Pdut "yaronp@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["/app/web/app.py"]