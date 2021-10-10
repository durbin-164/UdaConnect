FROM python:3.8-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev build-base linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5005

CMD ["python", "person_server.py"]