# TODO: Evaluate docker compose build https://medium.com/@adamsokode/dockerize-django-application-with-nginx-reverse-proxy-79036606fa5
# TODO: https://github.com/nginxinc/docker-nginx-unprivileged
FROM python:latest
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
COPY dhparam.pem /etc/ssl/certs/
RUN mkdir -p ${DEPLOYMENT_DIR}
RUN mkdir -p ${DEPLOYMENT_DIR}/pip_cache
COPY requirements.txt start-server.sh ${DEPLOYMENT_DIR}
#TODO: COPY .pip_cache /opt/app/pip_cache/
COPY app ${DEPLOYMENT_DIR}/app
WORKDIR ${DEPLOYMENT_DIR}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install django django-bootstrap-v5 django-theme-soft-design gunicorn --cache-dir pip_cache
RUN pip install -r requirements.txt --cache-dir pip_cache
RUN chown -R www-data:www-data ${DEPLOYMENT_DIR}
EXPOSE ${EXPOSED_PORTS}
STOPSIGNAL SIGTERM
RUN chmod +x app/manage.py
RUN chmod +x start-server.sh
CMD ["./start-server.sh"]
