# Atividade I.IV — OWASP

## 1. Introdução

Esta atividade tem como objetivo analisar o software desenvolvido no projeto **Conta Comigo**, utilizando como referência os 10 principais riscos de segurança conforme o **OWASP Top 10:2025**.

Nessa atividade buscou-se identificar problemas de segurança, apresentar evidências encontradas no projeto, justificar a classificação do risco e propor possíveis formas de correção.

Conforme orientado, o risco **A03:2025 — Software Supply Chain Failures** não foi considerado nesta análise.

Como na disciplina de Teste de Software o grupo já havia realizado análise utilizando o OWASP e o Postman, o relatóirio produzido durante a análise da aplicação utilizando o OWASP ZAP foi considerado como material complementar, constando nele resultados anteriores e evidências quem reforçam os achados da análise atual.

[Relatório anterior — Tutorial OWASP ZAP](https://github.com/becadev/OWASP-ZAP)

---

# 2. A01:2025 — Broken Access Control

## 2.1 Identificação do risco

Foi identificada uma possível falha relacionada ao controle de acesso em determinados recursos da API.

O projeto possui mecanismos de autorização baseados no tipo de usuário. Existem classes como `OnlyAssistenteSocial`, `OnlyAluno` e `IsAlunoOrAssistenteSocial`, demonstrando que existe uma preocupação com a separação de permissões por perfil.

Entretanto, a autorização por perfil não significa necessariamente que exista também uma autorização sobre o objeto específico que está sendo acessado.

Essa diferença é importante porque um usuário autenticado pode possuir permissão para utilizar determinado endpoint, mas ainda assim não deveria necessariamente conseguir consultar ou modificar qualquer objeto pertencente a outro usuário.

---

## 2.2 Evidência encontrada

Um exemplo está no `UsuarioViewSet`:

```python
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
```

O mesmo padrão aparece em outros ViewSets, como `AlunoViewSet` e `AssistenteSocialViewSet`, que utilizam `ModelViewSet` com um `queryset` geral.

Outro exemplo relevante é o `SolicitacaoViewSet`:

```python
class SolicitacaoViewSet(viewsets.ModelViewSet):
    queryset = Solicitacao.objects.all()
    serializer_class = SolicitacaoSerializer
    pagination_class = None
```

Nesse caso, não é observada na própria classe uma filtragem do `queryset` baseada no usuário autenticado.

Também foi identificado um ponto relevante no `DocumentoViewSet`. O endpoint responsável pelo envio de documentos recebe um identificador de aluno:

```python
@action(
    detail=True,
    methods=['post'],
    url_path='envia',
    parser_classes=[MultiPartParser, FormParser]
)
def envia(self, request, pk=None):
```

Posteriormente, esse identificador é utilizado para definir o aluno associado ao documento:

```python
data = request.data.copy()
data['aluno_id'] = pk
```

Embora exista uma permissão de perfil:

```python
permission_classes = [IsAlunoOrAssistenteSocial]
```

não é observada nessa operação uma verificação explícita de que o `pk` informado corresponde ao aluno associado ao usuário autenticado.

---

## 2.3 Justificativa

O problema identificado está relacionado ao princípio de **Broken Access Control** porque o sistema possui autorização baseada no tipo de usuário, mas determinados recursos não demonstram possuir uma verificação equivalente de propriedade do objeto.

Em outras palavras, existe uma diferença entre:

> "Este usuário pode utilizar este endpoint?"

e:

> "Este usuário pode acessar ou modificar especificamente este objeto?"

O primeiro controle aparece implementado em diversos pontos do projeto. O segundo não é aplicado de forma uniforme.

Isso pode criar situações em que um usuário autenticado tenha acesso a informações ou operações que deveriam estar restritas aos objetos relacionados à sua própria conta.

O problema é especialmente relevante porque a aplicação trabalha com informações pessoais, documentos, solicitações e benefícios.

---

## 2.4 Impacto

Caso essa ausência de verificação de propriedade possa ser explorada em um endpoint específico, um usuário autenticado poderia potencialmente:

* consultar dados de outros usuários;
* modificar recursos pertencentes a outros usuários;
* enviar documentos associados a outro aluno;
* excluir recursos que não pertencem ao usuário;
* obter informações que deveriam estar restritas ao seu próprio perfil.

O impacto dependeria do endpoint e do recurso afetado.

---

## 2.5 Como poderia ser corrigido

Uma abordagem mais segura seria combinar as permissões por perfil com filtros baseados no usuário autenticado.

Por exemplo:

```python
def get_queryset(self):
    return Solicitacao.objects.filter(
        aluno__usuario=self.request.user
    )
```

Também poderia ser utilizada uma permissão específica para verificar a propriedade do objeto antes de permitir operações de leitura ou alteração.

No caso de operações que recebem um `pk`, como o envio de documentos, deveria existir uma validação equivalente a:

```python
aluno = get_object_or_404(
    Aluno,
    pk=pk,
    usuario=request.user
)
```

É importante observar que o próprio projeto já possui um exemplo positivo dessa abordagem. O `ChamadoViewSet`, por exemplo, realiza filtragem baseada no usuário autenticado:

```python
if usuario.tipo == 'aluno':
    return Chamado.objects.filter(
        aluno__usuario=self.request.user
    )
elif usuario.tipo == 'assistente_social':
    return Chamado.objects.filter(
        assistente_social__usuario=usuario
    )
```

Esse padrão poderia ser utilizado como referência para revisar outros ViewSets.

---

# 3. A02:2025 — Security Misconfiguration

## 3.1 Identificação do risco

Foram identificadas diversas configurações que tornam a aplicação mais permissiva do que seria recomendável em um ambiente de produção.

Entre os principais pontos estão:

* `DEBUG` configurado com valor padrão `True`;
* CORS permitindo qualquer origem;
* credenciais habilitadas juntamente com CORS amplo;
* mecanismos de segurança ativados somente quando `DEBUG=False`;
* documentação Swagger disponibilizada publicamente;
* `BrowsableAPIRenderer` habilitado.

Esses elementos caracterizam um problema de **Security Misconfiguration**, pois a segurança da aplicação depende de configurações que podem permanecer excessivamente permissivas.

---

## 3.2 Evidência 1 — DEBUG habilitado por padrão

No arquivo `settings.py` existe:

```python
DEBUG = config(
    'DEBUG',
    default=True,
    cast=bool
)
```

O problema está principalmente no valor padrão:

```python
default=True
```

Caso a variável de ambiente não esteja corretamente configurada, a aplicação poderá iniciar com `DEBUG` habilitado.

Em produção, o modo de debug não deve permanecer habilitado.

---

## 3.3 Evidência 2 — CORS excessivamente permissivo

Também foi encontrada a configuração:

```python
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```

A primeira configuração permite requisições provenientes de qualquer origem.

A segunda permite o uso de credenciais em requisições cross-origin.

O ideal é definir explicitamente quais aplicações frontend podem acessar a API, no caso o front do próprio projeto.

---

## 3.4 Evidência 3 — Configurações de segurança dependentes de DEBUG

As configurações de segurança estão dentro do bloco:

```python
if not DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

Isso significa que essas proteções somente são ativadas quando `DEBUG` está desabilitado.

A abordagem é válida quando existe uma separação correta entre desenvolvimento e produção, mas torna ainda mais importante garantir que o ambiente de produção nunca seja executado com `DEBUG=True`.

---

## 3.5 Evidência 4 — Documentação da API pública

O `urls.py` configura a documentação Swagger como pública:

```python
schema_view = get_schema_view(
    ...,
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=[],
)
```

A documentação da API pode ser útil durante o desenvolvimento, mas disponibilizar informações detalhadas sobre endpoints publicamente pode facilitar o reconhecimento da estrutura da aplicação.

Em um ambiente de produção, poderia ser mais adequado restringir o acesso à documentação ou disponibilizá-la somente em ambientes de desenvolvimento.

---

## 3.6 Evidência complementar — análise anterior com OWASP ZAP

O relatório anterior de segurança apresentou achados relacionados à configuração da aplicação, incluindo:

* ausência de `X-Frame-Options`;
* ausência de Content Security Policy;
* ausência de `X-Content-Type-Options`;
* exposição de informações relacionadas à aplicação.

Esses resultados são utilizados apenas como **evidência histórica/complementar**, pois foram obtidos em uma análise anterior e não devem ser tratados automaticamente como comprovação de que todos esses problemas continuam presentes na versão atual.

---

## 3.7 Impacto

Uma configuração de segurança excessivamente permissiva pode:

* aumentar a superfície de ataque;
* facilitar o reconhecimento da API;
* permitir origens não previstas consumirem a aplicação;
* expor informações de desenvolvimento;
* reduzir a proteção contra ataques baseados em navegador;
* aumentar o impacto de uma eventual falha de autenticação ou autorização.

---

## 3.8 Como poderia ser corrigido

O primeiro passo seria alterar o comportamento padrão de `DEBUG`:

```python
DEBUG = config(
    'DEBUG',
    default=False,
    cast=bool
)
```

Além disso, o CORS deveria utilizar uma lista explícita de origens confiáveis, por exemplo:

```python
CORS_ALLOWED_ORIGINS = [
    "https://frontend.exemplo.com",
]
```

Em vez de:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

A documentação Swagger poderia ser protegida por autenticação ou disponibilizada somente em ambientes de desenvolvimento.

Também seria importante manter as configurações de segurança HTTP devidamente configuradas no ambiente de produção.

---

# 4. A09:2025 — Security Logging and Alerting Failures

## 4.1 Identificação do risco

Foi encontrado um problema relacionado ao registro de informações durante o processo de autenticação.

O sistema realiza integração com o serviço externo de autenticação SUAP. Durante essa operação, existem comandos `print()` utilizados para registrar informações da requisição e da resposta.

O problema é que os dados registrados podem conter informações sensíveis relacionadas à autenticação.

---

## 4.2 Evidência encontrada

No processo de troca do código de autenticação, existe uma estrutura semelhante a:

```python
data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": settings.SOCIAL_AUTH_SUAP_REDIRECT_URI,
    "client_id": settings.SOCIAL_AUTH_SUAP_KEY,
    "client_secret": settings.SOCIAL_AUTH_SUAP_SECRET,
}
```

Logo depois, o código realiza:

```python
print("data", data)
```

Também existe:

```python
print("response", token_response.json())
```

O primeiro `print()` é especialmente problemático porque o objeto `data` contém um campo `client_secret`.

Mesmo que o valor real do segredo não esteja exposto diretamente no código-fonte, o código está estruturado de maneira que esse segredo possa ser enviado para o mecanismo de saída/log do ambiente onde a aplicação estiver sendo executada.

---

## 4.3 Justificativa

Logs são importantes para diagnosticar problemas e detectar incidentes de segurança.

Entretanto, informações de autenticação, tokens, segredos de clientes e outros dados sensíveis não devem ser registrados indiscriminadamente.

Além disso, não foi identificada nos pontos analisados uma estratégia específica de logging de segurança e alertas para eventos importantes de autenticação.

O problema, portanto, não é simplesmente utilizar logs, mas sim utilizar mecanismos de logging de maneira inadequada, especialmente durante operações de autenticação.

---

## 4.4 Impacto

Caso logs contendo informações sensíveis sejam armazenados ou disponibilizados para pessoas ou sistemas que não deveriam ter acesso a essas informações, pode ocorrer:

* exposição de credenciais;
* comprometimento de mecanismos de autenticação;
* vazamento de informações sensíveis;
* dificuldade para controlar quem possui acesso aos dados registrados;
* aumento do impacto de uma eventual invasão do ambiente de execução.

---

## 4.5 Como poderia ser corrigido

Os `print()` deveriam ser removidos ou substituídos por um sistema de logging apropriado.

Por exemplo:

```python
import logging

logger = logging.getLogger(__name__)
```

Em vez de:

```python
print("data", data)
```

poderia ser registrado somente o necessário:

```python
logger.info(
    "Iniciando troca de código de autenticação"
)
```

Nunca deveriam ser registrados diretamente:

* `client_secret`;
* tokens de acesso;
* refresh tokens;
* senhas;
* códigos de autenticação;
* outros segredos.

Também é recomendável configurar níveis de log e mecanismos de monitoramento para eventos importantes, como:

* falhas repetidas de autenticação;
* erros de integração com o provedor de autenticação;
* alterações de permissões;
* acessos suspeitos;
* erros internos recorrentes.

---

# 5. A10:2025 — Mishandling of Exceptional Conditions

## 5.1 Identificação do risco

Foi identificado um problema no tratamento de exceções em endpoints relacionados às notificações.

O código captura qualquer exceção utilizando:

```python
except Exception as e:
```

e devolve diretamente a mensagem da exceção para o cliente.

---

## 5.2 Evidência encontrada

No `notificacoes.py`, existe um tratamento semelhante a:

```python
except Exception as e:
    return Response(
        {"error": str(e)},
        status=status.HTTP_400_BAD_REQUEST
    )
```

O mesmo padrão aparece em mais de uma operação.

Existem dois problemas principais nessa implementação.

### Primeiro problema: exposição da mensagem interna

O código utiliza:

```python
str(e)
```

e envia o resultado diretamente para o cliente.

Isso significa que uma mensagem gerada internamente pela aplicação pode ser transformada em uma resposta da API.

Dependendo do erro, essa mensagem pode revelar:

* nomes de tabelas;
* nomes de campos;
* detalhes de banco de dados;
* caminhos internos;
* informações sobre bibliotecas;
* detalhes da implementação.

### Segundo problema: tratamento genérico de qualquer exceção

A aplicação captura:

```python
Exception
```

e transforma qualquer erro em:

```python
HTTP 400 BAD REQUEST
```

Porém, nem todo erro representa uma requisição inválida.

Um erro inesperado do servidor, por exemplo, não deveria necessariamente ser tratado como erro 400.

---

## 5.3 Justificativa

O tratamento de exceções deve diferenciar erros esperados de situações inesperadas.

Erros esperados podem ser transformados em respostas controladas para o cliente.

Já erros inesperados devem ser registrados internamente e tratados de forma apropriada, sem revelar detalhes da implementação.

A utilização de:

```python
except Exception
```

juntamente com:

```python
str(e)
```

e:

```python
HTTP_400_BAD_REQUEST
```

dificulta essa separação.

---

## 5.4 Impacto

Essa implementação pode:

* revelar informações internas da aplicação;
* auxiliar um atacante durante o reconhecimento do sistema;
* dificultar a identificação correta de erros;
* mascarar problemas internos como erros do cliente;
* dificultar o monitoramento e diagnóstico da aplicação.

---

## 5.5 Como poderia ser corrigido

O ideal seria capturar somente as exceções esperadas.

Por exemplo:

```python
try:
    ...
except Notificacao.DoesNotExist:
    return Response(
        {"error": "Notificação não encontrada."},
        status=status.HTTP_404_NOT_FOUND
    )
```

Para erros inesperados, seria preferível registrar o erro internamente:

```python
logger.exception("Erro ao processar notificação")
```

e retornar ao usuário uma mensagem genérica:

```python
return Response(
    {"error": "Ocorreu um erro interno."},
    status=status.HTTP_500_INTERNAL_SERVER_ERROR
)
```

Dessa maneira, o usuário recebe somente a informação necessária, enquanto os detalhes técnicos permanecem nos logs internos.

---

# 6. Resumo dos riscos identificados

| Risco                                            | Situação encontrada                                                          | Evidência principal                                                                  | Correção sugerida                                                        |
| ------------------------------------------------ | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| **A01 — Broken Access Control**                  | Possível ausência de controle de propriedade dos objetos em alguns endpoints | `ModelViewSet` com `queryset` geral e operações sem verificação explícita do usuário | Filtrar `queryset` pelo usuário e utilizar permissões de objeto          |
| **A02 — Security Misconfiguration**              | Configurações excessivamente permissivas                                     | `DEBUG=True` por padrão, CORS amplo, Swagger público                                 | Restringir configurações e separar corretamente desenvolvimento/produção |
| **A09 — Security Logging and Alerting Failures** | Dados sensíveis podem ser enviados para logs                                 | `print("data", data)` contendo `client_secret`                                       | Remover dados sensíveis dos logs e utilizar logging estruturado          |
| **A10 — Mishandling of Exceptional Conditions**  | Exceções internas são devolvidas diretamente ao cliente                      | `except Exception as e` + `str(e)` + HTTP 400                                        | Tratar exceções específicas e retornar mensagens genéricas               |

---

# 7. Considerações sobre os demais riscos

Durante a análise, os demais itens do OWASP Top 10 também foram considerados.

O risco **A03:2025 — Software Supply Chain Failures** foi deliberadamente excluído, conforme solicitado no enunciado da atividade.

Para **A05:2025 — Injection**, não foi encontrada, na análise realizada, evidência suficientemente forte de utilização de SQL construído manualmente, `cursor.execute()` inseguro, `eval()` ou outro mecanismo que permitisse afirmar a existência de uma vulnerabilidade de injeção.

Em relação ao **A07:2025 — Authentication Failures**, o projeto utiliza autenticação integrada ao SUAP e tokens JWT. A existência desses mecanismos, por si só, não representa uma vulnerabilidade. Não foi encontrada evidência suficiente, nesta análise, para afirmar uma falha específica de autenticação.

Dessa forma, optou-se por não classificar esses itens como vulnerabilidades sem evidências mais concretas.

---

# 9. Conclusão

A análise identificou quatro pontos que podem ser relacionados aos riscos do OWASP Top 10:2025:

1. **A01 — Broken Access Control**
2. **A02 — Security Misconfiguration**
3. **A09 — Security Logging and Alerting Failures**
4. **A10 — Mishandling of Exceptional Conditions**

O problema mais relevante encontrado está relacionado ao **controle de acesso**, pois alguns recursos utilizam permissões baseadas no perfil do usuário, mas não apresentam de maneira uniforme uma verificação de propriedade dos objetos.

Também foram identificadas configurações excessivamente permissivas, principalmente relacionadas a `DEBUG`, CORS e exposição da documentação da API.

Outro ponto importante está no processo de autenticação, onde informações sensíveis podem ser registradas por meio de `print()`. Por fim, o tratamento genérico de exceções pode expor informações internas da aplicação e classificar incorretamente erros internos como erros de requisição.

A análise demonstra que mecanismos de segurança não devem ser aplicados somente no nível de autenticação. É necessário considerar também autorização por objeto, configuração segura do ambiente, proteção das informações registradas em logs e tratamento adequado de exceções.
