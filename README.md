### Detalhes da aplicação

Tec:

```
- stack: mysql:8.0 | python:3.10 | djangorestframework
- static analysis: pylint | mypy
- Arch: MTV | events[rabbitmq]
```

Details:

- RabbitMq online provido por: https://www.cloudamqp.com
- Servidor de arquivos local: https://min.io

***

### Instalando aplicação

#### Requirements

``` 
- docker
- docker compose
```

1 - Subindo aplicação na porta `8000`

```shell
    docker compose up -d
```

2 - Instalando o banco de dados

```shell
    docker compose exec web python manage.py migrate
```

