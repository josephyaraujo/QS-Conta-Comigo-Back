# Para logar como AS
Agora existe um atalho no projeto para alternar entre AS e Aluno sem mexer manualmente no banco.

Use o comando na raiz do projeto:

```bash
./cli
```

Ele vai pedir o perfil desejado e o e-mail retornado pelo SUAP. Depois disso, faça o login via SUAP novamente para o backend popular o vínculo correto.

Se preferir, também dá para usar argumentos:

```bash
./cli --role as --email seu.email@ifrn.edu.br
./cli --role aluno --email seu.email@ifrn.edu.br
```

O comando alterna o grupo `AS`, que é o que o backend usa para forçar o modo de assistente social no login.
## Passo a passo
1. Rode `./cli` e escolha se quer entrar como AS ou Aluno.
2. Informe o e-mail que o SUAP devolve no login.
3. Faça login via SUAP de novo para o backend atualizar o perfil.
4. Se quiser trocar de novo, rode o comando outra vez.
