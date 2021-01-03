#!/bin/bash

THREADS=${THREADS:-2}

echo "PORT: ${PORT}"
echo "WEB_CONCURRENCY (WORKERS): ${WEB_CONCURRENCY}"
echo "THREADS: ${THREADS}"

gunicorn server.main:app --threads "${THREADS}"
