FROM python:3.7

ADD requirements.txt /
RUN pip install -r requirements.txt

RUN mkdir /app
ADD . /app
WORKDIR /app

CMD python map_bot.py