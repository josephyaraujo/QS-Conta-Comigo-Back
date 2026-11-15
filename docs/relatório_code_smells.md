# Relatório — Atividade II.IV: Code Smells

## 1. Objetivo

A atividade teve como objetivo identificar e corrigir problemas de qualidade (*code smells*) no backend do sistema Conta Comigo, utilizando ferramentas de análise estática. Também foi realizada a integração dessas verificações ao pipeline de Integração Contínua (CI), permitindo acompanhar automaticamente a qualidade do código.

## 2. Ferramentas utilizadas

- **Ruff:** análise estática e identificação de problemas no código Python.
- **Django Test Framework:** execução dos testes automatizados.
- **Git e GitHub:** versionamento e gerenciamento das alterações.
- **GitHub Actions:** automação das verificações de qualidade e dos testes.

## 3. Code smells identificados e corrigidos

Foram identificadas e corrigidas quatro categorias de problemas:

### 3.1. Data e hora sem informação de fuso horário — DTZ005

**Arquivo:** `api/services/notificacaoService.py`

Foi substituído o uso de `datetime.now()` por `timezone.now()`, utilizando o gerenciamento de fuso horário disponibilizado pelo Django.

### 3.2. Captura genérica de exceções — BLE001

**Arquivo:** `api/views/notificacoes.py`

Foram removidos blocos `except Exception` desnecessários, simplificando o fluxo de execução e evitando a captura indiscriminada de erros inesperados.

### 3.3. Variáveis não utilizadas — F841

**Arquivo:** `api/views/relatorio.py`

Foram removidas variáveis que recebiam valores, mas não eram utilizadas posteriormente, eliminando atribuições desnecessárias.

### 3.4. Chave duplicada em dicionário — F601

**Arquivo:** `api/views/formularios.py`

Foi removida a declaração duplicada da chave `alunos_notificados_count` no dicionário utilizado para construir a resposta da operação de envio de formulários.

## 4. Integração ao pipeline de CI

O Ruff foi integrado ao workflow `Django CI`, localizado em `.github/workflows/django-ci.yml`.

Foi adicionada uma etapa específica para verificar as quatro regras tratadas na atividade: `DTZ005`, `BLE001`, `F841` e `F601`.

As verificações foram direcionadas aos arquivos modificados, mantendo também as demais etapas já existentes no pipeline, como execução dos testes, formatação e detecção de código duplicado.

## 5. Conclusão

A atividade permitiu identificar e corrigir quatro categorias distintas de code smells no backend do sistema Conta Comigo.

As correções contribuíram para melhorar a legibilidade, a organização e a manutenção do código. Além disso, a integração do Ruff ao GitHub Actions tornou as verificações parte do processo automatizado de desenvolvimento.

Com as alterações validadas e o pipeline executado com sucesso, os objetivos da atividade foram alcançados.
