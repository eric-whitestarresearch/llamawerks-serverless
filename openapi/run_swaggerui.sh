#! /bin/bash
docker stop lw_swagger_ui
docker rm lw_swagger_ui

PULUMI_DIR=`readlink -f ../pulumi`
docker run --platform linux/arm64  --name lw_swagger_ui -d -p 8080:8080 -e SWAGGER_JSON=/lw/openapi.yaml -v $PULUMI_DIR:/lw swaggerapi/swagger-ui