FROM python:3 as base

RUN apt-get update && apt-get install -y --reinstall wamerican

ADD . .

CMD [ "python", "./make_guess.py" ]
