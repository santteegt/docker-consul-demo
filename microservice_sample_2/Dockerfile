FROM python:3.5-alpine

MAINTAINER Santiago Gonzalez, <hernangt12re3@gmail.com>

ENV APP_DIR=/flask-app

EXPOSE 8080

# App configuration
WORKDIR ${APP_DIR}
RUN mkdir -p ${APP_DIR}
COPY requirements.txt ${APP_DIR}/

RUN pip install --upgrade pip && \
	pip install -U -r requirements.txt

COPY consul.query.sample.json ${APP_DIR}/
COPY Server.py ${APP_DIR}/

ENTRYPOINT ["python"]
CMD ["Server.py", "--log-file", "-"]
