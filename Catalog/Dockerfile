# Builder stage
FROM python:3.12.0 as builder
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Final stage
FROM python:3.12.0-slim
WORKDIR /app

# Copy built application from builder stage
COPY --from=builder /app /app

# Ensure all necessary packages are installed, including pytest
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pytest

# Debugging: Print PATH and check if pytest is installed
RUN echo $PATH
RUN which pytest || true
RUN ls -la /usr/local/bin/

# Copy tests directory
COPY tests /app/tests

# Create a non-privileged user
RUN useradd -m myuser && chown -R myuser /app
USER myuser

# Expose the application port
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_TEMPLATE_FOLDER /app/templates

# Start the application
CMD ["python", "catalog-app.py"]
