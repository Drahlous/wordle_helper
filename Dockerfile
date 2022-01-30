FROM python:3.8.0-slim as builder
RUN apt-get update && apt-get install -y --reinstall wamerican && apt-get clean

WORKDIR app
COPY . /app

FROM python:3.8.0-slim as runner
COPY --from=builder /usr/share/dict/words /usr/share/dict/words
COPY --from=builder /app/get_words.sh /app/get_words.sh
COPY --from=builder /app/make_guess.py /app/make_guess.py

ENV PATH=/root/.local/bin:$PATH

WORKDIR app

CMD [ "python3", "/app/make_guess.py" ]
