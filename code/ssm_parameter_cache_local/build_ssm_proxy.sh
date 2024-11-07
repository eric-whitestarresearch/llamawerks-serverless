TAG=4
docker build --platform linux/arm64 -t ericwsr/ssm_proxy:$TAG .

docker push ericwsr/ssm_proxy:$TAG