FROM python:3.12.7-bullseye

RUN mkdir package
# Copy code
COPY code/ ./package

# Install the specified packages
RUN pip install --target ./package -r ./package/requirements.txt

RUN apt-get update && apt-get install zip

RUN cd package && zip -r ../package.zip ./*

CMD sleep 300