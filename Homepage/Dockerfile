# Builder stage
FROM python:3.12.0 as builder
WORKDIR /app

# Install dependencies in a single layer to reduce image size
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code to the builder stage
COPY . .

# Final stage
FROM python:3.12.0-slim
WORKDIR /app

# Copy built application from builder stage
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Create a non-privileged user for running the application
RUN useradd -m myuser && chown -R myuser /app
USER myuser

# Expose the port the app runs on
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_TEMPLATE_FOLDER=/app/templates

# Command to run the Flask app
CMD ["python", "app.py"]
