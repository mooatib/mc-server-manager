FROM python:3.10.4

RUN mkdir -p /mcsm

WORKDIR /mcsm

COPY ./requirements.txt /requirements.txt

COPY . .

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

CMD ["python3", "bot.py"]