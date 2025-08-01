# Multi-stage build for Playwright Python framework
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy the entire framework
COPY . .

# Create test file directories
RUN mkdir -p uploaded_test_files reports screenshots

# Set permissions
RUN chmod +x scripts/*.sh 2>/dev/null || true

# Production stage
FROM base as production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import playwright; print('Playwright ready')" || exit 1

# Default command
CMD ["python", "-m", "pytest", "tests/", "-v", "--headless"]

# Development stage
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir pytest-xdist pytest-html pytest-json-report

# Expose port for debugging
EXPOSE 9222

# Development command with more verbose output
CMD ["python", "-m", "pytest", "tests/", "-v", "--headless", "--html=reports/report.html", "--json-report", "--json-report-file=reports/report.json"] 