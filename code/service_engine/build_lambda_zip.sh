docker stop se_build
docker rm se_build
docker image rm service_engine:build

docker build --platform linux/arm64 -t service_engine:build .

docker run --platform linux/arm64 --name se_build -d service_engine:build

docker cp se_build:package.zip .

docker stop se_build
docker rm se_build
