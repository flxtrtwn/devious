FROM python:latest
RUN mkdir -p ${DEPLOYMENT_DIR}
RUN mkdir -p ${DEPLOYMENT_DIR}/pip_cache
COPY requirements.txt start-server.sh ${DEPLOYMENT_DIR}
#TODO: COPY .pip_cache /opt/app/pip_cache/
COPY app ${DEPLOYMENT_DIR}/app
WORKDIR ${DEPLOYMENT_DIR}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install fastapi uvicorn gunicorn --cache-dir pip_cache
RUN pip install -r requirements.txt --cache-dir pip_cache
RUN chown -R www-data:www-data ${DEPLOYMENT_DIR}
STOPSIGNAL SIGTERM
RUN chmod +x start-server.sh
EXPOSE ${APPLICATION_PORT}
CMD ["./start-server.sh"]
