# Conta Comigo - Backend

Este é o repositório do backend para o projeto Conta Comigo. O ambiente de desenvolvimento é totalmente conteinerizado com Docker, garantindo que todos os desenvolvedores trabalhem em um ambiente idêntico.

## 🚀 Começando

Siga estas instruções para configurar e executar o ambiente de desenvolvimento na sua máquina.

### Pré-requisitos

Antes de começar, garanta que você tem os seguintes programas instalados:

* **Git:** Para clonar o repositório.
* **Docker Desktop:** Para gerenciar os contêineres. [Faça o download aqui](https://www.docker.com/products/docker-desktop/).
* **Visual Studio Code:** Nosso editor de código padrão. [Faça o download aqui](https://code.visualstudio.com/).
* **Extensão Dev Containers (da Microsoft):** Essencial para integrar o VS Code com o Docker. [Instale por aqui](vscode:extension/ms-vscode-remote.remote-containers).

### ⚙️ Instalação e Primeira Execução

Com os pré-requisitos instalados, siga estes passos para o primeiro setup:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/tads-cnat/Conta-Comigo-Backend.git
    cd conta-comigo-backend
    ```

2.  **Abra o projeto no VS Code:**
    ```bash
    code .
    ```

3.  **Reabra no Contêiner:** O VS Code deve detectar os arquivos de configuração (`.devcontainer`) e mostrar uma notificação no canto inferior direito perguntando se você quer "Reabrir no Contêiner" ("Reopen in Container"). **Clique nesse botão.**

    > 💡 **Dica:** Se a notificação não aparecer, abra a Paleta de Comandos (`Cmd+Shift+P` no Mac ou `Ctrl+Shift+P` no Windows/Linux), digite `Dev Containers: Rebuild and Reopen in Container` e selecione a opção.

4.  **Aguarde a Construção (Build):** Na primeira vez, o Docker irá baixar as imagens e construir o ambiente. Este processo pode levar alguns minutos.

**Pronto! Seu ambiente de desenvolvimento está 100% configurado.**

## 💻 Fluxo de Trabalho Diário

* **Para Iniciar o Ambiente:** Apenas abra a pasta do projeto no VS Code e clique em "Reopen in Container". Tudo iniciará automaticamente.
* **Executando o Servidor:** O servidor Django inicia automaticamente. Para iniciar em modo de depuração, vá para a aba "Run and Debug" (ícone de play) e clique no play verde ao lado de "Python: Django" (ou pressione `F5`).
* **Executando Comandos Django:** Use o terminal integrado do VS Code para rodar qualquer comando `manage.py`, como `makemigrations`, `shell`, etc.
* **Para Parar o Ambiente:** Feche a conexão (`Reopen Folder Locally`) e, se quiser liberar os recursos, rode `docker-compose down` em um terminal local.

## 🗄️ Acessando o Banco de Dados (DBeaver, etc.)

Você pode se conectar ao banco de dados PostgreSQL usando sua ferramenta de preferência com as seguintes credenciais:

* **Host:** `localhost`
* **Porta:** `5432`
* **Banco de Dados:** `contacomigo_db`
* **Usuário:** `postgres`
* **Senha:** `pafinha` (ou a senha definida no `docker-compose.yaml`)

## Endpoints implementados:

- Solicitação;
- Formulários;
- Formulario_questão;
- Formulario_questao_opcao;
- Dashboard;
- Benefícios;
- Auxílios;
- Auth/login;
- Auth/exchange.

## Testando endpoints no Swagger

Para testar os endpoints no swagger é necessário realizar o login, para isso realize os seguintes passos:

* O endpoint **GET/auth/login**  gera um link, pegue o link e abra em outra aba e coloque suas credenciais do SUAP. Se for sua primeira vez logando ele vai pedir permissão para compartilhar os dados.
* Ele irá te direcionar para outra aba que não irá carregar mas na url irá gerar um **code**, copie o texto que tem pós "code=" 
* Insira esse code no body do endpoint **GET/auth/exchange**, o response body irá fornecer informações do usuário e o **token access**, copie o token accsse e vá até o topo da documentação Swagger
* No botão **Authorize** digite **Bearer seu_access_token** (Não esqueça de dar espaço após escrever Bearer)
* Depois disso você estará autheticado e poderá usar os endpoints.

### JSON de testes para endpoints implementados:

#### Formulário:
> POST/formulario
  ``` json
    {
      "titulo": "Avaliação de Satisfação - Auxílio Alimentação",
      "objetivo": "Avaliar a qualidade do serviço de alimentação oferecido pelo campus",
      "solicitados": "todos",
      "data_inicio": "2025-11-05",
      "data_fim": "2025-11-30",
      "questoes": [
        {
          "titulo_pergunta": "Como você avalia a qualidade das refeições?",
          "tipo_pergunta": "multipla_escolha",
          "obrigatoriedade": true,
          "opcoes": [
            {"alternativa": "Excelente"},
            {"alternativa": "Bom"},
            {"alternativa": "Regular"},
            {"alternativa": "Ruim"},
            {"alternativa": "Péssimo"}
          ]
        },
        {
          "titulo_pergunta": "Você recomendaria o auxílio alimentação para outros alunos?",
          "tipo_pergunta": "multipla_escolha",
          "obrigatoriedade": true,
          "opcoes": [
            {"alternativa": "Sim, com certeza"},
            {"alternativa": "Sim, provavelmente"},
            {"alternativa": "Não tenho opinião"},
            {"alternativa": "Não, provavelmente não"},
            {"alternativa": "Não, definitivamente não"}
          ]
        }
      ]
    }
  ```
 

