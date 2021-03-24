#!/bin/bash

#THREADS=${THREADS:-2}

echo "PORT: ${PORT}"
#echo "WEB_CONCURRENCY (WORKERS): ${WEB_CONCURRENCY}"
#echo "THREADS: ${THREADS}"

uvicorn server.main:app --host 0.0.0.0 --port "${PORT}"
