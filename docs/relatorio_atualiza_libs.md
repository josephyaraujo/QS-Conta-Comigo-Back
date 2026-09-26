# Atividade I.VII — Bibliotecas Seguras

## 1. Objetivo

Configurar métodos para identificar vulnerabilidades e manter as bibliotecas do projeto atualizadas, reduzindo riscos de segurança e verificando se as atualizações mantêm o funcionamento da aplicação.

## 2. Métodos utilizados

Para esta atividade, foram escolhidos dois métodos de identificação e monitoramento de dependências:

### 2.1. GitHub Dependabot

O Dependabot foi configurado para monitorar as dependências Python do projeto e as GitHub Actions utilizadas no repositório.

Foi criado o arquivo `.github/dependabot.yml`, com verificações semanais para os seguintes ecossistemas:

* **pip:** monitoramento das dependências Python.
* **GitHub Actions:** monitoramento das dependências das ações utilizadas nos workflows.

O objetivo é identificar dependências que precisam de atualização e facilitar a manutenção contínua do projeto.

### 2.2. pip-audit

O `pip-audit` foi utilizado para identificar vulnerabilidades conhecidas nas dependências Python instaladas no ambiente.

A ferramenta foi instalada no ambiente de desenvolvimento e executada por meio do comando:

```bash
python -m pip_audit
```

A auditoria inicial identificou **97 registros de vulnerabilidades em 10 pacotes**.

Após as atualizações realizadas, uma nova auditoria identificou **13 registros de vulnerabilidades em 2 pacotes**.

Isso representa uma redução de **84 registros**, aproximadamente **86,6%** em relação à auditoria inicial.

## 3. Bibliotecas atualizadas

As seguintes dependências tiveram suas versões atualizadas no arquivo `requirements.txt`:

| Biblioteca             | Versão anterior | Versão atual |
| ---------------------- | --------------- | ------------ |
| cryptography           | 47.0.0          | 50.0.0       |
| Django                 | 5.0.7           | 5.2.17       |
| djangorestframework    | 3.15.2          | 3.17.2       |
| idna                   | 3.13            | 3.15         |
| Pillow                 | 12.2.0          | 12.3.0       |
| social-auth-app-django | 5.4.3           | 5.6.0        |
| sqlparse               | 0.5.5           | 0.6.0        |
| urllib3                | 2.6.3           | 2.7.0        |

As versões foram atualizadas buscando reduzir as vulnerabilidades identificadas e preservar a compatibilidade entre as dependências do projeto.

## 4. Dependências que permaneceram pendentes

Após as atualizações, a auditoria ainda identificou vulnerabilidades conhecidas em duas dependências:

* **PyJWT 2.12.1:** a ferramenta indicou a versão 2.13.0 como correção.
* **social-auth-core 4.8.7:** a ferramenta indicou a versão 5.0.0 como correção.

Durante as tentativas de atualização, foram identificados conflitos de compatibilidade entre as versões das dependências, incluindo restrições relacionadas ao PyJWT e ao pacote `requests`.

Por esse motivo, essas versões foram mantidas para preservar a resolução das dependências.

Assim, a auditoria final não foi considerada livre de vulnerabilidades, mas trouxe avanços significativos.

## 5. Testes e validações

Após as atualizações, foram executadas as seguintes verificações:

| Verificação                                                               | Resultado   |
| ------------------------------------------------------------------------- | ----------- |
| `python -m pip check`                                                     | Aprovado    |
| `python manage.py check`                                                  | Aprovado    |
| `python manage.py test`                                                   | Aprovado    |                                             
| `pytest -W error::DeprecationWarning -W error::PendingDeprecationWarning` | Aprovado    |                                             
| `python -m ruff check api conta_comigo_backend --select UP`               | Aprovado    |                                             

Os testes e as verificações foram concluídos sem erros, indicando que as atualizações realizadas não provocaram falhas nas validações executadas.

## 6. Resultados

A atividade permitiu:

* Configurar o GitHub Dependabot para monitoramento de dependências Python e GitHub Actions.
* Utilizar o `pip-audit` para identificar vulnerabilidades conhecidas.
* Atualizar oito dependências do projeto.
* Reduzir de 97 para 13 os registros de vulnerabilidades identificados pela auditoria.
* Executar testes e verificações de compatibilidade após as atualizações.
* Identificar dependências que ainda precisam de análise devido a conflitos de compatibilidade.

## 7. Conclusão

A atividade demonstrou a importância do monitoramento contínuo das bibliotecas utilizadas em um projeto de software.

A configuração do Dependabot e a utilização do `pip-audit` permitiram identificar dependências que necessitavam de atualização e reduzir significativamente os registros de vulnerabilidades encontrados.

As atualizações foram validadas por meio de testes e verificações automatizadas. Entretanto, ainda existem vulnerabilidades identificadas em duas dependências, que deverão ser tratadas posteriormente, considerando a compatibilidade entre os pacotes.
