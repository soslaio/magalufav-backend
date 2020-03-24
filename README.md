# Magalu - Favoritos

Backend REST da aplicação de favoritos do desafio Luiza Labs. Foram utilizadas as seguintes
tecnologias no desenvolvimento da solução:

1. **Python** como linguagem base;
2. **Django** como framework web base;
3. **Django Rest Framework** como framework para construção de REST APIs;
4. **JWT** como mecanismo de autenticação;
5. **Redis** como mecanismo de cache;
6. **Postgres** como banco de dados.

### Decisões arquiteturais

1. As informações dos produtos, que são oriundos de uma API externa, não são armazenados no banco de dados persistente;
2. A primeira vez que as informações de um produto são solicitadas, a consulta remota é executada e o resultado da mesma
é armazenado em cache. A partir daí, até que o cache expire, os dados do produto são sempre retornados de lá;
3. O tempo padrão do cache é de 1 dia, para que informações críticas como o preço não fiquem desatualizadas;
4. Considerando que pela regra de negócio as únicas informações do cliente armazenadas são nome e email, não foi possível
criar um mecanismo para que os clientes autentiquem para ter acesso às informações. O usuário e senha utilizados nos
exemplos (`admin` e `admin_pass`) são criados pelos scripts de inicialização da stack Docker. A criação de novos pode
ser feita através de interface administrativa do Django, mas não faz parte do escopo dessa API.

### Deploy com Docker

Para levantar a API, primeiramente é necessário obter os arquivos do sistema. Há duas opções para isso. A primeira é
fazer o download dos arquivos no endereço `https://github.com/soslaio/magalufav-backend/archive/master.zip`. Descompacte
e entre na pasta descompactada pelo terminal do seu sistema operacional.

A segunda opção é clonar os arquivos diretamente do repositório Git. Para isso você deve possuir o
[Git](https://git-scm.com/) instalado na sua máquina. Estando instalado, execute os seguintes comandos no terminal: 

    $ git clone https://github.com/soslaio/magalufav-backend.git
    $ cd magalufav-backend

Com os arquivos já baixados na máquina, o próximo passo é levantar o serviço através do Docker e executar os scripts de
inicialização do banco. Para isso foi criado um script, que pode ser executado digitando no terminal:

    $ chmod +x run.sh
    $ ./run.sh

Esse script baixa da internet todos as imagens dos serviços necessários para o funcionamento do sistema e faz também
toda a configuração do ambiente. A execução desse comando necessita de internet e pode ser um pouco demorado, dependendo
da máquina onde está sendo executado e da banda de internet disponível.

Após o término da execução, os endpoints da API já estão disponíveis para serem testados.

### Endpoints

Endpoints são endereços para acessar recursos na internet. Os seguintes endpoints são disponibilizados através deta API:

| HTTP Method | URI                                          | Ação
| ---         | ---                                          | ---
| POST        | http://[hostname]/token/                     | Obter o token JWT
| POST        | http://[hostname]/customers/                 | Criar um cliente
| GET         | http://[hostname]/customers/[uuid]           | Obter detalhes do cliente
| PUT         | http://[hostname]/customers/[uuid]           | Atualizar o cliente
| DELETE      | http://[hostname]/customers/[uuid]           | Remover o cliente
| POST        | http://[hostname]/favorites/                 | Criar um produto favorito
| GET         | http://[hostname]/customers/[uuid]/favorites | Obter produtos favoritos do cliente
| DELETE      | http://[hostname]/favorites/[uuid]           | Excluir um produto favorito

#### Exemplos de utilização

Segue exemplo de que dados enviar e o tipo de resposta dada pela API para requisições nos endpoints listados acima.
Para executar os exemplos é necessário possuir o programa [`curl`](https://curl.haxx.se/) e algum conhecimento de
requisições HTTP para fazer a adaptação dos comandos de acordo com as respostas geradas pelo sistema. Obviamente outros
clientes REST podem ser utilizados também, como o Postman, Insomnia, entre outros.

Note que, quando os comandos forem executados no terminal da sua máquina, as respostas serão diferentes. Isso acontece
principalmente com os tokens de autenticação e os identificadores dos recursos (customers, favorites), que são únicos e
gerados automaticamente pela API.

* **Obter o token JWT**

O token JWT é uma longa string que identifica o usuário logado a cada requisição efetuada. Esse token possui um tempo de
vida, e é válido apenas até que expire, sendo necessário gerar um novo através de uma nova consulta ou através da rota
de "refresh".

O tempo de vida do token configurado por padrão é de 1 hora, mas pode ser alterado através do parâmetro
`ACCESS_TOKEN_LIFETIME` presente no arquivo de configuração do Django. 

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

* **Criar um cliente**

O endpoint de criação do cliente implementa a regra de negócio que impede que um email seja cadastrado mais de uma vez
no banco de dados.

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
OBS: O `id` gerado será utilizado nos próximos comandos relacionados ao cliente.

* **Obter detalhes do cliente**

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

* **Atualizar o cliente**

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

* **Remover o cliente**

Remove o cliente e todos os favoritos que ele possui do banco de dados.

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

* **Criar um produto favorito**

O endpoint de criação de um favorito implementa a regra de negócio que impede que um mesmo produto seja adicionado mais
de uma vez para o mesmo cliente e a regra que impede que um produto inexistente seja incluído.

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

* **Obter produtos favoritos do cliente**

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

* **Excluir um produto favorito**

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

* **PAGE_SIZE**: Número de registros que são exibidos na paginação dos resultados;
* **CACHE_TIMEOUT**: Número de segundos que o Redis mantém as informações de um produto em cache;
* **ACCESS_TOKEN_LIFETIME**: Número de segundos  de validade do token JWT enviado para o cliente. Ao fim desse tempo o
token expira e é necessário fazer um refresh do token;
* **REFRESH_TOKEN_LIFETIME**: Número de segundos de validade do token JWT utilizado para fazer o refresh do token de
acesso.

#### Variáveis de ambiente

Há variáveis de ambiente que podem ser alteradas no arquivo `stack.yml`. São basicamente configurações de conexão com o
banco de dados e com o sistema de cache. Não é necessário alterar essas variáveis, já que são ajustadas para funcionar
dentro da stack do Docker, mas há essa possibilidade, caso seja utilizada dentro de outros contextos.

* DB_HOST: Host do banco de dados;
* DB_NAME: Nome do banco de dados;
* DB_USER: Usuário de acesso ao banco de dados;
* DB_PASS: Senha do usuário de acesso ao banco de dados;
* DB_PORT: Porta de conexão com o banco de dados;
* REDIS_HOST: Host do servidor de cache Redis;
* REDIS_PORT: Porta de conexão com o servidor de cache Redis.

