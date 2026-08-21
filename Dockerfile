FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED 1

# --- Cria usuário não-root 'vscode' ---
RUN apt-get update && apt-get install -y sudo && rm -rf /var/lib/apt/lists/*
RUN groupadd --gid 1000 vscode
RUN useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home vscode
RUN usermod -aG sudo vscode
RUN echo vscode ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/vscode && chmod 0440 /etc/sudoers.d/vscode
# --- FIM ---

# Instala o Git e outras ferramentas essenciais
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /api

# Copia apenas requirements.txt para instalar dependências durante o build.
# O código da aplicação NÃO é copiado — será mapeado da máquina host em tempo de execução.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Declare o diretório /api como ponto de montagem (opcional, ajuda ferramentas a detectar intenção)
VOLUME ["/api"]

# Não copiar o código da aplicação; o código deverá ser montado pelo host:
#  docker run -v /caminho/na/maquina:/api <imagem> ...
# ou via docker-compose com bind mount

# Continua executando como usuário não-root
USER vscode

CMD ["bash"]