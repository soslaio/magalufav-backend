
FROM python:3.7-slim-buster

# Atualizações do sistema.
RUN apt-get -y update
RUN apt-get -y upgrade

# Copia os arquivos necessários para a construção da imagem.
COPY magalufav /opt/api
COPY requirements.txt /opt/api/requirements.txt

# Instala os módulos python requeridos para a aplicação.
WORKDIR /opt/api/
RUN pip install -r requirements.txt

WORKDIR /opt/api/
