# Builder stage
FROM python:3.12.0 as builder
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Final stage
FROM python:3.12.0-slim
WORKDIR /app

# Install dependencies again in slim image
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY --from=builder /app /app

# Create a non-privileged user
RUN useradd -m myuser && chown -R myuser /app
USER myuser

EXPOSE 5004
ENV FLASK_TEMPLATE_FOLDER=/app/templates

CMD ["python", "upload-song-app.py"]
