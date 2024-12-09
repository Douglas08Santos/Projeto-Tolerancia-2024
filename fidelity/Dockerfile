# Use uma imagem base do Python
FROM python:3.12-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação
COPY . .

# Exponha a porta apropriada (substitua 5000 pela porta correta para cada serviço)
EXPOSE 5000

# Comando para rodar a aplicação (substitua app.py pelo nome correto do arquivo para cada serviço)
CMD ["python", "fidelity.py"]