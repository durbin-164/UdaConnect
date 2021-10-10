FROM python:3.8-alpine

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "person_visit_consumer.py"]