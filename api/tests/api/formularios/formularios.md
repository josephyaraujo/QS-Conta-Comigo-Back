## Endpoints Formulários
Para realizar os testes nos endpoints é preciso fazer o login pela API nas rotas de GET /auth/login/ para pegar a url de login no suap e depois o code gerado. Depois é necessário rodar o POST /auth/exchange/ passando o code e pegar na response o access token. Com o access token, inserimos ele no Authorization do Postman como Bearer Token.

### FORM-01 – Listar formulários (GET /api/formularios)
![alt text](img-1.png)

### FORM-02 – Criar formulário (POST /api/formularios/)
![alt text](img-2.png)

### FORM-03 – Atualizar formulário (PATCH /api/formularios/:id/)
![alt text](img-3.png)

### FORM-04 – Enviar formulário (POST /api/formularios/:id/envio/)
![alt text](img-4.png)

### FORM-05 – Enviar formulário com erros (POST /api/formularios/:id/envio/)
![alt text](img-5.png)

### FORM-06 – Estatísticas dos formulários (GET /api/formularios/estatisticas/)
![alt text](img-6.png)

### FORM-07 – Criar resposta de formulário (POST /api/resposta_formulario/)
![alt text](img-8.png)

### FORM-08 – Criar resposta de formulário com erros (POST /api/resposta_formulario/)
![alt text](img-9.png)

### FORM-09 – Consultar questão do formulário (GET /api/formulario_questao/)
![alt text](img-10.png)

### FORM-10 – Consultar opção de questão do formulário (GET /api/formulario_questao_opcao/)
![alt text](img-11.png)

### FORM-11 – Criar opção de questão do formulário (POST /api/formulario_questao_opcao/)
![alt text](img-12.png)

### FORM-12 – Atualizar opção de questão do formulário (PUT /api/formulario_questao_opcao/:id/)
![alt text](img-13.png)

### FORM-13 – Criar questão do formulário (POST /api/formulario_questao/)
![alt text](img-14.png)

### FORM-14 – Atualizar questão do formulário (PUT /api/formulario_questao/:id/)
![alt text](img-15.png)