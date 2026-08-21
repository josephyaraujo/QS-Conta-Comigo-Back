## Endpoints Chamados
Para realizar os testes nos endpoints é preciso fazer o login pela API nas rotas de GET /auth/login/ para pegar a url de login no suap e depois o code gerado. Depois é necessário rodar o POST /auth/exchange/ passando o code e pegar na response o access token. Com o access token, inserimos ele no Authorization do Postman como Bearer Token.

![alt text](cham.png)

### GET Listar Chamados
![alt text](cham1.png)

## POST Criar Chamados
![alt text](cham2.png)

### GET Buscar Chamado por ID
![alt text](cham3.png)

### PUT Atualizar Chamado
![alt text](cham4.png)

### PATCH Atualizar Parcial Chamado
![alt text](cham5.png)

### DELETE Chamado
![alt text](cham6.png)

### GET Chamado Inexistente
![alt text](cham7.png)

### GET Chamados Sem Autenticação
![alt text](cham8.png)