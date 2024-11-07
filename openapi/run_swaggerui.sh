#! /bin/bash
docker stop lw_swagger_ui
docker rm lw_swagger_ui

API_GW_ID=`aws apigateway get-rest-apis | jq '.items[] | select(.name | startswith("lw_api_gw")).id' | tr -d '"' `

aws apigateway get-export --parameters extensions='apigateway' --rest-api-id $API_GW_ID --stage-name dev --export-type swagger ./openapi.json

docker run --platform linux/arm64  --name lw_swagger_ui -d -p 8080:8080 -e SWAGGER_JSON=/lw/openapi.json -v ./:/lw swaggerapi/swagger-ui