FROM python:3.9-slim

WORKDIR /app/
COPY . /app/

RUN apt-get update 
RUN apt-get install -y ffmpeg --fix-missing

RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt

CMD ["python", "./src/main.py"]