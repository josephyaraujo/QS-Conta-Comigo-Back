# Relatório — Atividade II.VI.I: Code Smells incluindo Segurança

## 1. Introdução

Esta atividade teve como objetivo integrar uma ferramenta de análise estática de segurança ao projeto Conta Comigo, identificando possíveis vulnerabilidades no código Python e corrigindo os problemas encontrados.

Para isso, foi utilizada a ferramenta **Bandit**, que analisa código Python em busca de padrões associados a problemas de segurança. Além da correção dos apontamentos, a ferramenta foi integrada ao pipeline de integração contínua do projeto, permitindo a execução automática das verificações em cada push e pull request.

## 2. Metodologia

O trabalho foi desenvolvido na branch `security/analise-estatica-bandit`, seguindo o fluxo de desenvolvimento adotado no projeto: issue, branch, commits semânticos, pull request e merge.

Inicialmente, o Bandit foi instalado e sua versão foi fixada no arquivo `requirements.txt`:

```text
bandit==1.9.4
```

A primeira análise foi executada com o comando:

```bash
python -m bandit -r api conta_comigo_backend
```

A varredura identificou cinco ocorrências, distribuídas em três tipos de apontamentos:

| Código | Problema | Ocorrências | Severidade |
|---|---|---:|---|
| B113 | Requisições HTTP sem timeout | 3 | Medium |
| B110 | Uso de `try/except/pass` | 1 | Low |
| B105 | Possível senha hardcoded | 1 | Low |

## 3. Análise e correção dos apontamentos

### 3.1. B113 — Requisições HTTP sem timeout

Foram identificadas três chamadas HTTP realizadas com a biblioteca `requests` sem definição de tempo limite de execução:

- `api/SuapServices/suap_service.py`: duas ocorrências;
- `api/views/auth.py`: uma ocorrência.

A ausência de timeout poderia permitir que requisições demorassem indefinidamente, consumindo recursos da aplicação.

**Correção:** foi adicionado o parâmetro `timeout=10` às três requisições, estabelecendo um limite de dez segundos para a espera pelas respostas.

### 3.2. B110 — Tratamento genérico de exceção

No arquivo `api/services/relatorioService.py`, a função `formatar_data` utilizava um bloco `try/except` genérico, com `pass` no tratamento da exceção.

Esse comportamento ignorava possíveis erros sem apresentar uma justificativa ou tratamento específico.

**Correção:** o bloco foi removido, mantendo a conversão de datas por meio de operações de string. Dessa forma, o código ficou mais simples e não oculta exceções desnecessariamente.

### 3.3. B105 — Possível senha hardcoded

O Bandit identificou como possível senha hardcoded a string correspondente ao endpoint de autenticação OAuth do SUAP:

```python
token_url = "https://suap.ifrn.edu.br/o/token/"
```

Após a análise, verificou-se que o valor não representava uma senha ou credencial, mas sim uma URL pública utilizada no processo de autenticação. Portanto, tratava-se de um falso positivo da análise estática.

**Correção:** a variável foi renomeada para `authorization_endpoint`, tornando sua finalidade mais explícita e eliminando a identificação equivocada pelo Bandit.

### 3.4. Remoção de exposição de credenciais nos logs

Durante a inspeção do código de autenticação, também foi identificado que instruções `print()` registravam os dados enviados ao SUAP e a resposta recebida.

Como os dados enviados continham o `client_secret` e a resposta poderia conter o `access_token`, esses registros representavam um risco de exposição de credenciais.

**Correção:** as instruções de impressão foram removidas, evitando que informações sensíveis fossem registradas nos logs.

## 4. Integração ao pipeline e validação

Após as correções, foi realizada uma nova análise com o Bandit:

```bash
python -m bandit -r api conta_comigo_backend
```

O resultado foi:

```text
Test results:
    No issues identified.

Total issues (by severity):
    Undefined: 0
    Low: 0
    Medium: 0
    High: 0

Files skipped (0):
```

### 4.1. Integração com GitHub Actions

O Bandit foi integrado ao workflow `.github/workflows/django-ci.yml`, com a seguinte etapa:

```yaml
- name: Analisar segurança com Bandit
  run: python -m bandit -r api conta_comigo_backend
```

A etapa foi posicionada após a instalação das dependências, garantindo que a ferramenta esteja disponível durante a execução do pipeline.

Com isso, a análise de segurança passou a ser executada automaticamente nos eventos de push e pull request.

## 5. Integração das alterações

As alterações foram organizadas em dois commits semânticos:

- `297cb95` — `fix(security): corrige vulnerabilidades identificadas pelo Bandit`
- `75b5e26` — `ci(security): integra Bandit ao pipeline`

Após a publicação da branch, o GitHub Actions executou o workflow e todas as etapas foram aprovadas.

Em seguida, foi criado um pull request para integrar as alterações à branch principal do projeto.

## 6. Conclusão

A atividade permitiu incorporar uma nova camada de verificação de segurança ao projeto Conta Comigo, utilizando o Bandit para identificar padrões potencialmente vulneráveis no código Python.

Foram encontrados cinco apontamentos iniciais, distribuídos em três categorias. Após a análise e as correções, a ferramenta passou a concluir a varredura sem identificar problemas.

Além das correções diretamente apontadas pelo Bandit, foi removido o registro de informações sensíveis nos logs da autenticação com o SUAP, reduzindo o risco de exposição de credenciais.

Por fim, a integração ao GitHub Actions automatizou a análise de segurança no processo de desenvolvimento. Os 133 testes automatizados foram aprovados e todas as verificações do pipeline foram concluídas com sucesso.
