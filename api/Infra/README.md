# Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:

   - Docker

   - Docker Compose

   - Git

## Configuração e Execução Local
1. Clonar o Repositório
Bash
```
git clone <URL_DO_REPOSITORIO>
cd conta-comigo-backend
```
2. Variáveis de Ambiente

Crie um arquivo .env na raiz do diretório backend utilizando o arquivo .env.example como base:
```
Bash

cp .env.example .env

Preencha as variáveis obrigatórias no arquivo .env:
Snippet de código

# Configurações Gerais do Django
ALLOWED_HOSTS=localhost,127.0.0.1
DEBUG=True

# Banco de Dados PostgreSQL
POSTGRES_DB=contacomigo_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha_segura
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Integração Autenticação SUAP
SOCIAL_AUTH_SUAP_KEY=seu_client_id_do_suap
SOCIAL_AUTH_SUAP_SECRET=seu_client_secret_do_suap
SOCIAL_AUTH_SUAP_REDIRECT_URI=http://localhost:3000/complete/suap
```
3. Subir os Containers

Execute o comando do Docker Compose para construir as imagens e iniciar os serviços (API e Banco de Dados):
```
docker compose up --build -d
```
4. Migrações e Massa de Dados (Seed)

Com os containers ativos, execute as migrações do banco de dados e popule as tabelas iniciais necessárias:
```
# Executar as Migrações do Django
docker compose exec api python manage.py migrate

# Popular o banco de dados com a massa de dados padrão (Seeds)
docker compose exec api python manage.py seed
```
A API estará disponível localmente no endereço: http://localhost:8001/api/

A documentação interativa da API poderá ser acessada em:

    Swagger UI: http://localhost:8001/swagger/


 Implantação e Operação no Azure

A esteira de Integração e Implantação Contínua (CI/CD) está configurada via Azure Pipelines (azure-pipelines.yml). O build da imagem utiliza o arquivo otimizado Dockerfile.prod e injeta a massa de configuração necessária antes de realizar o deploy na Máquina Virtual (VM) de destino.
Variáveis Obrigatórias no Azure DevOps

Para que o pipeline execute o deploy corretamente, as seguintes variáveis precisam estar cadastradas na aba Variables da pipeline ou em um Variable Group no Azure DevOps:

    ALLOWED_HOSTS

    POSTGRES_DB

    POSTGRES_USER

    POSTGRES_PASSWORD

    POSTGRES_HOST

    POSTGRES_PORT

    SOCIAL_AUTH_SUAP_KEY

    SOCIAL_AUTH_SUAP_SECRET

    SOCIAL_AUTH_SUAP_REDIRECT_URI

Comandos Úteis na VM do Azure

Caso precise realizar tarefas administrativas diretamente no container de produção hospedado na máquina virtual do Azure, utilize as instruções abaixo via conexão SSH.
Verificar o status do container da API:
Bash

sudo docker ps | grep cc-backend-container

Executar comando de Seed (Massa de dados) em produção:

Para atualizar ou rodar a seed de dados de suporte dentro do container em execução na VM:
```
sudo docker exec -it cc-backend-container python manage.py seed
```
Verificar se o Gunicorn está operando corretamente com os Workers:

Para garantir que o container não está utilizando o servidor de desenvolvimento e sim os processos gerenciados do Gunicorn:
```
sudo docker top cc-backend-container | grep gunicorn
```
Analisar logs em tempo real da API:
```
sudo docker logs -f --tail 100 cc-backend-container
```

LINK: https://contacomigo-api.chilecentral.cloudapp.azure.com/