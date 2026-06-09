FROM python:3.11-slim
LABEL description="Netflix EDA — Reproduction of Kanigara (2021)"
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    git \
    wget \
    && ARCH="$(dpkg --print-architecture)" \
    && wget -q "https://github.com/quarto-dev/quarto-cli/releases/download/v1.5.57/quarto-1.5.57-linux-${ARCH}.deb" -O quarto.deb \
    && apt-get install -y --no-install-recommends ./quarto.deb \
    && rm quarto.deb \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -e ".[report]"
CMD ["make", "report"]
