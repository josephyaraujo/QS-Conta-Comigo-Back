# Atividade I.VI — Código Depreciado

## 1. Objetivo

Esta atividade teve como objetivo identificar a utilização de código depreciado ou obsoleto no projeto **Conta Comigo Backend**, configurar ferramentas para realizar essa verificação pela linha de comando e integrar a verificação ao pipeline de CI do GitHub Actions.

Além da identificação e correção de uma ocorrência encontrada no código-fonte, foi realizada uma falha controlada utilizando `DeprecationWarning`, com o objetivo de comprovar que o pipeline realmente falharia caso uma utilização de código depreciado fosse identificada.

---

## 2. Ferramentas utilizadas

Foram utilizadas duas abordagens complementares para a detecção.

### 2.1 Pytest

O projeto já utilizava **pytest**, portanto a ferramenta foi aproveitada para verificar avisos de depreciação durante a execução dos testes.

Foi configurada a execução dos testes tratando os seguintes avisos como erros:

```bash
pytest -W error::DeprecationWarning -W error::PendingDeprecationWarning
```

Dessa forma, caso algum código durante a execução dos testes gere um `DeprecationWarning` ou `PendingDeprecationWarning`, o teste falha e o pipeline também falha.

---

### 2.2 Ruff

Também foi utilizado o **Ruff** para realizar uma análise estática do código Python.

A versão utilizada foi:

```text
ruff 0.16.9
```

Para verificar regras relacionadas à modernização/depreciação do código, foi utilizada a família de regras `UP`:

```bash
python -m ruff check api conta_comigo_backend --select UP
```

---

## 3. Configuração do pipeline

A detecção foi adicionada ao workflow existente do GitHub Actions:

```text
.github/workflows/django-ci.yml
```

Foram adicionadas as seguintes etapas:

```yaml
- name: Detectar código depreciado
  run: pytest -W error::DeprecationWarning -W error::PendingDeprecationWarning

- name: Verificar código com Ruff
  run: python -m ruff check api conta_comigo_backend --select UP
```

Dessa maneira, o pipeline passa a verificar tanto avisos de depreciação durante a execução dos testes quanto problemas identificados estaticamente pelo Ruff.

---

## 4. Teste controlado de código depreciado

Inicialmente, os testes existentes foram executados com os avisos de depreciação tratados como erros:

```bash
pytest -W error::DeprecationWarning -W error::PendingDeprecationWarning
```

O resultado foi:

```text
137 passed in 3.49s
```

Isso demonstrou que, naquele momento, os testes existentes não geravam avisos de depreciação.

Como o objetivo da atividade também era comprovar que o pipeline realmente detectaria uma situação de código depreciado, foi criado temporariamente um teste controlado.

Arquivo utilizado:

```text
api/tests/test_deprecacao.py
```

Código utilizado:

```python
import warnings


def test_codigo_depreciado():
    warnings.warn(
        "Este código está depreciado.",
        DeprecationWarning,
        stacklevel=2,
    )
```

O teste foi executado novamente com:

```bash
pytest -W error::DeprecationWarning -W error::PendingDeprecationWarning
```

### Resultado da falha controlada

O pytest identificou o `DeprecationWarning` e fez o teste falhar:

```text
collected 138 items

...

api/tests/test_deprecacao.py F

...

E       DeprecationWarning: Este código está depreciado.
api/tests/test_deprecacao.py:5: DeprecationWarning

...

1 failed, 137 passed in 3.77s
```

Essa execução comprovou que a configuração:

```text
-W error::DeprecationWarning
```

funciona corretamente.

Ou seja, caso o projeto utilize código que gere um `DeprecationWarning`, a execução dos testes será interrompida e o pipeline ficará com falha.

> **Observação:** esse teste foi criado exclusivamente para validar o mecanismo de detecção e posteriormente foi removido do projeto. Ele não representa uma ocorrência real encontrada no código da aplicação.

---

## 5. Detecção de código obsoleto com Ruff

Após a configuração do Ruff, foi executado:

```bash
python -m ruff check api conta_comigo_backend --select UP
```

A ferramenta identificou uma ocorrência no arquivo:

```text
api/SuapServices/suap_service.py
```

O código originalmente estava escrito como:

```python
class PopulateUsuario():
```

O Ruff identificou a regra:

```text
UP039 [*] Unnecessary parentheses after class definition
```

Resultado apresentado:

```text
UP039 [*] Unnecessary parentheses after class definition
 --> api/SuapServices/suap_service.py:7:22
  |
5 | from django.db import transaction
6 |
7 | class PopulateUsuario():
  |                      ^^
8 |
9 |     def __init__(self):
  |
help: Remove parentheses
  |
6 |
- class PopulateUsuario():
7 + class PopulateUsuario:
8 |

Found 1 error.
[*] 1 fixable with the `--fix` option.
```

---

## 6. Correção encontrada

A declaração da classe foi corrigida de:

```python
class PopulateUsuario():
```

para:

```python
class PopulateUsuario:
```

Essa alteração remove os parênteses desnecessários da declaração da classe.

A correção foi feita diretamente no arquivo:

```text
api/SuapServices/suap_service.py
```

Após a alteração, o Ruff foi executado novamente:

```bash
python -m ruff check api conta_comigo_backend --select UP
```

Resultado:

```text
All checks passed!
```

---

## 7. Teste adicional do Ruff

Para validar especificamente a capacidade do Ruff de identificar determinados usos depreciados, foi criado temporariamente um arquivo de teste fora do código da aplicação.

Foi utilizado o seguinte código:

```python
from typing import List

nomes: List[str] = []
```

A verificação foi executada com:

```bash
python -m ruff check /tmp/test_deprecated.py --select UP
```

O Ruff identificou:

```text
UP035 `typing.List` is deprecated, use `list` instead
 --> /tmp/test_deprecated.py:1:1
1 | from typing import List
...

UP006 [*] Use `list` instead of `List` for type annotation
 --> /tmp/test_deprecated.py:3:8
3 | nomes: List[str] = []
...

Found 2 errors.
[*] 1 fixable with the `--fix` option.
```

Essa verificação serviu como demonstração adicional de que o Ruff consegue identificar usos depreciados relacionados às regras `UP006` e `UP035`.

O arquivo utilizado nessa demonstração era temporário e não fazia parte do código da aplicação.

---

## 8. Resultado no GitHub Actions

As verificações foram adicionadas ao pipeline do GitHub Actions.

As etapas relacionadas à atividade foram:

```text
Detectar código depreciado
Verificar código com Ruff
```

Após as correções, ambas as etapas foram executadas com sucesso.

O pipeline também manteve as demais etapas existentes do projeto, como:

```text
Verificar projeto Django
Executar migrations
Executar testes
```

---

## 9. Conclusão

A atividade permitiu configurar mecanismos para identificar código depreciado/obsoleto no projeto **Conta Comigo Backend**.

Foram utilizadas duas formas de detecção:

* **Pytest**, configurado para transformar `DeprecationWarning` e `PendingDeprecationWarning` em erros;
* **Ruff**, configurado no pipeline para analisar estaticamente o código utilizando as regras `UP`.

Durante a análise pelo Ruff foi encontrada uma ocorrência real no projeto, referente à declaração da classe `PopulateUsuario` com parênteses desnecessários.

Também foi realizada uma falha controlada utilizando `DeprecationWarning`, comprovando que o mecanismo configurado realmente interrompe a execução quando um aviso de depreciação é encontrado.

Dessa forma, o projeto passou a possuir uma verificação automatizada no pipeline capaz de identificar problemas desse tipo e impedir que alterações contendo esses problemas sejam consideradas válidas pelo processo de integração contínua.