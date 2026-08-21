## Endpoints Auxílios 
Para realizar os testes nos endpoints é preciso fazer o login pela API nas rotas de GET /auth/login/ para pegar a url de login no suap e depois o code gerado. Depois é necessário rodar o POST /auth/exchange/ passando o code e pegar na response o access token. Com o access token, inserimos ele no Authorization do Postman como Bearer Token.

![alt text](aux.png)

### GET Listar Auxílios
![alt text](aux1.png)

### GET Listar Auxílios (list)
![alt text](aux2.png)

### POST Criar Auxílios
![alt text](aux3.png)

### GET Buscar Auxílio por ID
![alt text](aux4.png)

### PUT Atualizar Auxílio
![alt text](aux5.png)

### PATCH Atualizar Parcial Auxílio
![alt text](aux6.png)

### DELETE Auxílio
![alt text](aux7.png)

### GET Auxílio Inexistente
![alt text](aux8.png)