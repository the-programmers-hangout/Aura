FROM python:3.8.2

WORKDIR /app

COPY requirements.txt ./app/requirements.txt

# Reduce Docker image size by disabling cache
RUN pip install --no-cache-dir -r ./app/requirements.txt

COPY . ./app

# force the stdout and stderr streams to be unbuffered
CMD [ "python", "-u", "./app/bot.py"]
