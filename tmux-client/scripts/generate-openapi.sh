#!/usr/bin/env bash
set -euo pipefail

swag init --dir .,./internal/api,./internal/audit,./internal/config,./internal/store,./internal/tools,./internal/types --generalInfo ./cmd/server/main.go --parseDependency --parseInternal

docker run --rm \
  -v "$(pwd)":/workspace \
  openapitools/openapi-generator-cli generate \
  -i /workspace/docs/swagger.yaml \
  -g openapi-yaml \
  -o /workspace/docs

mv docs/openapi/openapi.yaml docs/
rm -R docs/swagger.json docs/swagger.yaml docs/README.md docs/docs.go docs/.openapi-generator-ignore docs/.openapi-generator/ docs/openapi/
