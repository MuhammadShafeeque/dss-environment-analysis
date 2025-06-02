# Use official slim Python base image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential git

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Set default working directory
WORKDIR /workspace/elapse-compare
