# (como vai ser salvo no banco, como vai ser apresentado)
TIPO_DE_AUXILIO = [
    ("Auxílio Transporte", "auxilio_transporte"),
    ("Auxílio Moradia", "auxilio_moradia"),
    ("Alimentação Estudantil", "alimentacao_estudantil"),
    ("Apoio à Formação Estudantil", "apoio_formacao_estudantil"),
    ("Auxílios Eventuais", "auxilios_eventuais"),
    ("Curso de Idiomas", "curso_idiomas"),
    ("Outros", "outros")
]
TIPO_DE_CHAMADO_CHOICES = [
    ("alteracao_documentos", "Alteração de documentos"), 
    ("arquivos_pendentes", "Arquivos pendentes"),
    ("justificacao", "Justificação"),
    ("outro", "Outro")
]

STATUS_FORMULARIO_CHOICES = [
    ("aberto", "Aberto"),
    ("concluido", "Concluído"),
    ("rascunho", "Rascunho")
]

SOLICITADOS_CHOICES = [
    ("todos", "Todos os alunos"), 
    ("auxilio", "Alunos do auxílio selecionado"), 
    ("individual", "Alunos selecionados individualmente")
]

TIPO_PERGUNTA_CHOICES = [
    ('paragrafo', 'Parágrafo'),
    ('multipla_escolha', 'Múltipla escolha'),
    ('caixa_selecao', 'Caixas de seleção')
]

TIPO_DOCUMENTO_CHOICES = [
    ("rg", "RG"),
    ("cpf", "CPF"),
    ("comprovante_residencia", "Comprovante de residência"),
    ("historico_escolar", "Histórico escolar"),
    ("comprovante_renda", "Comprovante de renda"),
    ("comprovante_ausencia_renda", "Comprovante de ausência de renda"),
    ("outros", "Outros")
]

STATUS_PERGUNTA_CHOICES = [
    ("respondida", "Respondida"),
    ("nao_respondida", "Não respondida")
]

STATUS_CHAMADO_CHOICES = [
    ("em_analise", "Em análise"),
    ("concluido", "Concluído"),
    ("fechado", "Fechado")
]

STATUS_NOTIFICACAO_CHOICES = [
    ("enviada", "Enviada"),
    ("nao_lida", "Não lida"),
    ("lida", "Lida")
]

CURSOS_IFRN_NATAL_CENTRAL = [
    # Técnico Integrado (Ensino Médio)
    ("administracao", "Administração"), 
    ("controle_ambiental", "Controle Ambiental"), 
    ("edificacoes", "Edificações"), 
    ("eletrotecnica", "Eletrotécnica"), 
    ("geologia", "Geologia"), 
    ("informatica_internet", "Informática para Internet"), 
    ("manutencao_suporte", "Manutenção e Suporte em Informática"), 
    ("mecanica", "Mecânica"), 
    ("mineracao", "Mineração"), 

    # Técnico Subsequente
    ("controle_ambiental_sub", "Controle Ambiental (Subsequente)"), 
    ("edificacoes_sub", "Edificações (Subsequente)"), 
    ("eletrotecnica_sub", "Eletrotécnica (Subsequente)"), 
    ("geologia_sub", "Geologia (Subsequente)"), 
    ("mecanica_sub", "Mecânica (Subsequente)"), 
    ("mineracao_sub", "Mineração (Subsequente)"), 
    ("petroleo_gas_sub", "Petróleo e Gás (Subsequente)"), 
    ("redes_comp_sub", "Redes de Computadores (Subsequente)"), 
    ("manutencao_suporte_sub", "Manutenção e Suporte em Informática (Subsequente)"), 
    ("informatica_sub", "Informática (Subsequente)"), 
    ("seguranca_trabalho_sub", "Segurança do Trabalho (Subsequente)"), 
    ("estradas_sub", "Estradas (Subsequente)"), 

    # Cursos FIC
    ("implanta_voip_fic", "Implantação de Serviços VoIP (FIC)"),
    ("aplicador_ceramico_fic", "Aplicador de Revestimento Cerâmico (FIC)"),
    ("artesanato_reciclavel_fic", "Artesanato com Material Reciclável (FIC)"),

    # Graduação – Engenharias
    ("engenharia_civil", "Engenharia Civil"),
    ("engenharia_energia", "Engenharia de Energia"),
    ("engenharia_sanitaria", "Engenharia Sanitária e Ambiental"),

    # Graduação – Tecnologias (Tec. Superiores)
    ("tecnologia_ads", "Tecnologia em Análise e Desenvolvimento de Sistemas"),
    ("tecnologia_com_exterior", "Tecnologia em Comércio Exterior"),
    ("tecnologia_gestao_publica", "Tecnologia em Gestão Pública"),
    ("tecnologia_redes_comp", "Tecnologia em Redes de Computadores"),

    # Pós‑Graduação – Especializações
    ("esp_seguranca_trab", "Especialização em Engenharia de Segurança do Trabalho"),
    ("esp_ensino_geociencias", "Especialização em Ensino de Geociências"),
    ("esp_gestao_ambiental", "Especialização em Gestão Ambiental"),

    # Pós‑Graduação – Mestrados
    ("mestrado_prof_ensino_fis", "Mestrado Profissional em Ensino de Física"),
    ("mestrado_prof_recursos_nat", "Mestrado Profissional em Uso Sustentável de Recursos Naturais"),

    # Pós‑Graduação – Doutorado
    ("doutorado_educacao_prof", "Doutorado Acadêmico em Educação Profissional"),
]

STATUS_SOLICITACAO_CHOICES = [
    ("em_analise", "Em Análise"),
    ("deferido", "Deferido"),
    ("indeferido", "Indeferido"),
    ("deferido_sem_recurso", "Deferido sem recurso"),
    ("finalizado", "Finalizado"),
]

STATUS_BENEFICIO_CHOICES = [
    ("ativo", "Ativo"),
    ("inativo", "Inativo")
]

TIPO_NOTIFICACAO_CHOICES = [
    ("formulario", "Formulário"),
    ("chamado", "Chamado"),
    ("geral", "Geral")
]

CAMPUS_IFRN_CHOICES = [
    ("apodi", "Apodi"),
    ("caico", "Caicó"),
    ("canguaretama", "Canguaretama"),
    ("ceara_mirim", "Ceará-Mirim"),
    ("currais_novos", "Currais Novos"),
    ("ipanguacu", "Ipanguaçu"),
    ("joao_camara", "João Câmara"),
    ("jucurutu", "Jucurutu"),
    ("lajes", "Lajes"),
    ("macau", "Macau"),
    ("mossoro", "Mossoró"),
    ("Natal Central", "Natal-Central"),
    ("Natal-Cidade-Alta","Cidade Alta"),
    ("natal_zona_norte", "Natal-Zona Norte"),
    ("nova_cruz", "Nova Cruz"),
    ("parelhas", "Parelhas"),
    ("parnamirim", "Parnamirim"),
    ("pau_dos_ferros", "Pau dos Ferros"),
    ("santa_cruz", "Santa Cruz"),
    ("sao_goncalo", "São Gonçalo do Amarante"),
    ("sao_paulo_potengi", "São Paulo do Potengi")
]

