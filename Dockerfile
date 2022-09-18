FROM python:3.10.6

RUN apt update && apt install host -y && apt clean

WORKDIR /app/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY script.py .

COPY devices.yml .

COPY dns_rewrite.sh .

RUN ./dns_rewrite.sh

CMD [ "python", "-u", "/app/script.py" ]
