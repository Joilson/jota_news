### Detalhes da aplicação

Tec:

```
- stack: mysql:8.0 | python:3.10 | djangorestframework
- static analysis: pylint | mypy
- Arch: MTV | events[rabbitmq]
```

Detalhes:

- RabbitMq online provido por: https://www.cloudamqp.com
- Servidor de arquivos local pelo docker: https://min.io

Microsserviços Async:

Ao criar uma nova noticia o signals do Django lança o `post_save`
que é capturado pelo `send_to_other_projects` em um exchange do
tipo `fanout` para que possa ser capturado por 1 ou mais projetos(microsservices)
que podem ser responsaveis por enviar notificações ou realizar auditorias...

Microsserviços:
- Auditor: https://github.com/Joilson/jota_news_auditor
- Notifications: https://github.com/Joilson/jota_news_notifications

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

2 - Copie o .env.example para .env

```shell
    cp .env.example .env
```

3 - Instalando o banco de dados

```shell
    docker compose exec web python manage.py migrate
```

