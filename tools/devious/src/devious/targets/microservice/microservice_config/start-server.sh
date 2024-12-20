#!/usr/bin/env bash
cd app && gunicorn ${TARGET_NAME}.main:app --user www-data --bind 127.0.0.1:${APPLICATION_PORT} -w 4 -k uvicorn.workers.UvicornWorker
