# Start from the python:3.8-slim-buster base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Update and install ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    curl \
    software-properties-common \
    git

# Install Python dependencies
COPY requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app.py ./app.py

# Set the Streamlit configuration
ENV STREAMLIT_SERVER_PORT=8501

# When the container starts, run the main.py script
CMD ["streamlit", "run", "app.py"]
