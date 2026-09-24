FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN python -m pip install --no-cache-dir . \
    && useradd --system --uid 10001 --create-home mcp \
    && rm -rf /root/.cache/pip

USER 10001:10001
ENTRYPOINT ["clinical-calc-mcp"]
