# Relatório da Atividade II.III — Diagrama de Classes UML

## 1. Objetivo

Implementar a geração de um diagrama de classes UML para o projeto Conta Comigo, utilizando ferramentas integradas ao Django e automatizando sua criação por meio do pipeline do GitHub Actions.

## 2. Análise dos componentes implementados

### 2.1. Django Extensions

Foi adicionada ao projeto a biblioteca django-extensions, responsável por disponibilizar comandos administrativos adicionais ao Django, entre eles o comando graph_models, utilizado para gerar representações gráficas dos modelos da aplicação.

A dependência foi registrada no arquivo requirements.txt, com a versão 4.1.0.

Além disso, foi necessário adicionar django_extensions à configuração INSTALLED_APPS, localizada em conta_comigo_backend/settings.py, permitindo que o Django reconhecesse os comandos disponibilizados pela extensão.

### 2.2. pydot

A biblioteca pydot, na versão 4.0.1, foi adicionada como dependência do projeto.

Ela permite a integração entre o comando de geração do diagrama e o formato de representação gráfica utilizado pelo Graphviz. Dessa forma, o Django Extensions consegue produzir o arquivo de imagem correspondente às classes e aos relacionamentos identificados nos modelos.

### 2.3. Graphviz

O Graphviz é uma ferramenta externa utilizada para renderizar representações gráficas de estruturas e relacionamentos.

Como sua execução depende de um programa instalado no sistema operacional, foi necessário incluí-lo também no ambiente de execução do GitHub Actions.

Para isso, foi adicionada ao workflow uma etapa responsável pela instalação do Graphviz por meio do gerenciador de pacotes do Ubuntu:

```- name: Instalar Graphviz
  run: |
    sudo apt-get update
    sudo apt-get install -y graphviz
```

Essa configuração garante que o comando necessário para renderizar o diagrama esteja disponível durante a execução automatizada do pipeline.

### 2.4. Geração do diagrama de classes UML

Após a instalação e configuração das dependências, foi utilizado o comando abaixo para gerar o diagrama dos modelos pertencentes à aplicação api:

python manage.py graph_models api --pydot -g -o docs/diagrama-classes-dominio.png

Os parâmetros utilizados possuem as seguintes finalidades:

* graph_models: executa o comando disponibilizado pelo Django Extensions para gerar o diagrama.
* api: indica a aplicação cujos modelos serão representados.
* --pydot: utiliza o pydot como mecanismo de geração gráfica.
* -g: inclui informações dos modelos, como campos e relacionamentos.
* -o: define o caminho e o nome do arquivo de saída.

A imagem gerada foi armazenada no diretório docs/, com o nome diagrama-classes-dominio.png, e adicionada ao repositório.

### 2.5. Integração ao pipeline do GitHub Actions

A geração do diagrama também foi incorporada ao workflow existente em .github/workflows/django-ci.yml.

Após a preparação do ambiente e a execução das migrações, o pipeline cria o diretório de documentação, gera a imagem e disponibiliza o resultado como artefato da execução.

O trecho implementado foi:

```- name: Gerar diagrama de classes UML
  run: |
    mkdir -p docs
    python manage.py graph_models api --pydot -g -o docs/diagrama-classes-dominio.png
- name: Publicar diagrama UML como artefato
  uses: actions/upload-artifact@v7
  with:
    name: diagrama-classes-dominio
    path: docs/diagrama-classes-dominio.png
    if-no-files-found: error
    retention-days: 30
```

A utilização da ação upload-artifact permite armazenar a imagem gerada como um artefato associado à execução do workflow. Assim, o resultado pode ser consultado e baixado diretamente na página da execução do GitHub Actions.

A configuração if-no-files-found: error também estabelece que a execução deve falhar caso a imagem esperada não seja encontrada, evitando que uma geração malsucedida passe despercebida.

## 3. Conclusão

A atividade foi concluída com a implementação da geração do diagrama de classes UML e sua integração ao pipeline do GitHub Actions.

Com isso, o projeto passou a gerar automaticamente a representação visual de seus modelos durante a execução do CI, disponibilizando a imagem como artefato. As validações realizadas também confirmaram que as alterações não comprometeram o funcionamento da aplicação.

## 4. Referências

* DJANGO EXTENSIONS. https://django-extensions.readthedocs.io/
* GRAPHVIZ. https://graphviz.org/documentation/
* GITHUB ACTIONS. https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts