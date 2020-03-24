# Magalu - Favoritos
Backend REST da aplicação de favoritos do desafio Luiza Labs. Foram utilizadas as seguintes
tecnologias no desenvolvimento da solução:

* **Python** como linguagem base
* **Django** como framework web base
* **Django Rest Framework** como framework para construção de REST APIs
* **JWT** como mecanismo de autenticação
* **Redis** como mecanismo de cache
* **Postgres** como banco de dados

### Deploy com Docker

Para levantar a API, primeiramente é necessário obter os arquivos do sistema. Há duas opções para isso. A primeira é
fazer o download dos arquivos no endereço `https://github.com/soslaio/magalufav-backend/archive/master.zip`. Descompacte
e entre na pasta pelo terminal do seu sistema operacional.

A segunda opção é clonar os arquivos diretamente do repositório Git. Para isso você deve possuir o Git instalado na sua
máquina. Estando instalado, execute os seguintes comandos no terminal: 

    $ git clone https://github.com/soslaio/magalufav-backend.git
    $ cd magalufav-backend

Com os arquivos já baixados na máquina, o próximo passo é levantar o serviço através do Docker. Isso pode ser feito
através do terminal, digitando o seguinte comando:

    $ sudo docker-compose -f stack.yml up

Esse comando baixa da internet todos as imagens dos serviços necessários para o funcionamento do sistema e faz também
toda a configuração necessária. A execução desse comando necessita de internet e pode ser um pouco demorado, dependendo
da máquina onde está sendo executado e da banda de internet disponível.

Após o término da execução, a API já está disponível no endereço `http://localhost:81`.

### Endpoints

| HTTP Method | URI                                          | Ação
| ---         | ---                                          | ---
| POST        | http://[hostname]/token/                     | Obtém o token JWT
| POST        | http://[hostname]/customers/                 | Cria um cliente
| GET         | http://[hostname]/customers/[uuid]           | Detalhes do cliente
| PUT         | http://[hostname]/customers/[uuid]           | Atualiza o cliente
| DELETE      | http://[hostname]/customers/[uuid]           | Remove o cliente
| POST        | http://[hostname]/favorites/                 | Cria um produto favorito
| GET         | http://[hostname]/customers/[uuid]/favorites | Produtos favoritos do cliente
| DELETE      | http://[hostname]/favorites/[uuid]           | Exclui um produto favorito

#### Exemplos
Segue exemplo de que dados enviar e o tipo de resposta dada pela API para requisições nos endpoints listados acima.
Para executar os exemplos é necessário possuir o programa `curl`.

* **Obtém o token JWT** 

Comando:

    $ curl -i -H "Content-Type: application/json" -X POST -d '{ "username": "admin", "password": "admin_pass" }' http://localhost/token/

Resposta:

```
HTTP/1.1 200 OK
Server: gunicorn/20.0.4
Date: Mon, 23 Mar 2020 23:12:18 GMT
Connection: close
Content-Type: application/json
Vary: Accept
Allow: POST, OPTIONS
X-Frame-Options: DENY
Content-Length: 438
X-Content-Type-Options: nosniff

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4NTA4NzkyMSwianRpIjoiNGYzYWYyNTdlMmMzNDM4OGJjZjQ1ZWM1NDc2M2E2NmIiLCJ1c2VyX2lkIjoxfQ.Qq2k7C9etrqzCgHy2yWTNFZC6TBOeUvsCX6f3A0akQY",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg1MDA1MTIxLCJqdGkiOiIzNDA0NGUyZTY4NTg0ODUyODZlMzA4NmYwMGFhNDVlYiIsInVzZXJfaWQiOjF9.p5fNmBjInzF2_XKfY940Yuc_zmZAG8dHPKbBxaMTx5k"
}
```
OBS: O token retornado no atributo `access` será utilizado no cabeçalho das próximas requisições.

* **Cria um cliente**

Comando:

    $ curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg1MDA5OTc0LCJqdGkiOiJlZDVlNWVjZjIyZDE0YTVmODcwNWRkZDE3NTkzZWJhMyIsInVzZXJfaWQiOjF9.RhrlIFn7EGdNiWurlwL0Pr2JWqBlQwzBjMbtLqlPk_Q" -X POST -d '{ "name": "José da Silva", "email": "jose@silvacorp.com" }' http://localhost/customers/

Resposta:

```
HTTP/1.1 201 Created
Server: gunicorn/20.0.4
Date: Mon, 23 Mar 2020 23:38:18 GMT
Connection: close
Content-Type: application/json
Vary: Accept
Allow: POST, OPTIONS
X-Frame-Options: DENY
Content-Length: 98
X-Content-Type-Options: nosniff

{
   "id":"9af3de6c-8ea5-4c26-a3fd-03253afd50a5",
   "name":"José da Silva",
   "email":"jose@silvacorp.com"
}
```
OBS: O `id` gerado para o cliente será utilizado nos próximos comandos relacionados ao cliente.

* **Detalhes do cliente**

Comando:

    $ curl -i -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg1MDA5OTc0LCJqdGkiOiJlZDVlNWVjZjIyZDE0YTVmODcwNWRkZDE3NTkzZWJhMyIsInVzZXJfaWQiOjF9.RhrlIFn7EGdNiWurlwL0Pr2JWqBlQwzBjMbtLqlPk_Q" http://localhost/customers/9af3de6c-8ea5-4c26-a3fd-03253afd50a5/

Resposta:

```
HTTP/1.1 200 OK
Server: gunicorn/20.0.4
Date: Mon, 23 Mar 2020 23:48:39 GMT
Connection: close
Content-Type: application/json
Vary: Accept
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 98
X-Content-Type-Options: nosniff

{
   "id":"9af3de6c-8ea5-4c26-a3fd-03253afd50a5",
   "name":"José da Silva",
   "email":"jose@silvacorp.com"
}
```

* **Atualiza o cliente**

Comando:

    $ curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg1MDA5OTc0LCJqdGkiOiJlZDVlNWVjZjIyZDE0YTVmODcwNWRkZDE3NTkzZWJhMyIsInVzZXJfaWQiOjF9.RhrlIFn7EGdNiWurlwL0Pr2JWqBlQwzBjMbtLqlPk_Q" -X PUT -d '{ "name": "José da Silva Silva", "email": "jose@silvacorp.com" }' http://localhost/customers/9af3de6c-8ea5-4c26-a3fd-03253afd50a5/

Resposta:

```
HTTP/1.1 200 OK
Server: gunicorn/20.0.4
Date: Mon, 23 Mar 2020 23:53:49 GMT
Connection: close
Content-Type: application/json
Vary: Accept
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 104
X-Content-Type-Options: nosniff

{
   "id":"9af3de6c-8ea5-4c26-a3fd-03253afd50a5",
   "name":"José da Silva Silva",
   "email":"jose@silvacorp.com"
}
```

* **Remove o cliente**

Comando:

    $ curl -i -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg1MDA5OTc0LCJqdGkiOiJlZDVlNWVjZjIyZDE0YTVmODcwNWRkZDE3NTkzZWJhMyIsInVzZXJfaWQiOjF9.RhrlIFn7EGdNiWurlwL0Pr2JWqBlQwzBjMbtLqlPk_Q" -X DELETE http://localhost/customers/9af3de6c-8ea5-4c26-a3fd-03253afd50a5/

Resposta:

```
HTTP/1.1 204 No Content
Server: gunicorn/20.0.4
Date: Mon, 23 Mar 2020 23:58:49 GMT
Connection: close
Vary: Accept
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 0
X-Content-Type-Options: nosniff
```

* **Cria um produto favorito**

Comando:

    $ curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg1MDA5OTc0LCJqdGkiOiJlZDVlNWVjZjIyZDE0YTVmODcwNWRkZDE3NTkzZWJhMyIsInVzZXJfaWQiOjF9.RhrlIFn7EGdNiWurlwL0Pr2JWqBlQwzBjMbtLqlPk_Q" -d '{ "product_id": "a96b5916-9109-5d2e-138a-7b656efe1f92", "customer": "d705e535-d31a-48b9-9bd7-c193053b5f82" }' -X POST http://localhost/favorites/

Resposta:

```
HTTP/1.1 201 Created
Server: gunicorn/20.0.4
Date: Tue, 24 Mar 2020 00:03:50 GMT
Connection: close
Content-Type: application/json
Vary: Accept
Allow: POST, OPTIONS
X-Frame-Options: DENY
Content-Length: 147
X-Content-Type-Options: nosniff

{
   "id":"520ef1fd-7462-4fb9-9522-5c9c7af9d7e0",
   "product_id":"a96b5916-9109-5d2e-138a-7b656efe1f92",
   "customer":"d705e535-d31a-48b9-9bd7-c193053b5f82"
}
```

* **Produtos favoritos do cliente**

Comando:

    $ curl -i -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg1MDA5OTc0LCJqdGkiOiJlZDVlNWVjZjIyZDE0YTVmODcwNWRkZDE3NTkzZWJhMyIsInVzZXJfaWQiOjF9.RhrlIFn7EGdNiWurlwL0Pr2JWqBlQwzBjMbtLqlPk_Q" http://localhost/customers/d705e535-d31a-48b9-9bd7-c193053b5f82/favorites/

Resposta:

```
HTTP/1.1 200 OK
Server: gunicorn/20.0.4
Date: Tue, 24 Mar 2020 00:07:37 GMT
Connection: close
Content-Type: application/json
Vary: Accept
Allow: GET, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 366
X-Content-Type-Options: nosniff

{
   "meta":{
      "page_number":1,
      "page_size":100
   },
   "results":[
      {
         "id":"520ef1fd-7462-4fb9-9522-5c9c7af9d7e0",
         "title":"The Walking Dead - Season 2 para PS3",
         "image":"http://challenge-api.luizalabs.com/images/a96b5916-9109-5d2e-138a-7b656efe1f92.jpg",
         "price":129.9,
         "link":"http://challenge-api.luizalabs.com/api/product/a96b5916-9109-5d2e-138a-7b656efe1f92",
         "reviewScore":null
      }
   ]
}
```

* **Exclui um produto favorito**

Comando:

    curl -i -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg1MDA5OTc0LCJqdGkiOiJlZDVlNWVjZjIyZDE0YTVmODcwNWRkZDE3NTkzZWJhMyIsInVzZXJfaWQiOjF9.RhrlIFn7EGdNiWurlwL0Pr2JWqBlQwzBjMbtLqlPk_Q" -X DELETE http://localhost/favorites/520ef1fd-7462-4fb9-9522-5c9c7af9d7e0/

Resposta:

```
HTTP/1.1 204 No Content
Server: gunicorn/20.0.4
Date: Tue, 24 Mar 2020 00:10:47 GMT
Connection: close
Vary: Accept
Allow: DELETE, OPTIONS
X-Frame-Options: DENY
Content-Length: 0
X-Content-Type-Options: nosniff
```

### Parâmetros
#### Django
No arquivo de configuração do Django localizado em `magalufav/magalufav/settings.py` há alguns parâmetros definidos que
podem ser mudados conforme o cenário de execução da aplicação e conveniência. São eles:

* **PAGE_SIZE**: Número de registros que são exibidos na paginação dos resultados.
* **CACHE_TIMEOUT**: Número de segundos que o Redis mantém as informações de um produto
em cache.
* **ACCESS_TOKEN_LIFETIME**: Número de segundos  de validade do token JWT enviado para o cliente.
Ao fim desse tempo o tokem expira e é necessário fazer um refresh do token.
* **REFRESH_TOKEN_LIFETIME**: Número de segundos de validade do token JWT utilizado para fazer o
refresh do token de acesso.

#### Variáveis de ambiente
Há variáveis de ambiente que podem ser alteradas no arquivo `stack.yml`.
