#!/usr/bin/env bash
cd app && gunicorn ${TARGET_NAME}.main:app --user www-data --bind 0.0.0.0:${APPLICATION_PORT} -w 4 -k uvicorn.workers.UvicornWorker
