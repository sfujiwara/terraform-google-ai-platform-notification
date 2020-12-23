#!/bin/sh

VERSION=$(poetry version | awk '{print $2}')
IMAGE=gcr.io/sfujiwara/ai-platform-notification

docker build \
  --tag "${IMAGE}:${VERSION}" \
  --tag "${IMAGE}:latest" \
  .

docker push "${IMAGE}:${VERSION}"
docker push "${IMAGE}:latest"
