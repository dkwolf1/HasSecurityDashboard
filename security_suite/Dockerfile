ARG BUILD_FROM
FROM $BUILD_FROM

# Set environment
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VENV_PATH=/opt/venv

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    bash \
    curl \
    nmap \
    iputils \
    net-tools

# Create virtual environment
RUN python3 -m venv $VENV_PATH

# Install Python dependencies in virtual environment
RUN $VENV_PATH/bin/pip install --no-cache-dir --upgrade pip && \
    $VENV_PATH/bin/pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    python-multipart \
    jinja2 \
    aiofiles \
    python-nmap \
    requests \
    ssl-checker \
    cryptography \
    python-whois \
    ipaddress

# Create app directory
WORKDIR /app

# Copy application files
COPY app/ /app/
COPY run.sh /app/run.sh

# Make scripts executable
RUN chmod +x /app/run.sh

# Create non-root user
RUN addgroup -g 8080 app && \
    adduser -D -s /bin/sh -u 8080 -G app app

# Change ownership
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose port
EXPOSE 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8081/api/health || exit 1

# Start command
CMD ["/app/run.sh"]
