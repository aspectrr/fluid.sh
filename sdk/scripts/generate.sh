#!/bin/bash
# scripts/generate.sh

set -e

echo "Generating SDK..."

# Generate with custom templates
docker run --rm \
  -v ${PWD}/..:/local \
  openapitools/openapi-generator-cli generate --skip-validate-spec \
  -i /local/fluid-remote/docs/openapi.yaml \
  -g python \
  -o /local/sdk/fluid-sdk-py/ \
  -c /local/sdk/.openapi-generator/config.yaml \
  -t /local/sdk/.openapi-generator/templates/python/

echo "Running polish script..."
python3 scripts/polish_sdk.py

echo "Formatting code..."
cd fluid-sdk-py
pip install -r requirements.txt
black .
isort .

echo "Finished!"
