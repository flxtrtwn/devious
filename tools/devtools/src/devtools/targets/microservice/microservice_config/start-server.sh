#!/usr/bin/env bash
cd app && gunicorn main:app --user www-data --bind 127.0.0.1:${APPLICATION_PORT} -w 4 -k uvicorn.workers.UvicornWorker
