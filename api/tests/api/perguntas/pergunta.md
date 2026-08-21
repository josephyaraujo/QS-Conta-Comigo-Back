## Endpoints Perguntas 
Para realizar os testes nos endpoints é preciso fazer o login pela API nas rotas de GET /auth/login/ para pegar a url de login no suap e depois o code gerado. Depois é necessário rodar o POST /auth/exchange/ passando o code e pegar na response o access token. Com o access token, inserimos ele no Authorization do Postman como Bearer Token.
![alt text](image-3.png)


### PE-01 – Assistente social tenta criar pergunta
![alt text](image-1.png)
### PE-02 – Assistente social logada ver todas perguntas
![alt text](image-2.png)
### PE-03 – Assistente social (não é aluno) tenta acessar suas próprias perguntas
![alt text](image-3.png)
### PE-04 – Assinste social tenta responder pergunta existente com status de 'nao_respondida'
![alt text](image-4.png)
### PE-05 – Assinste social tenta responder pergunta existente com status de 'respondida'
![alt text](image-5.png)
### PE-06 – Assinste social tenta responder pergunta inexistente
![alt text](image-6.png)
### PE-07 – Assistente social autenticada responder pergunta com dados inválidos
![alt text](image-7.png)

### PE-08 – Aluno autenticado cria pergunta com dados válidos
![alt text](image-9.png)
### PE-09 – Aluno autenticado ver minhas perguntas
![alt text](image-8.png)
### PE-10 – Aluno autenticado cria pergunta com dados inválidos (campos obrigatórios faltando)
![alt text](image-10.png)
### PE-12 – Aluno tenta responder pergunta
![alt text](image-11.png)
### PE-12 – Aluno autenticado com filtro ?respondida=true retorna apenas perguntas respondidas
![alt text](image-12.png)
### PE-13 – Aluno autenticado com filtro ?respondida=false retorna apenas perguntas não respondidas
![alt text](image-13.png)
### PE-14 – Aluno sem perguntas cadastradas gera 404
![alt text](image-14.png)

### PE-15 – Usuário não autenticado tenta responder pergunta
![alt text](image-15.png)
### PE-16 – Usuário não autenticado tenta criar pergunta
![alt text](image-16.png)
### PE-17 – Usuário não autenticado tenta acessar suas próprias perguntas
![alt text](image-17.png)


