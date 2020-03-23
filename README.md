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
| POST        | http://[hostname]/customers/                 | Cria um cliente
| GET         | http://[hostname]/customers/[uuid]           | Detalhes do cliente
| PUT         | http://[hostname]/customers/[uuid]           | Atualiza o cliente
| DELETE      | http://[hostname]/customers/[uuid]           | Remove o cliente
| GET         | http://[hostname]/customers/[uuid]/favorites | Produtos favoritos do cliente
| POST        | http://[hostname]/favorites/                 | Cria um produto favorito
| DELETE      | http://[hostname]/favorites/[uuid]           | Exclui um produto favorito
| POST        | http://[hostname]/token/                     | Obtém o token JWT
| POST        | http://[hostname]/token/refresh/             | Renova o token JWT


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
