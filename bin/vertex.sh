#!/bin/bash

gcloud ai custom-jobs create \
  --display-name example \
  --region us-central1 \
  --labels "notification=hoge,piyo=" \
  --config bin/config.yaml
