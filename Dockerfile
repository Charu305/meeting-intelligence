FROM python:3.11-slim

WORKDIR /app

# Install ffmpeg for audio processing
RUN apt-get update && \
    apt-get install -y ffmpeg libsndfile1 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download Whisper model during build (not at runtime)
RUN python -c "from faster_whisper import WhisperModel; WhisperModel('tiny', compute_type='int8')"

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]