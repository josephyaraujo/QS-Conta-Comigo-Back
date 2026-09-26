
# Atividade I.V — Versionamento Semântico e LTS

## 1. Introdução

Esta atividade tem como objetivo identificar se o versionamento semântico (SemVer) e o suporte de longo prazo (LTS — Long-Term Support) estão disponíveis em três componentes de software utilizados no projeto Conta Comigo.

A análise considera as versões declaradas no arquivo `requirements.txt` do backend e as políticas de versionamento e suporte documentadas pelos respectivos projetos oficiais.

Os componentes analisados são:

- Django;
- Django REST Framework;
- Django REST Framework Simple JWT.

O objetivo é verificar como cada componente organiza suas versões, se possui uma política de suporte de longo prazo e apresentar evidências por meio de links para as documentações oficiais.

---

## 2. Metodologia

A análise foi realizada por meio da inspeção do arquivo `requirements.txt` e da consulta à documentação oficial dos componentes selecionados.

Foram considerados os seguintes critérios:

- **Versionamento Semântico (SemVer):** verificar se o componente utiliza uma convenção estruturada de numeração de versões e se declara seguir o padrão SemVer.
- **LTS (Long-Term Support):** verificar se o componente oferece versões com suporte de longo prazo e quais são as condições dessa política.
- **Evidências:** apresentar as versões declaradas no projeto e os links para as fontes oficiais que fundamentam as conclusões.

É importante destacar que possuir uma numeração de versões no formato `MAJOR.MINOR.PATCH` não significa, necessariamente, que um projeto adote integralmente o padrão SemVer.

---

## 3. Análise dos componentes

### 3.1. Django

**Componente:** Django  
**Categoria:** Framework web  
**Versão utilizada:** `5.0.7`

#### Versionamento semântico

O Django utiliza um sistema próprio de versionamento, com uma estrutura de numeração que apresenta semelhanças com o SemVer.

O projeto possui uma política oficial de lançamentos que estabelece como as versões são organizadas e como as mudanças são introduzidas.

Entretanto, a convenção utilizada pelo Django possui regras próprias e não deve ser considerada automaticamente uma implementação estrita do SemVer.

#### Suporte de longo prazo (LTS)

O Django possui versões designadas como LTS, que recebem suporte de segurança por um período maior do que as versões regulares.

A série 5.0, utilizada pelo projeto na versão 5.0.7, não é uma versão LTS. O suporte dessa série foi encerrado em abril de 2025.

Portanto, a versão utilizada no projeto não possui suporte oficial vigente.

#### Evidências

- [Política oficial de versões e suporte do Django](https://www.djangoproject.com/download/)
- [Política de lançamentos do Django](https://docs.djangoproject.com/en/5.0/internals/release-process/)
- [Anúncio oficial do Django 5.0](https://www.djangoproject.com/weblog/2023/dec/04/django-50-released/)

#### Resultado

- **Versionamento semântico:** possui sistema próprio de versionamento, semelhante ao SemVer.
- **LTS:** disponível para determinadas versões, mas não para a série 5.0 utilizada no projeto.
- **Situação da versão utilizada:** suporte encerrado.

---

### 3.2. Django REST Framework

**Componente:** Django REST Framework  
**Categoria:** Framework para construção de APIs REST  
**Versão utilizada:** `3.15.2`

#### Versionamento semântico

O Django REST Framework possui uma política própria de versionamento, com três componentes numéricos.

A documentação oficial descreve uma convenção que diferencia atualizações compatíveis, mudanças que podem afetar a API e grandes marcos do projeto.

Essa política apresenta características semelhantes ao versionamento semântico, mas possui regras próprias.

#### Suporte de longo prazo (LTS)

O projeto possui uma política de lançamentos e de descontinuação de funcionalidades.

Entretanto, não foi identificada nas fontes consultadas uma política formal de versões LTS que estabeleça um período específico de suporte de longo prazo.

A existência de uma política de manutenção e de compatibilidade não significa, por si só, que o componente ofereça LTS.

#### Evidências

- [Notas de versão e política de versionamento do Django REST Framework](https://www.django-rest-framework.org/community/release-notes/)
- [Anúncio de lançamento do Django REST Framework 3.16](https://www.django-rest-framework.org/community/3.16-announcement/)

#### Resultado

- **Versionamento semântico:** possui política própria de versionamento, com características semelhantes ao SemVer.
- **LTS:** não foi identificada uma política formal de suporte de longo prazo nas fontes consultadas.
- **Situação da versão utilizada:** a política de suporte da versão 3.15.2 deve ser avaliada conforme as notas de versão oficiais.

---

### 3.3. Django REST Framework Simple JWT

**Componente:** Django REST Framework Simple JWT  
**Categoria:** Biblioteca de autenticação baseada em JWT  
**Versão utilizada:** `5.5.1`

#### Versionamento semântico

O Simple JWT utiliza uma numeração estruturada de versões no formato `MAJOR.MINOR.PATCH`, como pode ser observado na versão 5.5.1 utilizada pelo projeto.

Entretanto, a documentação consultada não foi suficiente para confirmar que o projeto declara seguir integralmente o padrão SemVer.

Por esse motivo, a existência de uma numeração estruturada não será considerada, isoladamente, como comprovação de adesão formal ao SemVer.

#### Suporte de longo prazo (LTS)

A documentação do Simple JWT apresenta informações de compatibilidade com versões específicas do Django e do Django REST Framework.

A versão 5.5.1, por exemplo, documenta compatibilidade com Django 4.2, 5.0, 5.1 e 5.2 e com Django REST Framework 3.14 e 3.15.

Entretanto, não foi identificada nas fontes consultadas uma política formal de suporte de longo prazo para versões específicas do componente.

A existência de uma matriz de compatibilidade não equivale a uma garantia de LTS.

#### Evidências

- [Documentação oficial do Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Repositório oficial do Simple JWT no GitHub](https://github.com/jazzband/djangorestframework-simplejwt)

#### Resultado

- **Versionamento semântico:** utiliza numeração estruturada de versões, mas a adesão formal ao SemVer não foi confirmada.
- **LTS:** não foi identificada uma política formal de suporte de longo prazo nas fontes consultadas.
- **Situação da versão utilizada:** a compatibilidade documentada deve ser considerada na avaliação da dependência.

---

## 4. Tabela comparativa

| Componente | Versão no projeto | Versionamento semântico | LTS |
|---|---|---|---|
| Django | 5.0.7 | Sistema próprio, semelhante ao SemVer | Possui versões LTS, mas a série 5.0 não é LTS e está fora de suporte |
| Django REST Framework | 3.15.2 | Política própria, com características semelhantes ao SemVer | Não foi identificada política formal de LTS |
| Simple JWT | 5.5.1 | Numeração MAJOR.MINOR.PATCH; adesão formal não confirmada | Não foi identificada política formal de LTS |

---

## 5. Conclusão

A análise dos três componentes demonstra que todos possuem algum tipo de organização de versões, mas isso não significa que todos adotem formalmente o padrão SemVer ou ofereçam suporte de longo prazo.

O Django possui uma política explícita de suporte e versões LTS. Entretanto, a versão 5.0.7 utilizada no projeto pertence a uma série cujo suporte foi encerrado.

O Django REST Framework possui uma política própria de versionamento e descontinuação de funcionalidades, mas não foi identificada uma garantia formal de LTS nas fontes consultadas.

O Simple JWT utiliza uma numeração estruturada de versões e documenta a compatibilidade com outras dependências, mas não foi possível confirmar uma política formal de SemVer ou LTS.

Dessa forma, a atividade demonstra a importância de considerar não apenas o número da versão de uma dependência, mas também sua política de compatibilidade, manutenção e período de suporte.

---

## 6. Referências

- Django. [Download, versões e suporte oficial](https://www.djangoproject.com/download/).
- Django. [Política de lançamentos](https://docs.djangoproject.com/en/5.0/internals/release-process/).
- Django REST Framework. [Notas de versão e política de versionamento](https://www.django-rest-framework.org/community/release-notes/).
- Django REST Framework. [Anúncio da versão 3.16](https://www.django-rest-framework.org/community/3.16-announcement/).
- Django REST Framework Simple JWT. [Documentação oficial](https://django-rest-framework-simplejwt.readthedocs.io/).
- Django REST Framework Simple JWT. [Repositório oficial](https://github.com/jazzband/djangorestframework-simplejwt/).