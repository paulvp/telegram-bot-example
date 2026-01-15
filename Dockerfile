# Multi-stage build for optimized image size
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage - minimal runtime image
FROM python:3.11-alpine

# Install runtime dependencies only
RUN apk add --no-cache \
    libffi \
    openssl \
    bash \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY bot.py .
COPY monitor.sh .
COPY .env .

# Make monitor script executable
RUN chmod +x /app/monitor.sh

# Create logs directory
RUN mkdir -p /app/logs

# Update PATH
ENV PATH=/root/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pgrep -f "python bot.py" || exit 1

# Run bot with monitor script
CMD ["/app/monitor.sh"]
