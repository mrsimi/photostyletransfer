
FROM python:3.12

WORKDIR /webapp

COPY requirements.txt .

RUN apt-get update && apt-get install -y python3-opencv
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 50505

ENTRYPOINT ["gunicorn", "app:app"]