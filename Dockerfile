FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Docker CLI and Node.js
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl gnupg lsb-release && \
    # Install Docker CLI
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    # Install Node.js and npm
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli nodejs && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy files needed for installation
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Run as non-root user for better security
RUN useradd -m mcpo && \
    chown -R mcpo:mcpo /app
USER mcpo

# Set environment variables
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Default command - can be overridden via docker-compose or docker run
ENTRYPOINT ["mcpo"]
CMD ["--host", "0.0.0.0", "--port", "8000"]
