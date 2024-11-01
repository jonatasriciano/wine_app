# Usa uma imagem base Python
FROM python:3.9-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Instala as dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y wait-for-it

# Copia o código do projeto para o contêiner
COPY . .

# Comando de inicialização
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]