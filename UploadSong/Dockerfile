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

# Copy built application from builder stage
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Create a non-privileged user
RUN useradd -m myuser && chown -R myuser /app
USER myuser

# Expose the application port
EXPOSE 5004

# Set environment variable for Flask
ENV FLASK_TEMPLATE_FOLDER /app/templates

# Start the application
CMD ["python", "upload-song-app.py"]
