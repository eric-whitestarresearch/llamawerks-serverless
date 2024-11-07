FROM python:3.12.7-bullseye

RUN mkdir package
# Copy code
COPY code/ ./package

# Install the specified packages
RUN pip install -r ./package/requirements.txt

CMD python3 ./package/app.py