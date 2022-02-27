# Contributing

## Documentation

Update [`README.md`](README.md) with [terraform-docs](https://terraform-docs.io/).

```sh
docker-compose up terraform-docs
```

## Check example on Google Cloud Platform

### Apply Terraform module

```sh
export TF_VAR_project="<Your GCP project ID>"
export TF_VAR_region="us-central1"
```

```sh
cd examples
```

```sh
terraform apply
```

### Submit example job

```sh
./bin/ai_platform.sh
```
