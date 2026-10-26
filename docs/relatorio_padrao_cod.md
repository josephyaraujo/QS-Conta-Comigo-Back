# Relatório — Atividade II.I: Padrão de Codificação

**Projeto:** Conta Comigo — Backend
**Ferramenta:** Ruff Formatter
**Branch:** `feat/padrao-codificacao-python`

## Objetivo

Configurar uma ferramenta de padronização de código Python e integrá-la à pipeline do GitHub Actions, garantindo a verificação automática da formatação.

## Passo a passo realizado

1. **Issue e branch:** organizei a atividade no GitHub Flow, criando uma branch específica para o trabalho.
2. **Configuração do Ruff:** utilizei o Ruff Formatter para padronizar a formatação do código Python.
3. **Integração à pipeline:** adicionei à pipeline do GitHub Actions o comando `python -m ruff format --check api conta_comigo_backend`.
4. **Teste de falha:** a primeira execução identificou 90 arquivos que precisavam de formatação, fazendo a pipeline falhar conforme esperado.
5. **Correção:** executei `python -m ruff format api conta_comigo_backend`, reformatando os arquivos necessários.
6. **Validação:** confirmei que os 112 arquivos estavam formatados, os 137 testes passaram e as verificações do Django e do Ruff foram aprovadas.
7. **Integração:** registrei as alterações em um commit, enviamos a branch ao GitHub, abrimos um Pull Request e realizamos o merge na branch principal.

## Resultado
A atividade foi concluída com sucesso. A pipeline passou a verificar automaticamente a formatação do código Python, identificando desvios e impedindo que essa verificação seja ignorada durante a integração das alterações.
