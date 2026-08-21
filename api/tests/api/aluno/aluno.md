## Endpoints Aluno 
Para realizar os testes nos endpoints é preciso fazer o login pela API nas rotas de GET /auth/login/ para pegar a url de login no suap e depois o code gerado. Depois é necessário rodar o POST /auth/exchange/ passando o code e pegar na response o access token. Com o access token, inserimos ele no Authorization do Postman como Bearer Token.
![alt text](image.png)

### AL-01 – Listar alunos autenticado
![alt text](image-1.png)
### AL-02 – Listar alunos sem autenticação
![alt text](image-2.png)
### AL-03 – Criar aluno com dados válidos 
![alt text](image-3.png)
### AL-04 – Criar aluno com dados inválidos
![alt text](image-4.png)
### AL-05 – Atualizar aluno existente
![alt text](image-5.png)
### AL-06 – Atualizar aluno inexistente
![alt text](image-6.png)
### AL-07 – Deletar aluno existente
![alt text](image-7.png)
### AL-08 – Deletar aluno inexistente
![alt text](image-8.png)
### AL-09 – Lista aluno pelo id existente
![alt text](image-9.png)
### AL-10 – Lista aluno pelo id inexistente
![alt text](image-10.png)

