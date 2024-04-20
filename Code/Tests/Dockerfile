FROM python:3.7-slim

RUN apt-get update && \
    apt-get install -y portaudio19-dev python3-pyaudio && \
    pip install pyaudio numpy matplotlib soundfile PyQt5

WORKDIR /app
COPY AudioFiles /app

CMD ["python", "./SmartMixer.py"]
