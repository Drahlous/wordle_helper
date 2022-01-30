FROM python:3.8.0-slim as builder
RUN apt-get update && apt-get install -y --reinstall wamerican && apt-get clean

COPY . /app

FROM python:3.8.0-slim as runner
COPY --from=builder /usr/share/dict/words /usr/share/dict/words
COPY --from=builder /app/get_words.sh /app/get_words.sh
COPY --from=builder /app/simulate_game.py /app/simulate_game.py
COPY --from=builder /app/wordle_helper.py /app/wordle_helper.py

WORKDIR app

CMD [ "python3", "/app/simulate_game.py" ]
