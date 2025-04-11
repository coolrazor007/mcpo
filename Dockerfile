FROM python:3.12-slim-bookworm

# Create mcpo user and group
RUN groupadd -r mcpo && useradd -r -g mcpo mcpo

# Install uv (from official binary), nodejs, npm, and git
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Add mcpo user to docker group
RUN usermod -aG docker mcpo

# Install Node.js and npm via NodeSource 
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Confirm npm and node versions (optional debugging info)
RUN node -v && npm -v

# Copy your mcpo source code (assuming in src/mcpo)
COPY . /app
WORKDIR /app

# Set proper ownership
RUN chown -R mcpo:mcpo /app

# Create virtual environment explicitly in known location
ENV VIRTUAL_ENV=/app/.venv
RUN uv venv "$VIRTUAL_ENV" && chown -R mcpo:mcpo "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create and set permissions for cache directory
RUN mkdir -p /home/mcpo/.cache && chown -R mcpo:mcpo /home/mcpo

# Install mcpo (assuming pyproject.toml is properly configured)
RUN uv pip install . && rm -rf ~/.cache

# Verify mcpo installed correctly
RUN which mcpo

# Switch to mcpo user at runtime via docker-compose

# Expose port (optional but common default)
EXPOSE 8000

# Entrypoint set for easy container invocation
ENTRYPOINT ["mcpo"]

# Default command will be overridden by docker-compose
CMD ["--help"]
