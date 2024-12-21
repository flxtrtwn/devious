FROM python:latest
RUN mkdir -p ${DEPLOYMENT_DIR}
RUN mkdir -p ${DEPLOYMENT_DIR}/pip_cache
COPY start-server.sh ${DEPLOYMENT_DIR}
#TODO: COPY .pip_cache /opt/app/pip_cache/
COPY app ${DEPLOYMENT_DIR}/app
WORKDIR ${DEPLOYMENT_DIR}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install fastapi uvicorn gunicorn --cache-dir pip_cache
RUN pip install -e ${DEPLOYMENT_DIR}/app
RUN chown -R www-data:www-data ${DEPLOYMENT_DIR}
STOPSIGNAL SIGTERM
RUN chmod +x start-server.sh
EXPOSE ${APPLICATION_PORT}
CMD ["./start-server.sh"]

# Mount secrets
# RUN --mount=type=secret,id=some_secret \
#     some_command --secret "$$(cat /run/secrets/some_secret)"
