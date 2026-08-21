## Endpoints Cursos
Para realizar os testes nos endpoints é preciso fazer o login pela API nas rotas de GET /auth/login/ para pegar a url de login no suap e depois o code gerado. Depois é necessário rodar o POST /auth/exchange/ passando o code e pegar na response o access token. Com o access token, inserimos ele no Authorization do Postman como Bearer Token.

![alt text](image.png)

### CUR-01 – Listar cursos autenticado
![alt text](image-1.png)

### CUR-02 – Listar cursos sem autenticação
![alt text](image-4.png)

### CUR-03 – Consultar curso existente
![alt text](image-2.png)

### CUR-04 – Consultar curso inexistente
![alt text](image-3.png)

### CUR-05 – Criar curso válido
#### Para criar o curso ele precisa estar inserido no dicionário
![alt text](image-5.png)

### CUR-06 – Criar curso sem nome
#### Body da requisição 
```json
{
    "nome":""
}
```
![alt text](image-6.png)

### CUR-07 – Atualizar curso existente
#### Para atualizar o curso ele precisa estar inserido no dicionário
![alt text](image-7.png)
