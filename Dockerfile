# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (version 1.8.0+ supports PEP 621 [project] section)
RUN pip install poetry==2.1.2

# Configure Poetry
RUN poetry config virtualenvs.create false

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Set work directory
WORKDIR /app

# Copy Poetry files first for better caching
COPY pyproject.toml poetry.lock* ./

# Install dependencies (without installing the project itself)
RUN poetry install --only=main --no-interaction --no-root

# Copy source code
COPY . .

# Install the package
RUN poetry install --no-interaction

# Change ownership
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Create output directory
RUN mkdir -p /app/output

# Set default command
CMD ["egile-mcp-starter", "--help"]

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import egile_mcp_starter; print('OK')" || exit 1

# Add labels
LABEL maintainer="jpoullet2000@example.com" \
      description="Egile MCP Starter - A cookiecutter template for MCP servers" \
      version="0.1.0"
