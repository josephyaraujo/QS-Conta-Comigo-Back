# Guia de Testes — Conta Comigo Backend

Este documento explica como rodar os testes unitários e gerar o relatório de cobertura de código do projeto usanso o Coverage.py e o Pytest.

---

## Pré-requisitos

Certifique-se de que o ambiente virtual está ativado e as dependências instaladas:

```bash
# Ativar o ambiente virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalar o coverage (caso ainda não tenha)
pip install coverage
pip install pytest pytest-django pytest-cov
```

---

## Rodando os testes

```bash
# Todos os testes
python manage.py test api.tests

# Apenas models ou serializers
python manage.py test api.tests.models
python manage.py test api.tests.serializers

# Um arquivo específico
python manage.py test api.tests.models.test_auxilio
```

> **Nunca use o botão "Run Python File" do VS Code.** Sempre use o terminal com `python manage.py test`.

---

## Cobertura de código com o Coverage.py

```bash
# 1. Rodar os testes com coverage
coverage run --source=api manage.py test api.tests

# 2. Ver relatório no terminal
coverage report -m

# 3. Ver relatório visual no navegador (opcional)
coverage html
# Abra: htmlcov/index.html
```

## Cobertura de códifo com o Pytest

### Arquivos de configuração do projeto: 
Para garantir que os testes rodem corretamente e que o cálculo de cobertura ignore arquivos automáticos do Django (como migrações), a raiz do projeto já conta com dois arquivos essenciais:

- pytest.ini: Define o módulo de configurações padrão do Django (conta_comigo_backend.settings) e o padrão de nomenclatura dos arquivos de teste.

```bash
[pytest]
DJANGO_SETTINGS_MODULE = conta_comigo_backend.settings
python_files = tests.py test_*.py *_tests.py
```

- .coveragerc: Filtra e omite arquivos como manage.py, wsgi.py e pastas de migrations para que a métrica de cobertura foque estritamente nas nossas regras de negócio (Models, Serializers, Views e Utils).

```bash
[run]
source = .
omit =
    *apps.py
    *migrations*
    *settings*
    *urls.py
    manage.py
    *wsgi.py
    *asgi.py

[report]
show_missing = True
```
### Rodando os teste de cobertura no terminal: 

```bash
# 1. Rodar os testes com pytest
pytest --cov=.

# 2. Ver relatório visual no navegador (opcional)
pytest --cov=. --cov-report=html
# Abra: htmlcov/index.html
```
---

## Interpretação do relatório

| Coluna | Significado |
|--------|-------------|
| `Stmts` | Total de linhas de código executáveis |
| `Miss` | Linhas **não** executadas pelos testes |
| `Cover` | Percentual de cobertura |
| `Missing` | Quais linhas exatamente não foram cobertas |