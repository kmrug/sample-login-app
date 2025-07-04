# Use Python base image
FROM python:3

# Set base working directory
WORKDIR /usr/src/app

# Install required dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]