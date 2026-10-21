# Lethe local POC: one container runs the device, issuer, relay, gateway and lab adapter.
#   docker build -t lethe-demo .
#   docker run --rm -p 127.0.0.1:8787:8787 -e OPENAI_API_KEY -e LETHE_OPENAI_STORE=1 lethe-demo
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LETHE_HOST=0.0.0.0 \
    LETHE_PORT=8787

RUN pip install --no-cache-dir "cryptography>=46,<47" \
 && useradd --create-home --uid 10001 lethe

WORKDIR /app
COPY --chown=lethe:lethe server.py scrub.py lethe_crypto.py run_examples.py ./
COPY --chown=lethe:lethe static ./static
USER lethe

EXPOSE 8787
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8787/healthz', timeout=2)"
CMD ["python", "server.py"]
