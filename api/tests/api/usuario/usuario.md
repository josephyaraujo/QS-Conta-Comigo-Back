## Endpoints Usuario 
Para realizar os testes nos endpoints é preciso fazer o login pela API nas rotas de GET /auth/login/ para pegar a url de login no suap e depois o code gerado. Depois é necessário rodar o POST /auth/exchange/ passando o code e pegar na response o access token. Com o access token, inserimos ele no Authorization do Postman como Bearer Token.
![alt text](image.png)

### US-01 – Listar usuários com sucesso
![alt text](image-1.png)
### US-02 – Listar usuários sem autenticação
![alt text](image-2.png)
### US-03 – Criar usuário com dados válidos
![alt text](image-3.png)
### US-04 – Criar usuário com dados inválidos (campos obrigatórios faltando)
![alt text](image-4.png)
### US-05 – Criar usuário com email/username duplicado
![alt text](image-5.png)
### US-06 – Lista usuário pelo id existente
![alt text](image-6.png)
### US-07 – Lista usuário pelo id inexistente
![alt text](image-7.png)