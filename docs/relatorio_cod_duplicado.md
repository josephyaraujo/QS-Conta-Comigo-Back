# Relatório — Atividade II.II: Código Duplicado

**Disciplina:** Qualidade de Software  
**Projeto:** Conta Comigo — Backend  
**Repositório:** [QS-Conta-Comigo-Back](https://github.com/josephyaraujo/QS-Conta-Comigo-Back)  
**Branch de trabalho:** `feat/detector-codigo-duplicado`

## 1. Introdução

A duplicação de código ocorre quando trechos de implementação semelhantes são repetidos em diferentes partes de um sistema. Essa prática pode aumentar o esforço de manutenção, dificultar a evolução do código e fazer com que alterações precisem ser reproduzidas em vários locais.

Nesta atividade, foi realizada uma análise estática do backend do projeto Conta Comigo com o objetivo de identificar e reduzir duplicações, melhorar a organização do código e preservar o comportamento existente da aplicação.

## 2. Objetivos

- Identificar trechos de código duplicados no projeto.
- Aplicar técnicas de refatoração para centralizar comportamentos e dados repetidos.
- Utilizar o Pylint para detectar duplicações.
- Executar os testes automatizados para verificar se as alterações preservaram o funcionamento do sistema.
- Validar o resultado por meio de ferramentas automatizadas.

## 3. Metodologia e ferramentas

A atividade foi desenvolvida com análise estática do código Python, refatorações incrementais e execução de testes automatizados.

As principais ferramentas utilizadas foram:

- **Pylint:** ferramenta de análise estática configurada para detectar código duplicado por meio da regra `duplicate-code` (R0801).
- **Django Test Framework:** utilizado para executar os testes automatizados do projeto.

A configuração do Pylint foi ajustada para concentrar a análise na detecção de duplicações, desconsiderando elementos como comentários, docstrings e imports, conforme as opções definidas no arquivo `pyproject.toml`.

## 4. Problemas identificados e refatorações realizadas

### 4.1. Duplicação nos testes automatizados

Foram identificados dados de preparação repetidos em diferentes testes de modelos e serializers. Para reduzir essa repetição, foram criadas e reutilizadas funções auxiliares no arquivo `api/tests/factories.py`.

Essas funções centralizam a criação de dados de teste para entidades como benefícios, solicitações, formulários, questões, perguntas, assistentes sociais, alunos e auxílios.

Com isso, os testes passaram a compartilhar estruturas de dados padronizadas, facilitando a manutenção e reduzindo a necessidade de repetir configurações semelhantes.

### 4.2. Duplicação na definição de campos

Também foi identificada repetição na definição de campos relacionados aos formulários e às questões de formulários.

Para solucionar esse problema, foram centralizadas constantes com as listas de campos reutilizadas pelos serializers e pela configuração administrativa. Os arquivos envolvidos incluem `api/serializers/campos.py`, `api/serializers/formularios.py`, `api/serializers/base.py` e `api/admin.py`.

Essa mudança permite manter as definições compartilhadas em um único local, reduzindo inconsistências e simplificando futuras alterações.

### 4.3. Duplicação nas permissões das views

A análise estática apontou trechos semelhantes na implementação do método `get_permissions()` em diferentes views da aplicação, especialmente nas views de chamados, formulários, perguntas e solicitações.

Para reduzir essa duplicação, foi proposta a extração da lógica comum para a função auxiliar `obter_permissoes_por_acao`, localizada em `api/views/permissions_helpers.py`.

A função permite reutilizar a seleção de permissões conforme a ação executada, mantendo as diferenças entre as regras de acesso de alunos e assistentes sociais.

As listas de ações específicas de cada view permanecem definidas nas respectivas classes, enquanto a lógica compartilhada fica centralizada no helper.

## 5. Validação dos resultados

Após as refatorações, foram executadas as verificações automatizadas do projeto.

### 5.1. Testes automatizados

Comando executado:

`python manage.py test`

Resultado:

- **133 testes encontrados e executados.**
- Verificação do sistema Django sem problemas identificados.
- Todos os testes concluídos com sucesso.
- Nenhuma falha ou erro reportado.

### 5.2. Análise estática com Pylint

Comando executado:

`python -m pylint api conta_comigo_backend`

Resultado:

- **Pontuação final: 10,00/10.**
- Pontuação incial: 9,83/10.
- Não foram reportados avisos na saída apresentada.

A pontuação obtida indica que a análise executada pelo Pylint foi concluída sem penalizações na configuração utilizada. Em particular, o resultado confirma que a ferramenta não reportou as duplicações que motivaram as últimas refatorações.

## 6. Considerações finais

A atividade permitiu identificar e reduzir repetições em diferentes áreas do backend do Conta Comigo, incluindo a preparação de dados de teste, a definição de campos compartilhados e a lógica de seleção de permissões das views.

A centralização desses elementos contribui para tornar o código mais organizado e facilita sua manutenção, pois alterações em comportamentos compartilhados podem ser realizadas em um único local.

A validação final apresentou 133 testes aprovados e pontuação de 10,00/10 no Pylint. Esses resultados demonstram que as verificações executadas foram concluídas com sucesso após as refatorações, sem evidência de regressões nos testes automatizados.

Dessa forma, os resultados obtidos atendem ao objetivo técnico da atividade de reduzir duplicações e verificar a integridade do sistema após as mudanças.

## Referência

PYLINT. *duplicate-code / R0801*. Documentação oficial do Pylint. Disponível em: https://pylint.readthedocs.io/en/v4.1.3/user_guide/messages/refactor/duplicate-code.html. Acesso em: 25 set. 2026.