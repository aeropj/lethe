# Lethe local POC: one container runs the device (with an on-device PII model), issuer, relay, gateway and lab adapter.
#   docker build -t lethe-demo .
#   docker run --rm -p 127.0.0.1:8787:8787 lethe-demo     then paste an OpenAI key at http://localhost:8787
# The key you paste stays in the container's memory. -e OPENAI_API_KEY still works as a preset.
# The model and the city data are baked in: after the pull, detection needs no network at all.

# ---------------------------------------------------------------- dependencies (CPU-only PyTorch)
FROM python:3.12-slim AS deps
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
RUN pip install --index-url https://download.pytorch.org/whl/cpu "torch>=2.5" \
 && pip install "gliner==0.2.29" "cryptography>=46,<47" "phonenumbers>=8.13" protobuf sentencepiece

# ---------------------------------------------------------------- model weights and GeoNames, fetched at build time
FROM deps AS data
ENV HF_HOME=/opt/hf
RUN python - <<'PY'
import io, urllib.request, zipfile, os
from huggingface_hub import snapshot_download
snapshot_download("urchade/gliner_multi_pii-v1")
snapshot_download("microsoft/mdeberta-v3-base", allow_patterns=["config.json", "tokenizer_config.json", "spm.model"])
os.makedirs("/opt/data", exist_ok=True)
base = "https://download.geonames.org/export/dump/"
zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(base + "cities15000.zip").read())).extractall("/opt/data")
for f in ("admin1CodesASCII.txt", "countryInfo.txt"):
    open(f"/opt/data/{f}", "wb").write(urllib.request.urlopen(base + f).read())
PY

# ---------------------------------------------------------------- the app
FROM deps
LABEL org.opencontainers.image.title="Lethe demo" \
      org.opencontainers.image.description="Ask OpenAI a personal question privately: an on-device model swaps names, places and IDs, the request is sealed, relayed and checked with a blind credential, and every step is traced." \
      org.opencontainers.image.source="https://github.com/aeropj/lethe" \
      org.opencontainers.image.authors="aeropj"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false \
    HF_HOME=/opt/hf HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
    LETHE_DATA=/opt/data LETHE_HOST=0.0.0.0 LETHE_PORT=8787
COPY --from=data /opt/hf /opt/hf
COPY --from=data /opt/data /opt/data
RUN useradd --create-home --uid 10001 lethe && chmod -R a+rX /opt/hf /opt/data
WORKDIR /app
COPY --chown=lethe:lethe server.py scrub.py detect.py lethe_crypto.py run_examples.py ./
COPY --chown=lethe:lethe static ./static
COPY --chown=lethe:lethe eval ./eval
USER lethe

EXPOSE 8787
HEALTHCHECK --interval=30s --timeout=3s --start-period=20s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8787/healthz', timeout=2)"
CMD ["python", "server.py"]
