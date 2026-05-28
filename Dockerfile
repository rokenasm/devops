# python:3.11-slim chosen over the full image (~50MB vs ~1GB) and over
# alpine (pip wheels are easier on glibc).
FROM python:3.11-slim

WORKDIR /app

# Requirements copied first so the pip install layer is cached across rebuilds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY tests ./tests

# Default command runs the demo CLI so a `docker run` produces visible
# evidence the validator works inside the image.
CMD ["python", "-m", "src.app"]
