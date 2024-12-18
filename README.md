# Projeto-Tolerancia-2024

## Tecnologias Utilizadas
- Python
- Docker
  - Dockerfile
  - Compose
- RabbitMQ

## Serviços principais

- ecommerce
  - Serviço principal que coordena as compras.
- exchange
  - Responsável de realizar conversão de preço USD -> BRL baseado na cotação mais recente.
- fidelity
  - Faz a bonificação de pontos dos usuários baseadas em suas compras.
- store
  - Gerencia o estoque de produtos
- subscribe_fidelity

## Rotas de ações

- ecommerce
  - rota: <http://localhost:5050>
    - ação: '/buy' (POST)
      - parâmetro: json { "product" : int, "user" : int, "ft": int}

- store
  - rota: <http://localhost:5001>
  - ação: '/product' (GET)
    - retorno: json

- exchange
  - exchange-1
    - rota: <http://localhost:5011>
  - exchange-2
    - rota: <http://localhost:5012>
  - ação: '/exchange' (GET)

- fidelity
  - rota: <http://localhost:5003>

- RabbitMQ
  - rota: <http://localhost:5672>

## MISC

- RabbitMQ
  - ManagementUI
    - <http://localhost:15672>
    - login: guest
    - pwd: guest
