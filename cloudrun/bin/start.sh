#!/bin/bash

echo "PORT: ${PORT}"
echo "WEB_CONCURRENCY (WORKERS): ${WEB_CONCURRENCY}"

uvicorn server.main:app --host 0.0.0.0 --port "${PORT}"
