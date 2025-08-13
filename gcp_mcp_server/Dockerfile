FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    UV_VERSION=0.1.12 \
    PORT=8001

# Install uv
RUN pip install --no-cache-dir uv==${UV_VERSION}

# Set working directory
WORKDIR /app

# Copy only the requirements file first
COPY pyproject.toml ./

# Set up virtualenv and install dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip compile pyproject.toml -o requirements.txt && \
    uv pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE ${PORT}

# Command to run the application
CMD [".venv/bin/python", "server.py"]
